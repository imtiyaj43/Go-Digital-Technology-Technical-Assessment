resource "aws_ecr_repository" "go_digital_repo" {
  name                 = "go-digital-repo"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.go_digital_repo.repository_url
}
