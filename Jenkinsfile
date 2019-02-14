pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python:3-alpine' 
                }
            }
            steps {
                sh 'python -m py_compile app.py' 
                sh 'python -m compileall mercurius'
            }
        }
    }
}