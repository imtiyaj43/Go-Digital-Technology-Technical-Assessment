Go Digital Technology Technical Assessment

•	Overview
    This repository contains the solution for the Go Digital Technology Consulting LLP technical assessment. The task involves automating AWS resource creation and deployment using Terraform, Docker, AWS Lambda, and Jenkins CI/CD pipeline.

•	Task Requirements
    The project performs the following steps:
        1. Develop a Python application that:
            Reads data from AWS S3
            Pushes data to AWS RDS
            If RDS is unavailable, pushes data to AWS Glue Database
        2. Create a Docker image for this Python application and push it to AWS ECR.
        3. Deploy an AWS Lambda function using the Docker image.
        4. Use Terraform to create all required AWS resources.
        5. Set up a Jenkins CI/CD pipeline to automate deployment.

•	Technologies Used
    1. Python (Data processing script)
    2. Docker (Containerization of application)
    3. AWS Services:
          S3 (Storage)
          RDS (Relational Database Service)
          Glue Database (Alternative storage)
          ECR (Elastic Container Registry)
          Lambda (Serverless compute function)
    4. Terraform (Infrastructure as Code for AWS resources)
    5. Jenkins (CI/CD pipeline for automation)
