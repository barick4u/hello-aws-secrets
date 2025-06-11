pipeline {
    agent any

    environment {
        AWS_CLI = "/usr/local/bin/aws"
        SECRET_ID = "myapp/hello-world"
        REGION = "ap-south-1"
        PATH = "/opt/homebrew/bin:$PATH" // Ensure jq is available
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/barick4u/hello-aws-secrets.git'
            }
        }

        stage('Fetch AWS Secret') {
            steps {
                sh '''
                echo "Fetching secrets from AWS..."
                SECRET=$($AWS_CLI secretsmanager get-secret-value \
                  --region $REGION \
                  --secret-id $SECRET_ID \
                  --query SecretString \
                  --output text)

                USERNAME=$(echo "$SECRET" | jq -r '.username')
                PASSWORD=$(echo "$SECRET" | jq -r '.password')

                echo "Username: $USERNAME"
                echo "Password: $PASSWORD"
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t hello-aws-secret .'
            }
        }

        stage('Scan with Trivy') {
            steps {
                sh 'trivy image hello-aws-secret || true'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d --name hello-secret-app hello-aws-secret'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker containers...'
            sh 'docker rm -f hello-secret-app || true'
        }
    }
}
