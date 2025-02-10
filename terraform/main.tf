resource "aws_s3_bucket" "data_bucket" {
  bucket = "go-digital-data-bucket"
  acl    = "private"

  tags = {
    Name        = "Go Digital Data Bucket"
    Environment = "Dev"
  }
}

resource "aws_ecr_repository" "docker_repo" {
  name = "go-digital-repo"

  image_scanning_configuration {
    scan_on_push = true # Automatically scan for vulnerabilities
  }

  tags = {
    Name        = "Go Digital ECR Repository"
    Environment = "Dev"
  }
}

resource "aws_lambda_function" "my_lambda" {
  function_name    = "myLambdaFunction"
  role            = aws_iam_role.lambda_exec.arn
  package_type    = "Image"
  image_uri       = "${aws_ecr_repository.go_digital_repo.repository_url}:latest"
  timeout         = 30
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_policy_attach" {
  name       = "lambda-policy-attach"
  roles      = [aws_iam_role.lambda_exec.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

