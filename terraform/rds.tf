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
