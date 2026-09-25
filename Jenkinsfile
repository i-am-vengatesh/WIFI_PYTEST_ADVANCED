pipeline {
    agent any

    environment {
        KUBECONFIG = "C:\\Users\\USER\\.kube\\config"
        KIND_BIN   = "C:\\Users\\USER\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe\\kind.exe"
        IMAGE_NAME = "wifi-pytest-advanced"
        JOB_NAME   = "wifi-pytest-job-${BUILD_NUMBER}"
    }

    options {
        timeout(time: 15, unit: 'MINUTES')
        timestamps()
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

        stage('Verify Infrastructure') {
            steps {
                bat '''
                    @echo off
                    echo ===== Checking Kubernetes Context =====
                    kubectl config current-context
                    
                    echo ===== Applying PVC Manifest =====
                    if exist k8s\\pvc.yaml (
                        kubectl apply -f k8s\\pvc.yaml --validate=false --request-timeout=30s
                    )
                '''
            }
        }

        stage('Build & Load Container') {
            steps {
                bat """
                    @echo off
                    echo ===== Building Docker Image =====
                    set RETRY_COUNT=0
                    :build_loop
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    if errorlevel 1 (
                        set /a RETRY_COUNT+=1
                        if %RETRY_COUNT% LSS 3 (
                            echo WARNING: Docker build failed (network/DNS issue). Retrying in 10s... (%RETRY_COUNT%/3)
                            timeout /t 10 /nobreak
                            goto build_loop
                        ) else (
                            echo ERROR: Docker build failed after 3 attempts.
                            exit /b 1
                        )
                    )

                    echo ===== Loading Image into KinD Cluster =====
                    "${KIND_BIN}" load docker-image ${IMAGE_NAME}:${BUILD_NUMBER}
                """
            }
        }

        stage('Execute Pytest in Kubernetes') {
            steps {
                bat """
                    @echo off
                    echo ===== Verifying API Connectivity =====
                    kubectl version --request-timeout=15s
                    if errorlevel 1 (
                        echo WARNING: API server unresponsive. Waiting 10s...
                        timeout /t 10 /nobreak
                    )

                    echo ===== Cleaning Up Previous Jobs =====
                    kubectl delete job -l app=wifi-pytest --ignore-not-found=true --request-timeout=30s
                    kubectl delete job ${JOB_NAME} --ignore-not-found=true --request-timeout=30s
                    
                    echo ===== Generating Manifest for Build ${BUILD_NUMBER} =====
                    powershell -Command "(Get-Content k8s\\wifi-pytest-job.yaml) -replace 'name: wifi-pytest-job', 'name: ${JOB_NAME}' -replace 'image: wifi-pytest-advanced:1.0', 'image: ${IMAGE_NAME}:${BUILD_NUMBER}' | Set-Content k8s\\wifi-pytest-job-gen.yaml"
                    
                    echo ===== Applying Kubernetes Job =====
                    kubectl apply -f k8s\\wifi-pytest-job-gen.yaml --validate=false --request-timeout=30s
                    
                    echo ===== Waiting for Test Execution =====
                    kubectl wait --for=condition=complete job/${JOB_NAME} --timeout=5m
                    if errorlevel 1 (
                        echo ERROR: Job timed out or failed!
                        kubectl get pods
                        kubectl describe job ${JOB_NAME}
                        exit /b 1
                    )
                    
                    echo ===== Test Logs =====
                    kubectl logs job/${JOB_NAME}
                """
            }
        }

        stage('Extract Reports from PVC') {
            steps {
                bat '''
                    @echo off
                    echo ===== Extracting Reports via Helper Pod =====
                    if not exist reports mkdir reports

                    kubectl delete pod pvc-extractor --ignore-not-found=true --request-timeout=15s

                    echo ===== Starting Temporary Helper Pod =====
                    kubectl run pvc-extractor --image=alpine --restart=Never --overrides="{\\"spec\\":{\\"volumes\\":[{\\"name\\":\\"vol\\",\\"persistentVolumeClaim\\":{\\"claimName\\":\\"wifi-pytest-reports-pvc\\"}}],\\"containers\\":[{\\"name\\":\\"extractor\\",\\"image\\":\\"alpine\\",\\"command\\":[\\"sleep\\",\\"120\\"],\\"volumeMounts\\":[{\\"mountPath\\":\\"/app/reports\\",\\"name\\":\\"vol\\"}]}]}}"

                    echo ===== Waiting for Extractor Pod =====
                    kubectl wait --for=condition=Ready pod/pvc-extractor --timeout=60s

                    echo ===== Copying Entire Reports Directory =====
                    kubectl cp pvc-extractor:/app/reports/. ./reports/

                    echo ===== Cleaning Up Helper Pod =====
                    kubectl delete pod pvc-extractor --ignore-not-found=true

                    echo ===== Verifying Extracted Local Workspace Files =====
                    dir reports

                    if not exist reports\\wlan_test_report.html (
                        echo ^<html^>^<body^>^<h1^>No HTML Report Generated^</h1^>^</body^>^</html^> > reports\\wlan_test_report.html
                    )
                '''
            }
        }

        stage('Cleanup Docker Storage') {
            steps {
                bat '''
                    docker container prune -f
                    docker image prune -f --filter "until=48h"
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline run completed for Build #${BUILD_NUMBER}."
        }
        success {
            echo "Publishing test results..."
            
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'wlan_test_report.html',
                reportName: 'PytestWLANReport',
                reportTitles: 'WLAN Test Automation Execution'
            ])

            junit allowEmptyResults: true, testResults: 'reports/*.xml'
        }
        failure {
            echo "Build #${BUILD_NUMBER} failed. Check Kubernetes pod logs or pipeline execution output."
        }
    }
}