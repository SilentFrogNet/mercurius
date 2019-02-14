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
		stage('Test') {
            agent {
                docker {
                    image 'python:3.6'  //only version 2.7 of python -> 'qnib/pytest'
                }
            }
            steps {
                sh 'jenkins/run_tests.sh'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                    recordIssues enabledForFailure: true, tool: pyLint(pattern: 'test-reports/pylint.out')
                    step([
                        $class: 'CoberturaPublisher', 
                        autoUpdateHealth: false, 
                        autoUpdateStability: false, 
                        coberturaReportFile: '**/test-reports/coverage.xml', 
                        failUnhealthy: false, 
                        failUnstable: false, 
                        maxNumberOfBuilds: 0, 
                        onlyStable: false, 
                        sourceEncoding: 'ASCII', 
                        zoomCoverageChart: false
                    ])
                }
            }
        }
        // stage('Deliver') { 
        //     agent {
        //         docker {
        //             image 'cdrx/pyinstaller-linux:python3' 
        //         }
        //     }
        //     steps {
        //         sh 'pyinstaller --onefile --noconfirm --name mercurius app.py' 
        //     }
        //     post {
        //         success {
        //             archiveArtifacts 'dist/mercurius' 
        //         }
        //     }
        // }
    }
}