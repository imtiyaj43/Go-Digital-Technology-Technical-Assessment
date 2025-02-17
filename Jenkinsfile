pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID = '971422687529'
        AWS_ECR_URL = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        REPO_NAME = 'go-digital-repo'
        IMAGE_NAME = 'my-python-app'
        LAMBDA_FUNCTION_NAME = 's3-to-rds-lambda'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/imtiyaj43/Go-Digital-Technology-Technical-Assessment.git'
            }
        }
        stage('Terraform Apply') {  // First, create the infrastructure
            steps {
                script {
                    sh '''
                    export PATH=$PATH:/usr/local/bin
                    cd terraform
                    terraform init
                    terraform apply -auto-approve
                    '''
                }
            }
        }
        stage('Build Docker Image') { // Now, build the Docker image
            steps {
                sh 'docker build -t $IMAGE_NAME -f src/Dockerfile src/'
            }
        }
        stage('Push to ECR') { // Push the image to ECR
            steps {
                withCredentials([aws(credentialsId: 'aws-credentials')]) {
                    sh '''
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ECR_URL
                    docker tag $IMAGE_NAME:latest $AWS_ECR_URL/$REPO_NAME:latest
                    docker push $AWS_ECR_URL/$REPO_NAME:latest
                    '''
                }
            }
        }
        stage('Update Lambda Function') { // Deploy Lambda with new Docker Image
            steps {
                withCredentials([aws(credentialsId: 'aws-credentials')]) {
                    sh '''
                    aws lambda update-function-code \
                        --function-name $LAMBDA_FUNCTION_NAME \
                        --image-uri $AWS_ECR_URL/$REPO_NAME:latest \
                        --region $AWS_REGION
                    '''
                }
            }
        }
        stage('Test Lambda Function') { // Invoke Lambda function to verify deployment
            steps {
                withCredentials([aws(credentialsId: 'aws-credentials')]) {
                    sh '''
                    aws lambda invoke \
                        --function-name $LAMBDA_FUNCTION_NAME \
                        --region $AWS_REGION \
                        --payload '{}' response.json
                    cat response.json
                    '''
                }
            }
        }
    }
}
