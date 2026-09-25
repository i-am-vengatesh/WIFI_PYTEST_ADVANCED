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
                    kubectl config current-context
                    if exist k8s\\pvc.yaml (
                        kubectl apply -f k8s\\pvc.yaml
                    )
                '''
            }
        }

        stage('Build & Load Container') {
            steps {
                bat """
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    "${KIND_BIN}" load docker-image ${IMAGE_NAME}:${BUILD_NUMBER}
                """
            }
        }

        stage('Execute Pytest in Kubernetes') {
            steps {
                bat """
                    @echo off
                    echo ===== Cleaning Up Previous Kubernetes Jobs =====
                    kubectl delete job ${JOB_NAME} --ignore-not-found=true
                    
                    echo ===== Generating Manifest for Build ${BUILD_NUMBER} =====
                    powershell -Command "(Get-Content k8s\\wifi-pytest-job.yaml) -replace 'name: wifi-pytest-job', 'name: ${JOB_NAME}' -replace 'image: wifi-pytest-advanced:1.0', 'image: ${IMAGE_NAME}:${BUILD_NUMBER}' | Set-Content k8s\\wifi-pytest-job-gen.yaml"
                    
                    echo ===== Applying Kubernetes Job =====
                    kubectl apply -f k8s\\wifi-pytest-job-gen.yaml
                    
                    echo ===== Waiting for Test Execution =====
                    kubectl wait --for=condition=complete job/${JOB_NAME} --timeout=5m
                    
                    echo ===== Test Logs =====
                    kubectl logs job/${JOB_NAME}
                """
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
    }
}