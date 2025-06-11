pipeline {
  agent any

  environment {
    AWS_CLI = "/usr/local/bin/aws"
    SECRET_ID = "myapp/hello-world"
    REGION = "ap-south-1"
    PATH = "/opt/homebrew/bin:$PATH:/usr/local/bin:$PATH"
  }

  stages {
    stage('Checkout Code') {
      steps {
        git branch: 'main', url: 'https://github.com/barick4u/hello-aws-secrets.git'
      }
    }

    stage('Fetch AWS Secret') {
      steps {
        withCredentials([
          usernamePassword(
            credentialsId: 'aws-creds',
            usernameVariable: 'AWS_ACCESS_KEY_ID',
            passwordVariable: 'AWS_SECRET_ACCESS_KEY'
          )
        ]) {
          sh '''
          echo "Fetching secrets from AWS..."
          export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
          export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

          SECRET=$($AWS_CLI secretsmanager get-secret-value \
              --region $REGION \
              --secret-id $SECRET_ID \
              --query SecretString \
              --output text)

          echo "$SECRET" | jq .
          USERNAME=$(echo "$SECRET" | jq -r '.username')
          PASSWORD=$(echo "$SECRET" | jq -r '.password')

          echo "USERNAME=$USERNAME" >> secret.env
          echo "PASSWORD=$PASSWORD" >> secret.env
          '''
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
        sh 'trivy image hello-aws-secret || true'
      }
    }

    stage('Run Docker Container') {
      steps {
        sh 'docker run --env-file secret.env hello-aws-secret'
      }
    }
  }

  post {
    always {
      echo 'Cleaning up...'
      sh 'docker rm -f hello-secret-app || true'
    }
  }
}
