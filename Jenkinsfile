pipeline {
    agent any

    stages {

        stage('Verify Environment') {
            steps {
                bat '''
                    python --version
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    python -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pytest') {
            steps {
                bat '''
                    venv\\Scripts\\python.exe -m pytest -v --html=reports\\wlan_test_report.html --self-contained-html
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
        }
    }
}