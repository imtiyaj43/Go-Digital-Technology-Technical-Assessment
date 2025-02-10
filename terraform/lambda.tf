resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role1"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# Attach IAM Policies for Lambda to Access S3, RDS, and ECR
resource "aws_iam_policy" "lambda_permissions" {
  name        = "lambda_permissions"
  description = "Permissions for Lambda to access S3, RDS, and ECR"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.data_bucket.id}",
        "arn:aws:s3:::${aws_s3_bucket.data_bucket.id}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["rds:*"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage", "ecr:GetAuthorizationToken"],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_permissions.arn
}

# Lambda Function using ECR Image
resource "aws_lambda_function" "s3_to_rds_lambda" {
  function_name = "s3-to-rds-lambda"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.go_digital_repo.repository_url}:latest"
  timeout       = 60

  environment {
    variables = {
      RDS_HOST     = aws_db_instance.rds_db.endpoint
      RDS_USER     = "admin"
      RDS_PASSWORD = "Shaikh14"
      RDS_DB       = "godigitaldb"
      BUCKET_NAME  = aws_s3_bucket.data_bucket.id
    }
  }
}

output "lambda_function_arn" {
  value = aws_lambda_function.s3_to_rds_lambda.arn
}
