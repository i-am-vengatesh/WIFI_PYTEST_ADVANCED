def runPython(String args) {
    bat "venv\\Scripts\\python.exe ${args}"
}
pipeline {
    agent any

    options {
    skipDefaultCheckout(true)
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

        stage('Clean Workspace') {
    steps {
        cleanWs()
    }
}

        stage('Checkout') {
    steps {
        checkout scm
    }
}

stage('Verify Kubernetes') {
    steps {
        bat '''
            echo ===== Jenkins Windows User =====
            whoami

            echo.
            echo ===== USERPROFILE =====
            echo %USERPROFILE%

            echo.
            echo ===== KUBECONFIG =====
            echo %KUBECONFIG%

            echo.
            echo ===== Kubernetes Client =====
            kubectl version --client

            echo.
            echo ===== Kubernetes Context =====
            kubectl config current-context

            echo.
            echo ===== Kubernetes Contexts =====
            kubectl config get-contexts

            echo.
            echo ===== Kubernetes Nodes =====
            kubectl get nodes
        '''
    }
}
stage('Build Docker Image') {
    steps {
        bat '''
            echo ===== Building Docker Image =====
            docker build -t wifi-pytest-advanced:%BUILD_NUMBER% .

            echo.
            echo ===== Docker Image =====
            docker images wifi-pytest-advanced
        '''
    }
}

stage('Load Docker Image into Kind') {
    steps {
        bat '''
            echo ===== Loading Image into Kind =====
            kind load docker-image wifi-pytest-advanced:%BUILD_NUMBER%

            echo.
            echo ===== Verify Image in Kind =====
            docker exec kind-control-plane crictl images | findstr wifi-pytest-advanced
        '''
    }
}

stage('Prepare Kubernetes Job') {
    steps {
        bat '''
            echo Preparing Kubernetes Job for Build %BUILD_NUMBER%

            powershell -Command "(Get-Content k8s\\wifi-pytest-job.yaml) -replace 'name: wifi-pytest-job', 'name: wifi-pytest-job-%BUILD_NUMBER%' -replace 'image: wifi-pytest-advanced:1.0', 'image: wifi-pytest-advanced:%BUILD_NUMBER%' | Set-Content k8s\\wifi-pytest-job-generated.yaml"

            echo Generated Kubernetes Job:
            type k8s\\wifi-pytest-job-generated.yaml
        '''
    }
}




        stage('Verify Environment') {
            steps {
                bat '''
                    echo Build Number: %BUILD_NUMBER%
                    echo Job Name: %JOB_NAME%
                    echo Git Commit: %GIT_COMMIT%
                    echo Git Branch: %GIT_BRANCH%
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
        script {
            runPython("--version")
            runPython("-m pytest --version")
        }
    }
}

        stage('Run Pytest') {
            steps {
                bat '''
                venv\\Scripts\\python.exe -m pytest -v -s ^
              --env=lab_a ^
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
            artifacts: 'reports/*.xml,reports/*.html,reports/*.log',
            fingerprint: true,
            allowEmptyArchive: true
        )

        cleanWs()
    }

    success {
        echo 'WLAN validation pipeline completed successfully.'
    }

    failure {
        echo 'WLAN validation pipeline failed. Review Jenkins test results and reports.'
    }
}
}