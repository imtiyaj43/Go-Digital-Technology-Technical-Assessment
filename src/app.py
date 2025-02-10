import boto3
import pymysql
import json

# Create session explicitly
session = boto3.Session(region_name="ap-south-1")  

# AWS Clients (Use session)
s3 = session.client('s3')

# RDS Credentials
RDS_HOST = "terraform-20250210043914835200000001.cdaw0w26oeok.ap-south-1.rds.amazonaws.com"
RDS_USER = "admin"
RDS_PASSWORD = "Shaikh14"
RDS_DB = "godigitaldb"

def read_from_s3(bucket_name, file_key):
    """Read JSON data from S3"""
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except Exception as e:
        print(f"Error reading from S3: {e}")
        return None

def write_to_rds(data):
    """Write data to RDS MySQL"""
    try:
        conn = pymysql.connect(
            host=RDS_HOST, user=RDS_USER, password=RDS_PASSWORD, database=RDS_DB, connect_timeout=10
        )
        cursor = conn.cursor()
        
        # Fix: Use TEXT instead of JSON if needed
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                data TEXT
            )
        """)
        
        cursor.execute("INSERT INTO records (data) VALUES (%s)", (json.dumps(data),))
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Data successfully written to RDS")
        return True
    except Exception as e:
        print(f"❌ RDS write failed: {e}")
        return False

def main():
    """Main execution"""
    bucket_name = "go-digital-data-bucket"
    file_key = "data.json"

    # Step 1: Read from S3
    data = read_from_s3(bucket_name, file_key)
    if data is None:
        print("❌ No data found in S3. Check bucket and file key.")
        return
    
    # Step 2: Try writing to RDS
    if not write_to_rds(data):
        print("⚠️ Writing to RDS failed. Check RDS security settings or credentials.")

if __name__ == "__main__":
    main()
