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
        KIND = 'C:\\Users\\USER\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe\\kind.exe'

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
                    echo ===== Kind Executable =====
                    "%KIND%" version

                    echo.
                    echo ===== Loading Image into Kind =====
                    "%KIND%" load docker-image wifi-pytest-advanced:%BUILD_NUMBER%

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

                    echo.
                    echo ===== Generated Kubernetes Job =====
                    type k8s\\wifi-pytest-job-generated.yaml
                '''
            }
        }

        stage('Run Pytest in Kubernetes') {
            steps {
                bat '''
                    echo ===== Applying Kubernetes Job =====
                    kubectl apply -f k8s\\wifi-pytest-job-generated.yaml

                    echo.
                    echo ===== Kubernetes Job =====
                    kubectl get job wifi-pytest-job-%BUILD_NUMBER%

                    echo.
                    echo ===== Waiting for Job Completion =====
                    kubectl wait --for=condition=complete job/wifi-pytest-job-%BUILD_NUMBER% --timeout=5m

                    echo.
                    echo ===== Job Status =====
                    kubectl get job wifi-pytest-job-%BUILD_NUMBER%

                    echo.
                    echo ===== Pod Status =====
                    kubectl get pods -l job-name=wifi-pytest-job-%BUILD_NUMBER%

                    echo.
                    echo ===== Pytest Logs =====
                    kubectl logs job/wifi-pytest-job-%BUILD_NUMBER%
                '''
            }
        }

        stage('Collect Kubernetes Reports') {
    steps {
        bat '''
            echo ===== Creating Report Reader Pod =====

            powershell -Command "(Get-Content k8s\\reports-reader.yaml) -replace 'name: reports-reader', 'name: reports-reader-%BUILD_NUMBER%' | Set-Content k8s\\reports-reader-generated.yaml"

            kubectl apply -f k8s\\reports-reader-generated.yaml

            echo.
            echo ===== Waiting for Reader Pod =====
            kubectl wait --for=condition=Ready pod/reports-reader-%BUILD_NUMBER% --timeout=60s

            echo.
            echo ===== Creating Jenkins Report Directory =====
            if not exist reports\\k8s mkdir reports\\k8s

            echo.
            echo ===== Copying Kubernetes JUnit Report =====
            kubectl cp reports-reader-%BUILD_NUMBER%:/app/reports/junit-results.xml reports\\k8s\\junit-results-k8s.xml

            echo.
            echo ===== Copying Kubernetes HTML Report =====
            kubectl cp reports-reader-%BUILD_NUMBER%:/app/reports/wlan_test_report.html reports\\k8s\\wlan_test_report-k8s.html

            echo.
            echo ===== Kubernetes Reports Retrieved =====
            dir reports\\k8s

            echo.
            echo ===== Deleting Temporary Reader Pod =====
            kubectl delete pod reports-reader-%BUILD_NUMBER% --ignore-not-found
        '''
    }
}
    }

    post {
        always {
            junit 'reports/k8s/junit-results-k8s.xml'

            archiveArtifacts(
                artifacts: 'reports/k8s/*.xml,reports/k8s/*.html,reports/*.log',
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