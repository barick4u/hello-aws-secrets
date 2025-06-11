pipeline {
  agent any

  environment {
    IMAGE_NAME = "hello-secrets"
    AWS_REGION = "us-east-1"
    SECRET_ID  = "myapp/hello-world"
  }

  stages {
    stage('Checkout Code') {
      steps {
        git branch: 'main', url: 'https://github.com/barick4u/hello-aws-secrets.git'
      }
    }

    stage('Fetch AWS Secret') {
      steps {
        script {
          def secret = sh(script: "aws secretsmanager get-secret-value --region $AWS_REGION --secret-id $SECRET_ID --query SecretString --output text", returnStdout: true).trim()
          def creds = readJSON text: secret
          env.MY_SECRET_USER = creds.username
          env.MY_SECRET_PASS = creds.password
        }
      }
    }

    stage('Docker Build') {
      steps {
        sh 'docker build -t $IMAGE_NAME .'
      }
    }

    stage('Scan with Trivy') {
      steps {
        sh 'trivy image $IMAGE_NAME || true'
      }
    }

    stage('Run Docker Container') {
      steps {
        sh '''
        docker run --rm \
          -e MY_SECRET_USER=$MY_SECRET_USER \
          -e MY_SECRET_PASS=$MY_SECRET_PASS \
          $IMAGE_NAME
        '''
      }
    }
  }

  post {
    always {
      echo "Pipeline execution complete!"
    }
  }
}
