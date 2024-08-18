pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'your-dockerhub-username/game-library-app:latest'
        AWS_REGION = "us-east-1"   // Update with your AWS region
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    // No credentials needed for public repositories
                    git url: 'https://github.com/rs0fox/threetierappgamelib.git'
                }
            }
        }

        stage('Terraform Init') {
            environment {
                AWS_ACCESS_KEY_ID = credentials('aws').username
                AWS_SECRET_ACCESS_KEY = credentials('aws').password
            }
            steps {
                script {
                    dir('terraform') {
                        sh 'terraform init'
                    }
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                script {
                    dir('terraform') {
                        sh 'terraform plan'
                    }
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                script {
                    dir('terraform') {
                        sh 'terraform apply -auto-approve'
                    }
                }
            }
        }

        stage('Update kubeconfig') {
            steps {
                script {
                    sh "aws eks --region ${AWS_REGION} update-kubeconfig --name game-library-cluster"
                }
            }
        }

        stage('Build and Push Docker Image') {
            environment {
                DOCKER_USERNAME = credentials('jenkins-docker').username
                DOCKER_PASSWORD = credentials('jenkins-docker').password
            }
            steps {
                script {
                    sh '''
                        echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin
                        docker build -t ${DOCKER_IMAGE} .
                        docker tag ${DOCKER_IMAGE} ${DOCKER_IMAGE}
                        docker push ${DOCKER_IMAGE}
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh 'kubectl apply -f kubernetes/deployment.yaml'
                    sh 'kubectl apply -f kubernetes/service.yaml'
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    sh 'kubectl get pods'
                    sh 'kubectl get svc'
                }
            }
        }
    }
}
