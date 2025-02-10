resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

resource "aws_s3_bucket" "data_bucket" {
  bucket = "my-data-bucket-${random_string.suffix.result}"
}

output "s3_bucket_name" {
  value = aws_s3_bucket.your_bucket.id
}
