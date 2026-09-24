pipeline {

    agent any

    options {
        skipDefaultCheckout(true)

        timestamps()

        timeout(time: 30, unit: 'MINUTES')

        buildDiscarder(
            logRotator(
                numToKeepStr: '20'
            )
        )
    }

    environment {

        // ============================================================
        // Python
        // ============================================================

        PYTHON_EXE =
            'C:\\Users\\USER\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'

        // ============================================================
        // Kind
        // ============================================================

        KIND_EXE =
            'C:\\Users\\USER\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe\\kind.exe'

        KIND_CLUSTER = 'kind'

        // ============================================================
        // Docker
        // ============================================================

        DOCKER_IMAGE =
            'vengateshbabu1605/wifi-pytest-advanced'

        // ============================================================
        // GitOps
        // ============================================================

        GITOPS_REPO =
            'https://github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git'

        GITOPS_DIR = 'gitops-repo'

        GITOPS_BRANCH = 'main'

        GITOPS_CREDENTIALS = 'github-gitops-creds'

        // ============================================================
        // Kubernetes
        // ============================================================

        K8S_NAMESPACE = 'default'

        K8S_MANIFEST =
            'k8s\\pytest-job.yaml'

        K8S_JOB_PREFIX =
            'wifi-pytest-job'

        // ============================================================
        // Reports
        // ============================================================

        REPORT_DIR = 'reports'

    }

    stages {

        // ============================================================
        // 1. CHECKOUT SOURCE
        // ============================================================

        stage('Checkout Source') {

            steps {

                echo '=========================================='
                echo 'Checkout Source Repository'
                echo '=========================================='

                checkout scm

                bat '''
                    echo ===== Git Version =====
                    git --version

                    echo.
                    echo ===== Current Commit =====
                    git log -1 --oneline

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

                echo '=========================================='
                echo 'Verifying Environment'
                echo '=========================================='

                bat '''
                    echo ===== Python =====

                    "%PYTHON_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: Python executable not found.
                        echo Expected:
                        echo %PYTHON_EXE%
                        exit /b 1
                    )

                    echo.
                    echo ===== Docker =====

                    docker --version

                    if errorlevel 1 (
                        echo ERROR: Docker is not available.
                        exit /b 1
                    )

                    echo.
                    echo ===== Kind =====

                    "%KIND_EXE%" version

                    if errorlevel 1 (
                        echo ERROR: Kind executable not found.
                        echo Expected:
                        echo %KIND_EXE%
                        exit /b 1
                    )

                    echo.
                    echo ===== Kubectl =====

                    kubectl version --client

                    if errorlevel 1 (
                        echo ERROR: kubectl is not available.
                        exit /b 1
                    )

                    echo.
                    echo ===== Kubernetes Context =====

                    kubectl config current-context

                    if errorlevel 1 (
                        echo ERROR: Kubernetes context unavailable.
                        exit /b 1
                    )

                    echo.
                    echo ===== Kubernetes Nodes =====

                    kubectl get nodes -o wide

                    if errorlevel 1 (
                        echo ERROR: Kubernetes API is unavailable.
                        exit /b 1
                    )

                    echo.
                    echo ===== Kind Nodes =====

                    "%KIND_EXE%" get nodes --name "%KIND_CLUSTER%"

                    if errorlevel 1 (
                        echo ERROR: Kind cluster is unavailable.
                        exit /b 1
                    )

                    echo.
                    echo ===== Docker Info =====

                    docker info --format "CPUs={{.NCPU}} Memory={{.MemTotal}}"

                    if errorlevel 1 (
                        echo ERROR: Docker daemon is unavailable.
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

                echo '=========================================='
                echo 'Building Docker Image'
                echo '=========================================='

                bat '''
                    echo ===== Docker Image =====

                    echo %DOCKER_IMAGE%:%BUILD_NUMBER%

                    echo.

                    echo ===== Docker Build =====

                    docker build ^
                        -t %DOCKER_IMAGE%:%BUILD_NUMBER% ^
                        .

                    if errorlevel 1 (
                        echo ERROR: Docker image build failed.
                        exit /b 1
                    )

                    echo.

                    echo ===== Docker Image Created =====

                    docker images %DOCKER_IMAGE%

                    echo.

                    echo ==========================================
                    echo Docker Build Successful
                    echo ==========================================
                '''
            }
        }


        // ============================================================
        // 4. CLONE GITOPS REPOSITORY
        // ============================================================

        stage('Clone GitOps Repository') {

            steps {

                echo '=========================================='
                echo 'Cloning GitOps Repository'
                echo '=========================================='

                dir("${GITOPS_DIR}") {

                    deleteDir()

                    bat '''
                        echo ===== Clone GitOps Repository =====

                        git clone %GITOPS_REPO% .

                        if errorlevel 1 (
                            echo ERROR: GitOps repository clone failed.
                            exit /b 1
                        )

                        echo.

                        echo ===== GitOps Branch =====

                        git branch

                        echo.

                        echo ===== GitOps Commit =====

                        git log -1 --oneline
                    '''
                }
            }
        }


        // ============================================================
        // 5. VERIFY GITOPS REPOSITORY
        // ============================================================

        stage('Verify GitOps Repository') {

            steps {

                echo '=========================================='
                echo 'Verifying GitOps Repository'
                echo '=========================================='

                dir("${GITOPS_DIR}") {

                    bat '''
                        echo ===== Git Remote =====

                        git remote -v

                        echo.

                        echo ===== Local Commit =====

                        git log -1 --oneline

                        echo.

                        echo ===== Remote Main =====

                        git ls-remote origin refs/heads/main

                        if errorlevel 1 (
                            echo ERROR: GitHub connectivity failed.
                            exit /b 1
                        )

                        echo.

                        echo GitHub Connectivity Successful
                    '''
                }
            }
        }


        // ============================================================
        // 6. UPDATE GITOPS MANIFEST
        // ============================================================

        stage('Update GitOps Manifest') {

            steps {

                echo '=========================================='
                echo 'Updating GitOps Kubernetes Manifest'
                echo '=========================================='

                dir("${GITOPS_DIR}") {

                    bat '''
                        echo ===== Manifest Before Update =====

                        findstr /N "image:" %K8S_MANIFEST%

                        echo.

                        echo ===== Updating Image =====

                        powershell -NoProfile -Command ^
                        "(Get-Content '%K8S_MANIFEST%') -replace 'image: vengateshbabu1605/wifi-pytest-advanced:[^ ]+', 'image: vengateshbabu1605/wifi-pytest-advanced:%BUILD_NUMBER%' | Set-Content '%K8S_MANIFEST%'"

                        if errorlevel 1 (
                            echo ERROR: Manifest update failed.
                            exit /b 1
                        )

                        echo.

                        echo ===== Manifest After Update =====

                        findstr /N "image:" %K8S_MANIFEST%

                        echo.

                        echo ===== Git Diff =====

                        git diff -- %K8S_MANIFEST%
                    '''
                }
            }
        }


        // ============================================================
        // 7. COMMIT GITOPS CHANGES
        // ============================================================

        stage('Commit GitOps Changes') {

            steps {

                echo '=========================================='
                echo 'Committing GitOps Changes'
                echo '=========================================='

                dir("${GITOPS_DIR}") {

                    bat '''
                        echo ===== Git Status =====

                        git status

                        echo.

                        echo ===== Git Add =====

                        git add %K8S_MANIFEST%

                        if errorlevel 1 (
                            echo ERROR: Git add failed.
                            exit /b 1
                        )

                        echo.

                        echo ===== Configure Git Identity =====

                        git config user.name "Jenkins CI"

                        git config user.email "jenkins@localhost"

                        echo.

                        echo ===== Verify Git Identity =====

                        git config user.name

                        git config user.email

                        echo.

                        echo ===== Git Commit =====

                        git commit -m "Update image to build %BUILD_NUMBER%"

                        if errorlevel 1 (
                            echo ERROR: Git commit failed.
                            exit /b 1
                        )
                    '''
                }
            }
        }


        // ============================================================
        // 8. PUSH GITOPS CHANGES
        // ============================================================

        stage('Push GitOps Changes') {

            steps {

                timeout(time: 3, unit: 'MINUTES') {

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
                                echo ===== Git Remote =====

                                git remote -v

                                echo.

                                echo ===== Local Commit =====

                                git log -1 --oneline

                                echo.

                                echo ===== Preparing GitHub Authentication =====

                                (
                                    echo @echo off
                                    echo set "PROMPT=%%~1"
                                    echo echo %%PROMPT%% ^| findstr /I "Username" ^>nul
                                    echo if not errorlevel 1 (
                                    echo     echo %%GIT_USERNAME%%
                                    echo ) else (
                                    echo     echo %%GIT_PASSWORD%%
                                    echo )
                                ) > git-askpass.cmd

                                set GIT_ASKPASS=%CD%\\git-askpass.cmd

                                set GIT_TERMINAL_PROMPT=0

                                git remote set-url origin https://%GIT_USERNAME%@github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git

                                echo.

                                echo ===== GitHub Push =====

                                git push origin main

                                if errorlevel 1 (
                                    echo.
                                    echo ==========================================
                                    echo Git Push FAILED
                                    echo ==========================================
                                    del /q git-askpass.cmd
                                    exit /b 1
                                )

                                echo.

                                echo ==========================================
                                echo Git Push SUCCESSFUL
                                echo ==========================================

                                del /q git-askpass.cmd
                            '''
                        }
                    }
                }
            }
        }


        // ============================================================
        // 9. LOAD DOCKER IMAGE INTO KIND
        // ============================================================

        stage('Load Docker Image into Kind') {

            steps {

                echo '=========================================='
                echo 'Loading Docker Image into Kind'
                echo '=========================================='

                bat '''
                    echo ===== Docker Image =====

                    docker images %DOCKER_IMAGE%:%BUILD_NUMBER%

                    if errorlevel 1 (
                        echo ERROR: Docker image does not exist.
                        exit /b 1
                    )

                    echo.

                    echo ===== Loading Image into Kind =====

                    "%KIND_EXE%" load docker-image ^
                        %DOCKER_IMAGE%:%BUILD_NUMBER% ^
                        --name "%KIND_CLUSTER%"

                    if errorlevel 1 (
                        echo ERROR: Failed to load Docker image into Kind.
                        exit /b 1
                    )

                    echo.

                    echo ===== Image Loaded Successfully =====

                    "%KIND_EXE%" get nodes --name "%KIND_CLUSTER%"
                '''
            }
        }


        // ============================================================
        // 10. PREPARE KUBERNETES JOB
        // ============================================================

        stage('Prepare Kubernetes Job') {

            steps {

                echo '=========================================='
                echo 'Preparing Kubernetes Job'
                echo '=========================================='

                dir("${GITOPS_DIR}") {

                    bat '''
                        echo ===== Kubernetes Context =====

                        kubectl config current-context

                        if errorlevel 1 (
                            echo ERROR: Kubernetes context unavailable.
                            exit /b 1
                        )

                        echo.

                        echo ===== Kubernetes Cluster =====

                        kubectl get nodes

                        if errorlevel 1 (
                            echo ERROR: Kubernetes API unavailable.
                            exit /b 1
                        }

                        echo.

                        echo ===== Preparing Build-Specific Manifest =====

                        powershell -NoProfile -Command ^
                        "$content = Get-Content '%K8S_MANIFEST%' -Raw; ^
                        $content = $content -replace '(?m)^\\s*generateName:\\s*.*\\r?\\n', ''; ^
                        $content = $content -replace '(?m)^(\\s{2}name:\\s*)wifi-pytest-job\\s*$', '$1wifi-pytest-job-%BUILD_NUMBER%'; ^
                        $content = $content -replace 'imagePullPolicy:\\s*Always', 'imagePullPolicy: Never'; ^
                        Set-Content 'k8s\\pytest-job-build.yaml' $content"

                        if errorlevel 1 (
                            echo ERROR: Failed to prepare Kubernetes manifest.
                            exit /b 1
                        )

                        echo.

                        echo ===== Prepared Manifest =====

                        findstr /N "name:" k8s\\pytest-job-build.yaml

                        echo.

                        echo ===== Image =====

                        findstr /N "image:" k8s\\pytest-job-build.yaml

                        echo.

                        echo ===== Image Pull Policy =====

                        findstr /N "imagePullPolicy:" k8s\\pytest-job-build.yaml

                        echo.

                        echo ===== Delete Previous Build Job =====

                        kubectl delete job wifi-pytest-job-%BUILD_NUMBER% ^
                            -n %K8S_NAMESPACE% ^
                            --ignore-not-found=true

                        echo.

                        echo ===== Create Kubernetes Job =====

                        kubectl apply -f k8s\\pytest-job-build.yaml

                        if errorlevel 1 (
                            echo ERROR: Kubernetes Job creation failed.
                            exit /b 1
                        )

                        echo.

                        echo ===== Kubernetes Job Created =====

                        kubectl get job wifi-pytest-job-%BUILD_NUMBER% ^
                            -n %K8S_NAMESPACE%

                        if errorlevel 1 (
                            echo ERROR: Expected Kubernetes Job was not created.
                            echo.
                            echo ===== All Jobs =====
                            kubectl get jobs -A
                            exit /b 1
                        )
                    '''
                }
            }
        }


        // ============================================================
        // 11. RUN PYTEST IN KUBERNETES
        // ============================================================

        stage('Run Pytest in Kubernetes') {

            steps {

                echo '=========================================='
                echo 'Running Pytest in Kubernetes'
                echo '=========================================='

                bat '''
                    echo ===== Waiting For Kubernetes Job =====

                    kubectl wait ^
                        --for=condition=complete ^
                        job/wifi-pytest-job-%BUILD_NUMBER% ^
                        -n %K8S_NAMESPACE% ^
                        --timeout=10m

                    if errorlevel 1 (

                        echo.
                        echo ==========================================
                        echo Kubernetes Job Did Not Complete
                        echo ==========================================

                        echo.
                        echo ===== Job Status =====

                        kubectl get job wifi-pytest-job-%BUILD_NUMBER% ^
                            -n %K8S_NAMESPACE% ^
                            -o wide

                        echo.
                        echo ===== Pods =====

                        kubectl get pods ^
                            -n %K8S_NAMESPACE% ^
                            -l job-name=wifi-pytest-job-%BUILD_NUMBER% ^
                            -o wide

                        echo.
                        echo ===== Pod Description =====

                        kubectl describe pod ^
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
                    echo Kubernetes Job Completed
                    echo ==========================================

                    echo.
                    echo ===== Job Status =====

                    kubectl get job wifi-pytest-job-%BUILD_NUMBER% ^
                        -n %K8S_NAMESPACE%

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

                echo '=========================================='
                echo 'Creating Kubernetes Reports Reader'
                echo '=========================================='

                bat '''
                    if exist "%REPORT_DIR%" (
                        rmdir /s /q "%REPORT_DIR%"
                    )

                    mkdir "%REPORT_DIR%"

                    echo Reports directory created.
                '''
            }
        }


        // ============================================================
        // 13. COLLECT KUBERNETES REPORTS
        // ============================================================

        stage('Collect Kubernetes Reports') {

            steps {

                echo '=========================================='
                echo 'Collecting Kubernetes Reports'
                echo '=========================================='

                bat '''
                    echo ===== Kubernetes Pods =====

                    kubectl get pods ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=wifi-pytest-job-%BUILD_NUMBER% ^
                        -o wide

                    echo.

                    echo ===== Finding Pod =====

                    for /f "tokens=*" %%P in ('kubectl get pods -n %K8S_NAMESPACE% -l job-name=wifi-pytest-job-%BUILD_NUMBER% -o jsonpath="{.items[0].metadata.name}"') do (

                        echo Pod: %%P

                        echo.

                        echo ===== Pod Files =====

                        kubectl exec ^
                            -n %K8S_NAMESPACE% ^
                            %%P ^
                            -- ls -la /app/reports

                        echo.

                        echo ===== Copy HTML Report =====

                        kubectl cp ^
                            %K8S_NAMESPACE%/%%P:/app/reports ^
                            "%WORKSPACE%\\reports\\kubernetes" ^
                            -c pytest

                    )

                    if exist "%REPORT_DIR%\\kubernetes" (

                        echo.
                        echo ===== Collected Kubernetes Reports =====

                        dir /s "%REPORT_DIR%\\kubernetes"

                    ) else (

                        echo.
                        echo WARNING: Kubernetes reports directory was not copied.

                    )
                '''
            }
        }


        // ============================================================
        // 14. VERIFY REPORTS
        // ============================================================

        stage('Verify Reports') {

            steps {

                echo '=========================================='
                echo 'Verifying Test Reports'
                echo '=========================================='

                bat '''
                    echo ===== Workspace Reports =====

                    if exist "%REPORT_DIR%" (
                        dir /s "%REPORT_DIR%"
                    ) else (
                        echo Reports directory does not exist.
                    )

                    echo.

                    echo ===== Searching JUnit XML =====

                    dir /s /b "%REPORT_DIR%\\*.xml" 2>nul

                    echo.

                    echo ===== Searching HTML Reports =====

                    dir /s /b "%REPORT_DIR%\\*.html" 2>nul

                    echo.

                    echo ===== Kubernetes Job =====

                    kubectl get job wifi-pytest-job-%BUILD_NUMBER% ^
                        -n %K8S_NAMESPACE%

                    echo.

                    echo ===== Kubernetes Pods =====

                    kubectl get pods ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=wifi-pytest-job-%BUILD_NUMBER%
                '''
            }
        }
    }


    // ================================================================
    // POST ACTIONS
    // ================================================================

    post {

        always {

            echo '=========================================='
            echo 'Pipeline Post Actions'
            echo '=========================================='

            script {

                // ----------------------------------------------------
                // Publish JUnit
                // ----------------------------------------------------

                if (fileExists('reports/junit-results.xml')) {

                    echo 'Publishing JUnit results.'

                    junit(
                        testResults: 'reports/junit-results.xml',
                        allowEmptyResults: true
                    )

                } else {

                    echo 'JUnit report not available.'
                }


                // ----------------------------------------------------
                // Archive Reports
                // ----------------------------------------------------

                archiveArtifacts(
                    artifacts: 'reports/**/*',
                    allowEmptyArchive: true,
                    fingerprint: true
                )
            }


            // --------------------------------------------------------
            // Cleanup / Diagnostics
            // --------------------------------------------------------

            echo '=========================================='
            echo 'Kubernetes Diagnostics / Cleanup'
            echo '=========================================='

            bat '''
                echo ===== Kubernetes Jobs =====

                kubectl get jobs -A || echo WARNING: Unable to query Kubernetes jobs.

                echo.

                echo ===== Kubernetes Pods =====

                kubectl get pods -A || echo WARNING: Unable to query Kubernetes pods.

                echo.

                echo ===== Workspace Cleanup =====

                if exist gitops-repo\\git-askpass.cmd (
                    del /q gitops-repo\\git-askpass.cmd
                )

                if exist gitops-repo\\k8s\\pytest-job-build.yaml (
                    del /q gitops-repo\\k8s\\pytest-job-build.yaml
                )

                echo Cleanup completed.
            '''
        }


        success {

            echo '=========================================='
            echo 'PIPELINE SUCCESSFUL'
            echo '=========================================='

            echo "Build Number: ${env.BUILD_NUMBER}"

            echo "Docker Image: ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}"

            echo "Kubernetes Job: wifi-pytest-job-${env.BUILD_NUMBER}"

            echo '=========================================='
        }


        failure {

            echo '=========================================='
            echo 'PIPELINE FAILED'
            echo '=========================================='

            echo "Build Number: ${env.BUILD_NUMBER}"

            echo 'Check the failed stage above.'

            echo '=========================================='
        }
    }
}

