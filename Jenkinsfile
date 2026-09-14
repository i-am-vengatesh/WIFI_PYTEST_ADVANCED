pipeline {
    agent any

    options {
    timestamps()
    timeout(time: 30, unit: 'MINUTES')
    disableConcurrentBuilds()
}
environment {
    PYTHON = 'C:\\Users\\USER\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'
    HTML_REPORT = 'reports\\wlan_test_report.html'
    JUNIT_REPORT = 'reports\\junit-results.xml'
}

    stages {

        stage('Verify Environment') {
            steps {
                bat '''
                    "%PYTHON%" --version
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    "%PYTHON%" -m venv venv
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

        stage('Validate Test Environment') {
    steps {
        bat '''
            venv\\Scripts\\python.exe --version
            venv\\Scripts\\python.exe -m pytest --version
        '''
    }
}

        stage('Run Pytest') {
            steps {
                bat '''
                    venv\\Scripts\\python.exe -m pytest -v ^
              --html=%HTML_REPORT% ^
              --self-contained-html ^
              --junitxml=%JUNIT_REPORT%
                '''
            }
        }
    }

    post {
    always {
        junit 'reports/junit-results.xml'

        archiveArtifacts(
            artifacts: 'reports/*.html,reports/*.log',
            fingerprint: true,
            allowEmptyArchive: true
        )
    }

    success {
        echo 'WLAN validation pipeline completed successfully.'
    }

    failure {
        echo 'WLAN validation pipeline failed. Review Jenkins test results and reports.'
    }
}
}