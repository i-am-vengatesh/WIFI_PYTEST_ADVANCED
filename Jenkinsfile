pipeline {
    agent any

    stages {

        stage('Verify Environment') {
            steps {
                bat '''
                    "C:\\Users\\USER\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" --version
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    "C:\\Users\\USER\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m venv venv
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
                    venv\\Scripts\\python.exe -m pytest -v --html=reports\\wlan_test_report.html --self-contained-html --junitxml=reports\\junit-results.xml
                '''
            }
        }
    }

    post {
        always {
            junit 'reports/junit-results.xml'

            archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
        }
    }
}