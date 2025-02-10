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

    }
}
