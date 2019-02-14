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
                sh 'jenkins/setup_env.sh'
                sh 'python -m py_compile app.py' 
                sh 'python -m compileall mercurius'
            }
        }
		stage('Test') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'py.test --verbose --junit-xml test-reports/results.xml mercurius/tests'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}