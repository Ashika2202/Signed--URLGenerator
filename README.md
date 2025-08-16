🔐 Signed URL Generator

This is a Python project that generates signed URLs for AWS S3 files.  
Signed URLs allow temporary access to private files in S3 without sharing your AWS keys

 About
- Built using Python and Boto3
- Creates secure pre-signed URLs
- Useful for file sharing without exposing credentials

How It Works
1. User requests a file from S3
2. The program generates a signed URL
3. The signed URL is valid for a limited time

Important Note
- Do not upload your AWS Access Keys to GitHub.  
- Keep them private in a .env file or environment variables.  

Author
Project developed by Ashika N
