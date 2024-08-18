pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'your-dockerhub-username/game-library-app:latest'
        DOCKER_CREDENTIALS_ID = 'docker-credentials'  // The ID of your Docker credentials in Jenkins
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                        docker build -t ${DOCKER_IMAGE} .
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                            echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin
                            docker push ${DOCKER_IMAGE}
                        '''
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh '''
                        kubectl apply -f kubernetes/deployment.yaml
                        kubectl apply -f kubernetes/service.yaml
                    '''
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
