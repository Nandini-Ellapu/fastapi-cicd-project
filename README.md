# 🚀 FastAPI CI/CD Pipeline Using Docker, Docker Hub, GitHub Actions & AWS EC2

This repository contains a complete end-to-end **CI/CD Pipeline** for deploying a FastAPI application using:

- Docker  
- Docker Hub  
- GitHub Actions  
- AWS EC2  
- SSH automation  

Full documentation is included in this repository as a PDF:
📄 **FastAPI CICD Pipeline.pdf**

---

## 📌 Project Overview

This project automates:

1. Packaging FastAPI app inside Docker  
2. Pushing the image to Docker Hub  
3. Automatically deploying on AWS EC2 using GitHub Actions  

---
## 📁 Project Structure
fastapi-cicd-project/
├── app/
│ ├── main.py
│ ├── requirements.txt
│ └── Dockerfile
├── .github/
│ └── workflows/
│ └── deploy.yml
└── FastAPI CICD Pipeline.pdf

---

## 🧩 FastAPI Application

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def index():
    return {"message": "FastAPI CI/CD working successfully!"}

🐳 Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
---
⚙️ GitHub Actions Workflow (deploy.yml)
name: CI/CD Pipeline

on:
  push:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Build Docker image
      run: docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/fastapi-cicd:latest ./app

    - name: Push Docker image
      run: docker push ${{ secrets.DOCKERHUB_USERNAME }}/fastapi-cicd:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest

    steps:
    - name: Deploy to EC2
      uses: appleboy/ssh-action@v1.0.0
      with:
        host: ${{ secrets.SSH_HOST }}
        username: ${{ secrets.SSH_USER }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          sudo docker pull ${{ secrets.DOCKERHUB_USERNAME }}/fastapi-cicd:latest
          sudo docker stop fastapi-app || true
          sudo docker rm fastapi-app || true
          sudo docker run -d --name fastapi-app -p 8000:8000 \
            ${{ secrets.DOCKERHUB_USERNAME }}/fastapi-cicd:latest
---
🔑 GitHub Secrets Used
| Secret Name          | Description                            |
| -------------------- | -------------------------------------- |
| `DOCKERHUB_USERNAME` | Docker Hub username                    |
| `DOCKERHUB_TOKEN`    | Docker Hub access token                |
| `SSH_HOST`           | EC2 Public IP                          |
| `SSH_USER`           | `ubuntu`                               |
| `SSH_PRIVATE_KEY`    | EC2 private key used by GitHub Actions |
---
🖥 AWS EC2 Setup
Run these on EC2:
sudo apt update
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker
sudo ufw allow 8000
---
🔐 SSH Key for Deployment
ssh-keygen -t ed25519 -f ~/.ssh/github_key -C "github-actions"
cat ~/.ssh/github_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/github_key
chmod 700 ~/.ssh
Add private key to GitHub Secrets.
---
🌍 Access Your Application
Once deployed, open: http://<EC2_PUBLIC_IP>:8000
Expected output:
{"message": "FastAPI CI/CD working successfully!"}
---
📄 Documentation
Full step-by-step documentation:
📌 FastAPI CICD Pipeline.pdf

👩‍💻 Author
Nandini Ellapu
DevOps | Docker | AWS | GitHub Actions | CI/CD




