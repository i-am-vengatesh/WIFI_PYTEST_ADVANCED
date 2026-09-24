pipeline {

    agent any

    options {
        timestamps()
        timeout(time: 60, unit: 'MINUTES')
    }

    environment {

        // ============================================================
        // Main Project
        // ============================================================
        DOCKER_IMAGE = 'wifi-pytest-advanced'

        // ============================================================
        // Kind
        // ============================================================
        KIND_EXE = 'C:\\Users\\USER\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe\\kind.exe'

        // ============================================================
        // Kubernetes
        // ============================================================
        K8S_JOB_BASE = 'wifi-pytest-job'
        K8S_NAMESPACE = 'default'

        // ============================================================
        // GitOps Repository
        // ============================================================
        GITOPS_REPO = 'https://github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git'
        GITOPS_BRANCH = 'main'
        GITOPS_DIR = 'gitops-repo'
        GITOPS_MANIFEST = 'k8s\\pytest-job.yaml'

        // Jenkins credential containing:
        // Username = GitHub username
        // Password = GitHub Personal Access Token
        GITOPS_CREDENTIALS = 'github-gitops-creds'
    }

    stages {

        // ============================================================
        // 1. CHECKOUT SOURCE
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

                    if errorlevel 1 (
                        echo.
                        echo ERROR: Docker is not available.
                        exit /b 1
                    )

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

                    if errorlevel 1 (
                        echo.
                        echo ERROR: Kubernetes context is not available.
                        exit /b 1
                    )

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
                        -t %DOCKER_IMAGE%:%BUILD_NUMBER% .

                    if errorlevel 1 (
                        echo.
                        echo ERROR: Docker image build failed.
                        exit /b 1
                    )

                    echo.
                    echo ===== Docker Image Created =====

                    docker images %DOCKER_IMAGE%
                '''
            }
        }


        // ============================================================
        // 4. CLONE GITOPS REPOSITORY
        // ============================================================
        stage('Clone GitOps Repository') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Clone GitOps Repository'
                echo '=========================================='

                dir("${GITOPS_DIR}") {

                    deleteDir()

                    withCredentials([
                        usernamePassword(
                            credentialsId: "${GITOPS_CREDENTIALS}",
                            usernameVariable: 'GIT_USERNAME',
                            passwordVariable: 'GIT_PASSWORD'
                        )
                    ]) {

                        bat '''
                            @echo off

                            echo.
                            echo ===== Cloning GitOps Repository =====

                            git clone ^
                                --branch %GITOPS_BRANCH% ^
                                %GITOPS_REPO% .

                            if errorlevel 1 (
                                echo.
                                echo ERROR: GitOps repository clone failed.
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
        // 5. VERIFY GITOPS REPOSITORY
        // ============================================================
        stage('Verify GitOps Repository') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Verify GitOps Repository'
                echo '=========================================='

                dir("${GITOPS_DIR}") {

                    withCredentials([
                        usernamePassword(
                            credentialsId: "${GITOPS_CREDENTIALS}",
                            usernameVariable: 'GIT_USERNAME',
                            passwordVariable: 'GIT_PASSWORD'
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
                                echo ERROR: GitHub connectivity check failed.
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

                dir("${GITOPS_DIR}") {

                    bat '''
                        @echo off

                        echo.
                        echo ===== BEFORE UPDATE =====

                        findstr /n /i "image:" "%GITOPS_MANIFEST%"

                        echo.
                        echo ===== Updating Image =====

                        powershell -NoProfile -ExecutionPolicy Bypass -Command ^
                        "$file = '%GITOPS_MANIFEST%';" ^
                        "$content = Get-Content -Raw $file;" ^
                        "$newImage = 'vengateshbabu1605/wifi-pytest-advanced:%BUILD_NUMBER%';" ^
                        "$updated = [regex]::Replace($content, 'image:\\s*vengateshbabu1605/wifi-pytest-advanced:\\S+', 'image: ' + $newImage);" ^
                        "if ($updated -eq $content) { Write-Host 'ERROR: Docker image reference was not found in manifest.'; exit 1 };" ^
                        "Set-Content -Path $file -Value $updated -NoNewline;"

                        if errorlevel 1 (
                            echo.
                            echo ERROR: GitOps manifest update failed.
                            exit /b 1
                        )

                        echo.
                        echo ===== AFTER UPDATE =====

                        findstr /n /i "image:" "%GITOPS_MANIFEST%"

                        echo.
                        echo ===== Git Diff =====

                        git diff -- "%GITOPS_MANIFEST%"

                        echo.
                        echo ===== Verify Image Tag =====

                        findstr /i "vengateshbabu1605/wifi-pytest-advanced:%BUILD_NUMBER%" "%GITOPS_MANIFEST%"

                        if errorlevel 1 (
                            echo.
                            echo ERROR: Expected image tag was not found.
                            exit /b 1
                        )
                    '''
                }
            }
        }


        // ============================================================
        // 7. COMMIT GITOPS CHANGES
        // ============================================================
        stage('Commit GitOps Changes') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Commit GitOps Changes'
                echo '=========================================='

                dir("${GITOPS_DIR}") {

                    bat '''
                        @echo off

                        echo.
                        echo ===== Git Status =====

                        git status

                        echo.
                        echo ===== Git Add =====

                        git add "%GITOPS_MANIFEST%"

                        if errorlevel 1 (
                            echo ERROR: Git add failed.
                            exit /b 1
                        )

                        echo.
                        echo ===== Git Commit =====

                        git commit ^
                            -m "Update Pytest image to build %BUILD_NUMBER%"

                        if errorlevel 1 (
                            echo.
                            echo ERROR: Git commit failed.
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
        // 8. PUSH GITOPS CHANGES
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

        dir("${GITOPS_DIR}") {

            withCredentials([
                usernamePassword(
                    credentialsId: "${GITOPS_CREDENTIALS}",
                    usernameVariable: 'GIT_USERNAME',
                    passwordVariable: 'GIT_PASSWORD'
                )
            ]) {

                bat '''
                    @echo off
                    setlocal EnableExtensions

                    echo.
                    echo ===== Git Remote =====
                    git remote -v

                    echo.
                    echo ===== Local Commit =====
                    git log -1 --oneline

                    echo.
                    echo ===== Preparing GitHub Authentication =====

                    set "GIT_TERMINAL_PROMPT=0"
                    set "GIT_ASKPASS=%CD%\\git-askpass.bat"

                    (
                        echo @echo off
                        echo if /I "%%~1"=="Password for 'https://github.com':" goto PASSWORD
                        echo if /I "%%~1"=="Password for 'https://%%GIT_USERNAME%%@github.com':" goto PASSWORD
                        echo echo %%GIT_USERNAME%%
                        echo exit /b 0
                        echo :PASSWORD
                        echo echo %%GIT_PASSWORD%%
                        echo exit /b 0
                    ) > "%GIT_ASKPASS%"

                    echo.
                    echo ===== GitHub Push =====

                    git push origin HEAD:%GITOPS_BRANCH%

                    if errorlevel 1 (
                        echo.
                        echo ==========================================
                        echo Git Push FAILED
                        echo ==========================================
                        del /f /q "%GIT_ASKPASS%" >nul 2>&1
                        exit /b 1
                    )

                    echo.
                    echo ==========================================
                    echo Git Push Successful
                    echo ==========================================

                    echo.
                    echo ===== Remote Main After Push =====

                    git ls-remote origin refs/heads/%GITOPS_BRANCH%

                    del /f /q "%GIT_ASKPASS%" >nul 2>&1

                    endlocal
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
                    echo ===== Docker Image =====

                    docker images %DOCKER_IMAGE%:%BUILD_NUMBER%

                    echo.
                    echo ===== Loading Image into Kind =====

                    "%KIND_EXE%" load docker-image ^
                        %DOCKER_IMAGE%:%BUILD_NUMBER% ^
                        --name kind

                    if errorlevel 1 (
                        echo.
                        echo ERROR: Failed to load Docker image into Kind.
                        exit /b 1
                    )

                    echo.
                    echo ===== Kind Images =====

                    docker exec kind-control-plane ^
                        crictl images | findstr /i "%DOCKER_IMAGE%"
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

                dir("${GITOPS_DIR}") {

                    bat '''
                        @echo off

                        echo.
                        echo ===== Kubernetes Manifest =====

                        type "%GITOPS_MANIFEST%"

                        echo.
                        echo ===== Creating Runtime Job Manifest =====

                        powershell -NoProfile -ExecutionPolicy Bypass -Command ^
                        "$file = '%GITOPS_MANIFEST%';" ^
                        "$content = Get-Content -Raw $file;" ^
                        "$content = $content -replace 'name:\\s*wifi-pytest-job', 'name: wifi-pytest-job-%BUILD_NUMBER%';" ^
                        "Set-Content -Path 'pytest-job-runtime.yaml' -Value $content -NoNewline;"

                        if errorlevel 1 (
                            echo ERROR: Failed to create runtime manifest.
                            exit /b 1
                        )

                        echo.
                        echo ===== Runtime Manifest =====

                        type pytest-job-runtime.yaml
                    '''
                }

                dir("${GITOPS_DIR}") {

                    bat '''
                        @echo off

                        echo.
                        echo ===== Applying Kubernetes Job =====

                        kubectl delete job ^
                            -l app=wifi-pytest ^
                            -n %K8S_NAMESPACE% ^
                            --ignore-not-found=true

                        kubectl apply ^
                            -f pytest-job-runtime.yaml ^
                            -n %K8S_NAMESPACE%

                        if errorlevel 1 (
                            echo.
                            echo ERROR: Kubernetes Job creation failed.
                            exit /b 1
                        )

                        echo.
                        echo ===== Kubernetes Jobs =====

                        kubectl get jobs -n %K8S_NAMESPACE%
                    '''
                }
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
                    echo ===== Waiting for Kubernetes Job =====

                    kubectl wait ^
                        --for=condition=complete ^
                        job/wifi-pytest-job-%BUILD_NUMBER% ^
                        -n %K8S_NAMESPACE% ^
                        --timeout=10m

                    if errorlevel 1 (
                        echo.
                        echo Job did not complete successfully.
                        echo.
                        echo ===== Job Status =====
                        kubectl get job wifi-pytest-job-%BUILD_NUMBER% ^
                            -n %K8S_NAMESPACE% ^
                            -o wide

                        echo.
                        echo ===== Pods =====
                        kubectl get pods ^
                            -n %K8S_NAMESPACE% ^
                            -l job-name=wifi-pytest-job-%BUILD_NUMBER%

                        echo.
                        echo ===== Pod Logs =====
                        kubectl logs ^
                            -n %K8S_NAMESPACE% ^
                            -l job-name=wifi-pytest-job-%BUILD_NUMBER% ^
                            --all-containers=true

                        exit /b 1
                    )

                    echo.
                    echo ==========================================
                    echo Kubernetes Pytest Job Completed
                    echo ==========================================

                    echo.
                    echo ===== Job =====

                    kubectl get job ^
                        wifi-pytest-job-%BUILD_NUMBER% ^
                        -n %K8S_NAMESPACE%

                    echo.
                    echo ===== Pods =====

                    kubectl get pods ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=wifi-pytest-job-%BUILD_NUMBER%

                    echo.
                    echo ===== Pytest Logs =====

                    kubectl logs ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=wifi-pytest-job-%BUILD_NUMBER% ^
                        --all-containers=true
                '''
            }
        }


        // ============================================================
        // 12. CREATE REPORTS READER
        // ============================================================
        stage('Create Reports Reader') {

            steps {

                echo ''
                echo '=========================================='
                echo 'Create Reports Reader'
                echo '=========================================='

                bat '''
                    @echo off

                    echo.
                    echo ===== Checking Reports PVC =====

                    kubectl get pvc -n %K8S_NAMESPACE%

                    echo.
                    echo ===== Reports PVC =====

                    kubectl get pvc ^
                        wifi-pytest-reports-pvc ^
                        -n %K8S_NAMESPACE%

                    if errorlevel 1 (
                        echo.
                        echo ERROR: Reports PVC not found.
                        exit /b 1
                    )

                    echo.
                    echo Reports PVC is available.
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

                    if not exist reports mkdir reports

                    echo.
                    echo ===== Finding Completed Pytest Pod =====

                    kubectl get pods ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=wifi-pytest-job-%BUILD_NUMBER% ^
                        -o wide

                    echo.
                    echo ===== Reports Collection =====

                    echo Report collection depends on the mounted
                    echo reports PVC and reader configuration.

                    echo.
                    echo ===== Kubernetes Resources =====

                    kubectl get all -n %K8S_NAMESPACE%
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
                    echo ===== Reports Directory =====

                    if exist reports (
                        dir /s reports
                    ) else (
                        echo Reports directory does not exist yet.
                    )

                    echo.
                    echo ===== Kubernetes Job Status =====

                    kubectl get job ^
                        wifi-pytest-job-%BUILD_NUMBER% ^
                        -n %K8S_NAMESPACE%

                    echo.
                    echo ===== Kubernetes Pod Status =====

                    kubectl get pods ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=wifi-pytest-job-%BUILD_NUMBER%
                '''
            }
        }
    }


    // =================================================================
    // POST ACTIONS
    // =================================================================
    post {

        always {

            echo ''
            echo '=========================================='
            echo 'Pipeline Post Actions'
            echo '=========================================='

            script {

                if (fileExists('reports/junit-results.xml')) {

                    echo 'JUnit report found.'

                    junit(
                        testResults: 'reports/junit-results.xml',
                        allowEmptyResults: true
                    )

                } else {

                    echo 'JUnit report not available.'
                }
            }

            archiveArtifacts(
                artifacts: 'reports/**/*',
                allowEmptyArchive: true
            )
        }


        success {

            echo ''
            echo '=========================================='
            echo 'PIPELINE SUCCESS'
            echo '=========================================='

            echo "Build Number: ${env.BUILD_NUMBER}"
        }


        failure {

            echo ''
            echo '=========================================='
            echo 'PIPELINE FAILED'
            echo '=========================================='

            echo "Build Number: ${env.BUILD_NUMBER}"
            echo 'Check the failed stage above.'
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
                    echo ===== Kubernetes Jobs =====

                    kubectl get jobs -n %K8S_NAMESPACE% 2>nul

                    echo.
                    echo ===== Kubernetes Pods =====

                    kubectl get pods -n %K8S_NAMESPACE% 2>nul

                    echo.
                    echo ===== Workspace Cleanup =====

                    if exist git-askpass.bat (
                        del /f /q git-askpass.bat >nul 2>&1
                    )

                    echo Cleanup completed.
                '''
            }
        }
    }
}