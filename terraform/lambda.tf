# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

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

# ✅ Instead of creating a new IAM policy, reference the existing one
data "aws_iam_policy" "lambda_permissions" {
  name = "lambda_permissions"
}

# ✅ Attach the existing IAM policy
resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = data.aws_iam_policy.lambda_permissions.arn
}

# ✅ Ensure ECR repo exists before deploying Lambda
resource "aws_ecr_repository" "go_digital_repo" {
  name = "go-digital-repo"
}

# ✅ Lambda Function using ECR Image (only after image exists)
resource "aws_lambda_function" "s3_to_rds_lambda" {
  function_name = "s3-to-rds-lambda"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"

  # ✅ Ensure image exists before deploying Lambda
  image_uri = "${aws_ecr_repository.go_digital_repo.repository_url}:latest"

  timeout = 60

  environment {
    variables = {
      RDS_HOST     = aws_db_instance.rds_db.endpoint
      RDS_USER     = "admin"
      RDS_PASSWORD = "Shaikh14"
      RDS_DB       = "godigitaldb"
      BUCKET_NAME  = aws_s3_bucket.data_bucket.id
    }
  }

  depends_on = [aws_ecr_repository.go_digital_repo]
}

output "lambda_function_arn" {
  value = aws_lambda_function.s3_to_rds_lambda.arn
}

