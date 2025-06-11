pipeline {
    agent any

    environment {
        AWS_CLI = "/usr/local/bin/aws"  // Adjust if path differs
        SECRET_ID = "myapp/hello-world"
        REGION = "ap-south-1"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/barick4u/hello-aws-secrets.git'
            }
        }

        stage('Fetch AWS Secret') {
            #steps {
                #script {
               #     def secret = sh(
              #          script: "${AWS_CLI} secretsmanager get-secret-value --region ${REGION} --secret-id ${SECRET_ID} --query SecretString --output text",
             #           returnStdout: true
            #        ).trim()
           #         echo "Fetched secret: ${secret}" // Don't do this in real prod pipelines (for security)
          #      }
         #   }
        #}
	steps {
        sh '''
          echo "Fetching secrets from AWS..."
          SECRET=$(aws secretsmanager get-secret-value \
            --region ap-south-1 \
            --secret-id myapp/hello-world \
            --query SecretString \
            --output text)

          USERNAME=$(echo "$SECRET" | jq -r '.username')
          PASSWORD=$(echo "$SECRET" | jq -r '.password')

          echo "Username: $USERNAME"
          echo "Password: $PASSWORD"
        '''
      }
    }
  }
}

        stage('Docker Build') {
            steps {
                sh 'docker build -t hello-aws-secret .'
            }
        }

        stage('Scan with Trivy') {
            steps {
                sh 'trivy image hello-aws-secret || true'  // ignore failure if Trivy not installed
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
