Go Digital Technology Technical Assessment

•	Overview
o	This repository contains the solution for the Go Digital Technology Consulting LLP technical assessment. The task involves automating AWS resource creation and deployment using Terraform, Docker, AWS Lambda, and Jenkins CI/CD pipeline.

•	Task Requirements
o	The project performs the following steps:
	Develop a Python application that:
•	Reads data from AWS S3
•	Pushes data to AWS RDS
•	If RDS is unavailable, pushes data to AWS Glue Database
	Create a Docker image for this Python application and push it to AWS ECR.
	Deploy an AWS Lambda function using the Docker image.
	Use Terraform to create all required AWS resources.
	Set up a Jenkins CI/CD pipeline to automate deployment.

•	Technologies Used
o	Python (Data processing script)
o	Docker (Containerization of application)
o	AWS Services:
	S3 (Storage)
	RDS (Relational Database Service)
	Glue Database (Alternative storage)
	ECR (Elastic Container Registry)
	Lambda (Serverless compute function)
o	Terraform (Infrastructure as Code for AWS resources)
o	Jenkins (CI/CD pipeline for automation)
