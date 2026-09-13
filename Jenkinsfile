pipeline {
    agent any

    stages {

        stage('Verify Environment') {
            steps {
                bat '''
                    "D:\\vengatesh\\Python\\Pytest\\Projects\\WIFI_PYTEST_ADVANCED\\venv\\Scripts\\python.exe" --version
                '''
            }
        }

        stage('Run Pytest') {
            steps {
                bat '''
                    cd /d D:\\vengatesh\\Python\\Pytest\\Projects\\WIFI_PYTEST_ADVANCED

                    "D:\\vengatesh\\Python\\Pytest\\Projects\\WIFI_PYTEST_ADVANCED\\venv\\Scripts\\python.exe" -m pytest -v --html=reports/wlan_test_report.html --self-contained-html
                '''
            }
        }

        stage('Copy Report') {
            steps {
                bat '''
                    if not exist reports mkdir reports

                    copy /Y "D:\\vengatesh\\Python\\Pytest\\Projects\\WIFI_PYTEST_ADVANCED\\reports\\wlan_test_report.html" "%WORKSPACE%\\reports\\wlan_test_report.html"
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