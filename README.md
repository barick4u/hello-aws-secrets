## 🛠️ How to Use This Project

This project demonstrates a secure Jenkins pipeline that fetches secrets from AWS Secrets Manager at runtime and passes them into a running Docker container.

### ✅ Prerequisites

- Jenkins (Freestyle or Pipeline job enabled)
- Docker installed on Jenkins machine
- AWS CLI installed and configured
- `jq` installed (used for parsing JSON secrets)
- Trivy installed (optional, for vulnerability scanning)

### 🔐 Jenkins Credentials Setup

Store your AWS credentials securely using Jenkins Credentials Manager:

1. Go to **Jenkins → Manage Jenkins → Credentials → Global**.
2. Add a new **Username/Password** credential:
   - ID: `aws-creds`
   - Username: Your **AWS Access Key ID**
   - Password: Your **AWS Secret Access Key**

This prevents hardcoding sensitive data into your Jenkinsfile.

### 🧪 Run the Pipeline

Once your Jenkins job is connected to this GitHub repo, just trigger the build!

The pipeline will:

1. Checkout the code
2. Fetch secrets from Secrets Manager
3. Build the Docker image (`hello-aws-secret`)
4. Scan the image using Trivy
5. Run the container with secrets injected as env variables

---

✅ No secrets are baked into the Docker image or stored in the repo.  
📂 Secrets are injected **at runtime**, keeping the build secure.

---
