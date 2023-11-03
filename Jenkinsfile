pipeline {
    agent any

    stages {
        stage('Clone Git Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def dockerImage = docker.build("my-docker-image:${BUILD_NUMBER}", "-f path/to/Dockerfile .")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://your-docker-registry', 'docker-credentials-id') {
                        dockerImage.push()
                    }
                }
            }
        }
    }
}
