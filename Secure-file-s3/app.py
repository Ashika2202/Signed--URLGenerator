# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import boto3

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# AWS S3 configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_REGION = os.getenv('AWS_REGION')
S3_BUCKET = os.getenv('S3_BUCKET_NAME')

s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name=S3_REGION)

# Local folder to temporarily store files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            local_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(local_path)
            try:
                s3.upload_file(local_path, S3_BUCKET, filename)
                flash('File uploaded successfully!', 'success')
            except Exception as e:
                flash(f'Upload failed: {str(e)}', 'danger')
            finally:
                os.remove(local_path)
            return redirect(url_for('upload'))
    return render_template('upload.html')

@app.route('/files')
def files():
    try:
        objects = s3.list_objects_v2(Bucket=S3_BUCKET).get('Contents', [])
    except Exception as e:
        flash(f'Could not retrieve files: {str(e)}', 'danger')
        objects = []
    return render_template('files.html', files=objects)

@app.route('/download/<filename>')
def download(filename):
    local_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        s3.download_file(S3_BUCKET, filename, local_path)
        return send_file(local_path, as_attachment=True)
    except Exception as e:
        flash(f'Failed to download file: {str(e)}', 'danger')
        return redirect(url_for('files'))
    
if __name__ == '__main__':
    app.run(debug=True)

