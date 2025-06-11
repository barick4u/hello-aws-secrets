pipeline {
  agent any

  environment {
    AWS_CLI = "/Users/satyajitbarick/jenkins-awscli/bin/aws"
    IMAGE_NAME = "hello-secrets"
    AWS_REGION = "ap-south-1"
    SECRET_ID  = "myapp/hello-world"
  }

  stages {
    stage('Clone Repo') {
      steps {
        git branch: 'main', url: 'https://github.com/barick4u/hello-aws-secrets.git'
      }
    }

    stage('Fetch AWS Secrets') {
      steps {
        script {
          def secret = sh(
            script: "${AWS_CLI} secretsmanager get-secret-value --region ${AWS_REGION} --secret-id ${SECRET_ID} --query SecretString --output text",
            returnStdout: true
          ).trim()

          def creds = readJSON text: secret
          env.MY_SECRET_USER = creds.username
          env.MY_SECRET_PASS = creds.password
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $IMAGE_NAME .'
      }
    }

    stage('Scan with Trivy') {
      steps {
        sh 'trivy image $IMAGE_NAME || true'
      }
    }

    stage('Run Docker with Secrets') {
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
      echo "Pipeline finished!"
    }
  }
}
