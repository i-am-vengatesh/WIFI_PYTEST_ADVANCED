pipeline {

    agent any

    options {
        timestamps()

        // Prevent a Git/network problem from occupying Jenkins forever
        timeout(time: 60, unit: 'MINUTES')

        // Keep only one pipeline execution at a time
        disableConcurrentBuilds()

        // Clean workspace before starting
        skipDefaultCheckout(true)
    }

    stage('Verify Environment') {

    steps {

        echo ''
        echo '=========================================='
        echo 'Verify Environment'
        echo '=========================================='

        bat '''
            @echo off

            echo.
            echo ===== Docker Version =====
            docker --version

            echo.
            echo ===== Kind Version =====
            "%KIND_EXE%" version

            if errorlevel 1 (
                echo.
                echo ERROR: Kind executable could not be executed.
                echo KIND_EXE=%KIND_EXE%
                exit /b 1
            )

            echo.
            echo ===== Kubectl Version =====
            kubectl version --client

            if errorlevel 1 (
                echo.
                echo ERROR: kubectl is not available.
                exit /b 1
            )

            echo.
            echo ===== Kubernetes Context =====
            kubectl config current-context

            echo.
            echo ===== Kubernetes Nodes =====
            kubectl get nodes

            if errorlevel 1 (
                echo.
                echo ERROR: Kubernetes cluster is not accessible.
                exit /b 1
            )

            echo.
            echo ===== Docker Info =====
            docker info

            if errorlevel 1 (
                echo.
                echo ERROR: Docker is not accessible.
                exit /b 1
            )

            echo.
            echo ==========================================
            echo Environment Verification Successful
            echo ==========================================
        '''
    }
}


    stages {


        // ============================================================
        // 1. CHECKOUT APPLICATION SOURCE
        // ============================================================
        stage('Checkout Source') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Checkout WIFI_PYTEST_ADVANCED'
                echo '=========================================='

                checkout scm

                bat '''
                    @echo off

                    echo.
                    echo ===== Git Version =====
                    git --version

                    echo.
                    echo ===== Current Commit =====
                    git rev-parse HEAD

                    echo.
                    echo ===== Current Branch =====
                    git branch --show-current
                '''
            }
        }


        // ============================================================
        // 2. VERIFY ENVIRONMENT
        // ============================================================
        stage('Verify Environment') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Verify Environment'
                echo '=========================================='

                bat '''
                    @echo off

                    echo.
                    echo ===== Docker Version =====
                    docker --version

                    echo.
                    echo ===== Kind Version =====
                    "%KIND_EXE%" version

                    echo.
                    echo ===== Kubectl Version =====
                    kubectl version --client

                    echo.
                    echo ===== Docker Info =====
                    docker info

                    echo.
                    echo ===== Kubernetes Context =====
                    kubectl config current-context

                    echo.
                    echo ===== Kubernetes Nodes =====
                    kubectl get nodes

                    echo.
                    echo ===== Python Version =====
                    python --version
                '''
            }
        }


        // ============================================================
        // 3. BUILD DOCKER IMAGE
        // ============================================================
        stage('Build Docker Image') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Build Docker Image'
                echo '=========================================='

                bat '''
                    @echo off

                    echo.
                    echo ===== Building Docker Image =====

                    docker build ^
                        -t %DOCKER_IMAGE%:%BUILD_NUMBER% ^
                        .

                    if errorlevel 1 (
                        echo Docker build failed.
                        exit /b 1
                    )

                    echo.
                    echo ===== Docker Image Created =====

                    docker images %DOCKER_IMAGE%
                '''
            }
        }


        // ============================================================
        // 4. GITOPS - CLONE REPOSITORY
        // ============================================================
        stage('Clone GitOps Repository') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Clone GitOps Repository'
                echo '=========================================='

                dir('gitops-repo') {

                    deleteDir()

                    withCredentials([
                        gitUsernamePassword(
                            credentialsId: "${GITOPS_CREDENTIALS}",
                            gitToolName: 'git'
                        )
                    ]) {

                        bat '''
                            @echo off

                            echo.
                            echo ===== Cloning GitOps Repository =====

                            git clone "%GITOPS_REPO%" .

                            if errorlevel 1 (
                                echo GitOps repository clone failed.
                                exit /b 1
                            )

                            echo.
                            echo ===== GitOps Repository =====

                            git remote -v

                            echo.
                            echo ===== Git Branch =====

                            git branch -a
                        '''
                    }
                }
            }
        }


        // ============================================================
        // 5. VERIFY GITHUB CONNECTION
        // ============================================================
        stage('Verify GitOps Repository') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Verify GitOps Repository'
                echo '=========================================='

                dir('gitops-repo') {

                    withCredentials([
                        gitUsernamePassword(
                            credentialsId: "${GITOPS_CREDENTIALS}",
                            gitToolName: 'git'
                        )
                    ]) {

                        bat '''
                            @echo off

                            echo.
                            echo ===== Git Remote =====

                            git remote -v

                            echo.
                            echo ===== Local Commit =====

                            git rev-parse HEAD

                            echo.
                            echo ===== Remote Main =====

                            git ls-remote origin refs/heads/main

                            if errorlevel 1 (
                                echo.
                                echo GitHub connectivity/authentication failed.
                                exit /b 1
                            )

                            echo.
                            echo ==========================================
                            echo GitHub Connectivity Successful
                            echo ==========================================
                        '''
                    }
                }
            }
        }


        // ============================================================
        // 6. UPDATE GITOPS MANIFEST
        // ============================================================
        stage('Update GitOps Manifest') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Update GitOps Manifest'
                echo '=========================================='

                dir('gitops-repo') {

                    bat '''
                        @echo off

                        echo.
                        echo ===== BEFORE UPDATE =====

                        findstr /I "image:" "%GITOPS_MANIFEST%"

                        echo.
                        echo ===== Updating Image =====

                        powershell -NoProfile -ExecutionPolicy Bypass -Command ^
                        "(Get-Content '%GITOPS_MANIFEST%') -replace 'image: wifi-pytest-advanced:[^ ]+', 'image: wifi-pytest-advanced:%BUILD_NUMBER%' | Set-Content '%GITOPS_MANIFEST%'"

                        if errorlevel 1 (
                            echo Failed to update Kubernetes manifest.
                            exit /b 1
                        )

                        echo.
                        echo ===== AFTER UPDATE =====

                        findstr /I "image:" "%GITOPS_MANIFEST%"

                        echo.
                        echo ===== Git Diff =====

                        git diff -- "%GITOPS_MANIFEST%"
                    '''
                }
            }
        }


        // ============================================================
        // 7. COMMIT GITOPS CHANGE
        // ============================================================
        stage('Commit GitOps Changes') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Commit GitOps Changes'
                echo '=========================================='

                dir('gitops-repo') {

                    bat '''
                        @echo off

                        git config user.name "Jenkins CI"
                        git config user.email "jenkins@localhost"

                        echo.
                        echo ===== Git Status =====

                        git status

                        echo.
                        echo ===== Git Add =====

                        git add "%GITOPS_MANIFEST%"

                        echo.
                        echo ===== Git Commit =====

                        git commit -m "Update Pytest image to build %BUILD_NUMBER%"

                        if errorlevel 1 (
                            echo.
                            echo No changes to commit or commit failed.
                            exit /b 1
                        )

                        echo.
                        echo ===== New Commit =====

                        git log -1 --oneline
                    '''
                }
            }
        }


        // ============================================================
        // 8. PUSH GITOPS CHANGE
        // ============================================================
        stage('Push GitOps Changes') {

            options {
                timeout(time: 3, unit: 'MINUTES')
            }

            steps {

                echo ''
                echo '=========================================='
                echo 'Pushing GitOps Changes'
                echo '=========================================='

                dir('gitops-repo') {

                    withCredentials([
                        gitUsernamePassword(
                            credentialsId: "${GITOPS_CREDENTIALS}",
                            gitToolName: 'git'
                        )
                    ]) {

                        bat '''
                            @echo off

                            echo.
                            echo ===== Git Remote =====

                            git remote -v

                            echo.
                            echo ===== Local Commit =====

                            git log -1 --oneline

                            echo.
                            echo ===== Pushing GitOps Changes =====

                            set GIT_TERMINAL_PROMPT=0

                            git push origin HEAD:main

                            if errorlevel 1 (
                                echo.
                                echo ==========================================
                                echo Git Push FAILED
                                echo ==========================================
                                exit /b 1
                            )

                            echo.
                            echo ==========================================
                            echo Git Push Successful
                            echo ==========================================
                        '''
                    }
                }
            }
        }


        // ============================================================
        // 9. LOAD DOCKER IMAGE INTO KIND
        // ============================================================
        stage('Load Docker Image into Kind') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Load Docker Image into Kind'
                echo '=========================================='

                bat '''
                    @echo off

                    echo.
                    echo ===== Loading Image =====

                    "%KIND_EXE%" load docker-image ^
                        %DOCKER_IMAGE%:%BUILD_NUMBER% ^
                        --name %KIND_CLUSTER%

                    if errorlevel 1 (
                        echo Failed to load Docker image into Kind.
                        exit /b 1
                    )

                    echo.
                    echo ===== Verify Image Inside Kind =====

                    docker exec %KIND_CLUSTER%-control-plane ^
                        crictl images
                '''
            }
        }


        // ============================================================
        // 10. PREPARE KUBERNETES JOB
        // ============================================================
        stage('Prepare Kubernetes Job') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Prepare Kubernetes Job'
                echo '=========================================='

                bat '''
                    @echo off

                    echo.
                    echo ===== Creating Reports Directory =====

                    if not exist reports\\k8s (
                        mkdir reports\\k8s
                    )

                    echo.
                    echo ===== Generate Kubernetes Job =====

                    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
                    "$content = Get-Content 'k8s\\wifi-pytest-job.yaml' -Raw; ^
                    $content = $content -replace 'name: wifi-pytest-job', 'name: wifi-pytest-job-%BUILD_NUMBER%'; ^
                    $content = $content -replace 'image: wifi-pytest-advanced:[^ ]+', 'image: wifi-pytest-advanced:%BUILD_NUMBER%'; ^
                    $content | Set-Content 'k8s\\wifi-pytest-job-generated.yaml'"

                    if errorlevel 1 (
                        echo Failed to generate Kubernetes Job YAML.
                        exit /b 1
                    )

                    echo.
                    echo ===== Generated Job =====

                    type k8s\\wifi-pytest-job-generated.yaml
                '''
            }
        }


        // ============================================================
        // 11. RUN PYTEST IN KUBERNETES
        // ============================================================
        stage('Run Pytest in Kubernetes') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Run Pytest in Kubernetes'
                echo '=========================================='

                bat '''
                    @echo off

                    echo.
                    echo ===== Applying Kubernetes Job =====

                    kubectl apply -f k8s\\wifi-pytest-job-generated.yaml

                    if errorlevel 1 (
                        echo Failed to create Kubernetes Job.
                        exit /b 1
                    )

                    echo.
                    echo ===== Waiting for Job =====

                    kubectl wait ^
                        --for=condition=complete ^
                        job/wifi-pytest-job-%BUILD_NUMBER% ^
                        --timeout=10m

                    if errorlevel 1 (
                        echo.
                        echo Kubernetes Job did not complete successfully.

                        echo.
                        echo ===== Job Status =====
                        kubectl get job wifi-pytest-job-%BUILD_NUMBER%

                        echo.
                        echo ===== Pod Status =====
                        kubectl get pods -l job-name=wifi-pytest-job-%BUILD_NUMBER%

                        echo.
                        echo ===== Job Logs =====
                        kubectl logs job/wifi-pytest-job-%BUILD_NUMBER%

                        exit /b 1
                    )

                    echo.
                    echo ===== Kubernetes Job Completed =====

                    kubectl get job wifi-pytest-job-%BUILD_NUMBER%

                    echo.
                    echo ===== Pytest Logs =====

                    kubectl logs job/wifi-pytest-job-%BUILD_NUMBER%
                '''
            }
        }


        // ============================================================
        // 12. CREATE REPORTS READER POD
        // ============================================================
        stage('Create Reports Reader') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Create Reports Reader Pod'
                echo '=========================================='

                bat '''
                    @echo off

                    echo.
                    echo ===== Creating Reports Reader =====

                    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
                    "$content = Get-Content 'k8s\\reports-reader.yaml' -Raw; ^
                    $content = $content -replace 'name: reports-reader', 'name: reports-reader-%BUILD_NUMBER%'; ^
                    $content | Set-Content 'k8s\\reports-reader-generated.yaml'"

                    kubectl apply -f k8s\\reports-reader-generated.yaml

                    if errorlevel 1 (
                        echo Failed to create reports reader.
                        exit /b 1
                    )

                    echo.
                    echo ===== Waiting for Reports Reader =====

                    kubectl wait ^
                        --for=condition=Ready ^
                        pod/reports-reader-%BUILD_NUMBER% ^
                        --timeout=2m

                    if errorlevel 1 (
                        echo Reports reader did not become ready.
                        kubectl get pod reports-reader-%BUILD_NUMBER%
                        kubectl describe pod reports-reader-%BUILD_NUMBER%
                        exit /b 1
                    )

                    echo.
                    echo ===== Reports Reader Ready =====

                    kubectl get pod reports-reader-%BUILD_NUMBER%
                '''
            }
        }


        // ============================================================
        // 13. COLLECT KUBERNETES REPORTS
        // ============================================================
        stage('Collect Kubernetes Reports') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Collect Kubernetes Reports'
                echo '=========================================='

                bat '''
                    @echo off

                    echo.
                    echo ===== Creating Local Report Directory =====

                    if not exist reports\\k8s (
                        mkdir reports\\k8s
                    )

                    echo.
                    echo ===== Copying JUnit XML =====

                    kubectl cp ^
                        reports-reader-%BUILD_NUMBER%:/app/reports/junit-results.xml ^
                        reports\\k8s\\junit-results-k8s.xml

                    if errorlevel 1 (
                        echo Failed to copy JUnit XML.
                        exit /b 1
                    )

                    echo.
                    echo ===== Copying HTML Report =====

                    kubectl cp ^
                        reports-reader-%BUILD_NUMBER%:/app/reports/wlan_test_report.html ^
                        reports\\k8s\\wlan_test_report-k8s.html

                    if errorlevel 1 (
                        echo Failed to copy HTML report.
                        exit /b 1
                    )

                    echo.
                    echo ===== Reports Collected =====

                    dir reports\\k8s
                '''
            }
        }


        // ============================================================
        // 14. VERIFY REPORTS
        // ============================================================
        stage('Verify Reports') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Verify Reports'
                echo '=========================================='

                bat '''
                    @echo off

                    echo.
                    echo ===== JUnit XML =====

                    if not exist "%JUNIT_REPORT%" (
                        echo JUnit report not found.
                        exit /b 1
                    )

                    dir "%JUNIT_REPORT%"

                    echo.
                    echo ===== HTML Report =====

                    if not exist "%HTML_REPORT%" (
                        echo HTML report not found.
                        exit /b 1
                    )

                    dir "%HTML_REPORT%"

                    echo.
                    echo ===== Reports Verified Successfully =====
                '''

                junit 'reports/k8s/junit-results-k8s.xml'
            }
        }
    }


    // ================================================================
    // POST ACTIONS
    // ================================================================
    post {

        always {

            echo ''
            echo '=========================================='
            echo 'Pipeline Post Actions'
            echo '=========================================='

            script {

                if (fileExists('reports/k8s/junit-results-k8s.xml')) {

                    echo 'JUnit report available.'

                } else {

                    echo 'JUnit report not available.'
                }
            }

            archiveArtifacts(
                artifacts: 'reports/k8s/**/*',
                allowEmptyArchive: true,
                fingerprint: true
            )
        }


        success {

            echo ''
            echo '=========================================='
            echo 'PIPELINE SUCCESS'
            echo '=========================================='

            echo ''
            echo 'Build Number: %BUILD_NUMBER%'
            echo 'Docker Image: %DOCKER_IMAGE%:%BUILD_NUMBER%'
            echo 'Kubernetes Job: %K8S_JOB_BASE%-%BUILD_NUMBER%'
            echo ''
            echo 'GitOps repository updated.'
            echo 'Argo CD should reconcile the new Git state.'
            echo ''
        }


        failure {

            echo ''
            echo '=========================================='
            echo 'PIPELINE FAILED'
            echo '=========================================='

            echo ''
            echo 'Build Number: %BUILD_NUMBER%'
            echo 'Check the failed stage above.'
            echo ''
        }


        aborted {

            echo ''
            echo '=========================================='
            echo 'PIPELINE ABORTED'
            echo '=========================================='
        }


        cleanup {

            echo ''
            echo '=========================================='
            echo 'Cleanup'
            echo '=========================================='

            script {

                bat '''
                    @echo off

                    echo.
                    echo ===== Kubernetes Objects =====

                    kubectl get jobs -o wide 2>nul

                    echo.
                    echo ===== Kubernetes Pods =====

                    kubectl get pods -o wide 2>nul

                    echo.
                    echo ===== Workspace Cleanup =====
                '''

                deleteDir()
            }
        }
    }
}