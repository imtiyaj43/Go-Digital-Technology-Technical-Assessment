resource "aws_s3_bucket" "data_bucket" {
  bucket = "go-digital-data-bucket"
  acl    = "private"

  tags = {
    Name        = "Go Digital Data Bucket"
    Environment = "Dev"
  }
}

resource "aws_db_instance" "rds_db" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  db_name              = "godigitaldb"
  username             = "admin"
  password             = "Shaikh14"
  parameter_group_name = "default.mysql8.0"
  publicly_accessible  = false
  skip_final_snapshot  = true

  tags = {
    Name        = "Go Digital RDS Database"
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

