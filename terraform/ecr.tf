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
