resource "aws_s3_bucket" "data_bucket" {
  bucket = "go-digital-data-bucket"
  acl    = "private"

  tags = {
    Name        = "Go Digital Data Bucket"
    Environment = "Dev"
  }
}
