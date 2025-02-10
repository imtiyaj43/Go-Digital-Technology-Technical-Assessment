pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID = '971422687529'
        AWS_ECR_URL = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        REPO_NAME = 'go-digital-repo'
        IMAGE_NAME = 'my-python-app'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/imtiyaj43/Go-Digital-Technology-Technical-Assessment.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME -f src/Dockerfile src/'
            }
        }

        stage('Push to ECR') {
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

        stage('Terraform Apply') {
            steps {
                sh 'cd terraform && terraform init && terraform apply -auto-approve'
            }
        }

        stage('Deploy Lambda') {
            steps {
                sh '''
                aws lambda update-function-code --function-name myLambdaFunction --image-uri $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest
                '''
            }
        }
    }
}
