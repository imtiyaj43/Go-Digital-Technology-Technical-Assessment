import boto3
import pymysql
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize AWS clients
s3 = boto3.client("s3", region_name="ap-south-1")
glue = boto3.client("glue")

# RDS Credentials
RDS_HOST = "terraform-20250210043914835200000001.cdaw0w26oeok.ap-south-1.rds.amazonaws.com"
RDS_USER = "admin"
RDS_PASSWORD = "Shaikh14"
RDS_DB = "godigitaldb"

# Fetch bucket name from environment variable
bucket_name = os.getenv("BUCKET_NAME", "default-bucket-name")
file_key = "data.json"

# Sample Data to Upload
sample_data = {"name": "Test User", "age": 25}

def upload_to_s3():
    """Uploads sample JSON data to S3 if not found."""
    try:
        s3.head_object(Bucket=bucket_name, Key=file_key)
        logging.info("File already exists in S3. Skipping upload.")
    except Exception as e:
        logging.info("File not found. Uploading sample data...")
        try:
            s3.put_object(Bucket=bucket_name, Key=file_key, Body=json.dumps(sample_data))
            logging.info("File uploaded successfully.")
        except Exception as upload_error:
            logging.error(f"Failed to upload file to S3: {upload_error}")

def read_from_s3():
    """Read JSON data from S3."""
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response["Body"].read().decode("utf-8")
        return json.loads(content)
    except Exception as e:
        logging.error(f"Error reading from S3: {e}")
        return None

def write_to_rds(data):
    """Write data to RDS MySQL."""
    try:
        conn = pymysql.connect(
            host=RDS_HOST, user=RDS_USER, password=RDS_PASSWORD, database=RDS_DB
        )
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS records (id INT AUTO_INCREMENT PRIMARY KEY, data JSON)")
        cursor.execute("INSERT INTO records (data) VALUES (%s)", (json.dumps(data),))
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Data successfully written to RDS.")
        return True
    except Exception as e:
        logging.error(f"RDS write failed: {e}")
        return False

def write_to_glue(data):
    """Write data to AWS Glue (dummy function for now)."""
    logging.info("Writing data to Glue...")
    return "Data successfully written to Glue"

def main():
    """Main execution."""
    logging.info(f"Using S3 Bucket: {bucket_name}")

    upload_to_s3()  # Upload sample data first
    data = read_from_s3()  # Read from S3

    if data:
        if not write_to_rds(data):  # If RDS fails, use Glue
            write_to_glue(data)
    else:
        logging.error("No data retrieved from S3. Exiting.")

if __name__ == "__main__":
    main()
