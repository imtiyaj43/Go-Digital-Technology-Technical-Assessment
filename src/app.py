import boto3
import pymysql
import json

# Initialize AWS clients
s3 = boto3.client('s3', region_name="ap-south-1")
glue = boto3.client('glue')

# RDS Credentials
RDS_HOST = "terraform-20250210043914835200000001.cdaw0w26oeok.ap-south-1.rds.amazonaws.com"
RDS_USER = "admin"
RDS_PASSWORD = "Shaikh14"
RDS_DB = "godigitaldb"

bucket_name = "my-data-bucket-ympp6p"
file_key = "data.json"

# Sample Data to Upload
sample_data = {"name": "Test User", "age": 25}

def upload_to_s3():
    """Uploads sample JSON data if not found"""
    try:
        s3.head_object(Bucket=bucket_name, Key=file_key)
        print("File already exists in S3. Skipping upload.")
    except:
        print("File not found. Uploading sample data...")
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=json.dumps(sample_data))

def read_from_s3():
    """Read JSON data from S3"""
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    content = response['Body'].read().decode('utf-8')
    return json.loads(content)

def write_to_rds(data):
    """Write data to RDS MySQL"""
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
        print("Data successfully written to RDS")
        return True
    except Exception as e:
        print(f"RDS write failed: {e}")
        return False

def write_to_glue(data):
    """Write data to AWS Glue (dummy function for now)"""
    print("Writing data to Glue...")
    return "Data successfully written to Glue"

def main():
    """Main execution"""
    upload_to_s3()  # Upload sample data first
    data = read_from_s3()  # Read from S3

    if not write_to_rds(data):  # If RDS fails, use Glue
        write_to_glue(data)

if __name__ == "__main__":
    main()
