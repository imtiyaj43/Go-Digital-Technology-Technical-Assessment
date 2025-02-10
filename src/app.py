import boto3
import pymysql
import json

session = boto3.Session(region_name="ap-south-1")  # Explicitly set region

# AWS clients
s3 = boto3.client('s3')
glue = boto3.client('glue')

# RDS Credentials
RDS_HOST = "terraform-20250210043914835200000001.cdaw0w26oeok.ap-south-1.rds.amazonaws.com"
RDS_USER = "admin"
RDS_PASSWORD = "Shaikh14"
RDS_DB = "godigitaldb"

def read_from_s3(bucket_name, file_key):
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
        return "Data successfully written to RDS"
    except Exception as e:
        print(f"RDS write failed: {e}")
        return None

def write_to_glue(data):
    """Write data to AWS Glue (dummy function for now)"""
    print("Writing data to Glue...")
    return "Data successfully written to Glue"

def main():
    """Main execution"""
    bucket_name = "go-digital-data-bucket"
    file_key = "data.json"

    data = read_from_s3(bucket_name, file_key)

    # Try to write to RDS first
    if write_to_rds(data) is None:
        write_to_glue(data)

if __name__ == "__main__":
    main()
