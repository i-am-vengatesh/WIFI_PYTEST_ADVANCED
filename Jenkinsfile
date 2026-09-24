pipeline {

    agent any

    environment {

        // ============================================================
        // Python
        // ============================================================
        PYTHON_EXE = 'C:\\Users\\USER\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'

        // ============================================================
        // Docker
        // ============================================================
        DOCKER_IMAGE = "vengateshbabu1605/wifi-pytest-advanced:${BUILD_NUMBER}"

        // ============================================================
        // Kind
        // Jenkins service PATH does not contain kind.exe
        // ============================================================
        KIND_EXE = 'C:\\Users\\USER\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe\\kind.exe'

        KIND_CLUSTER = 'kind'

        // ============================================================
        // GitHub repositories
        // ============================================================
        SOURCE_REPO = 'https://github.com/i-am-vengatesh/WIFI_PYTEST_ADVANCED.git'
        GITOPS_REPO = 'https://github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git'

        // ============================================================
        // Kubernetes
        // ============================================================
        K8S_NAMESPACE = 'default'
        K8S_JOB_NAME = "wifi-pytest-job-${BUILD_NUMBER}"

        // ============================================================
        // Reports
        // ============================================================
        REPORT_DIR = 'reports'
        JUNIT_REPORT = 'reports/junit-results.xml'
        HTML_REPORT = 'reports/wlan_test_report.html'
    }


    stages {


        // ============================================================
        // 1. Checkout Source
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
        // 2. Verify Environment
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
        // 3. Build Docker Image
        // ============================================================
        stage('Build Docker Image') {

            steps {

                echo '=========================================='
                echo 'Building Docker Image'
                echo '=========================================='

                bat '''
                    echo ===== Docker Image =====
                    echo %DOCKER_IMAGE%

                    echo.
                    echo ===== Docker Build =====

                    docker build ^
                        -t %DOCKER_IMAGE% ^
                        .

                    if errorlevel 1 (
                        echo ERROR: Docker image build failed.
                        exit /b 1
                    )

                    echo.
                    echo ===== Docker Image Created =====

                    docker images vengateshbabu1605/wifi-pytest-advanced
                '''
            }
        }


        // ============================================================
        // 4. Clone GitOps Repository
        // ============================================================
        stage('Clone GitOps Repository') {

            steps {

                echo '=========================================='
                echo 'Cloning GitOps Repository'
                echo '=========================================='

                dir('gitops-repo') {

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
        // 5. Verify GitOps Repository
        // ============================================================
        stage('Verify GitOps Repository') {

            steps {

                echo '=========================================='
                echo 'Verifying GitOps Repository'
                echo '=========================================='

                dir('gitops-repo') {

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
        // 6. Update GitOps Manifest
        // ============================================================
        stage('Update GitOps Manifest') {

            steps {

                echo '=========================================='
                echo 'Updating GitOps Kubernetes Manifest'
                echo '=========================================='

                dir('gitops-repo') {

                    bat '''
                        echo ===== Manifest Before Update =====

                        findstr /N "image:" k8s\\pytest-job.yaml

                        echo.
                        echo ===== Updating Image =====

                        powershell -NoProfile -Command ^
                        "(Get-Content 'k8s\\pytest-job.yaml') -replace 'image: vengateshbabu1605/wifi-pytest-advanced:[^ ]+', 'image: vengateshbabu1605/wifi-pytest-advanced:%BUILD_NUMBER%' | Set-Content 'k8s\\pytest-job.yaml'"

                        if errorlevel 1 (
                            echo ERROR: Manifest update failed.
                            exit /b 1
                        )

                        echo.
                        echo ===== Manifest After Update =====

                        findstr /N "image:" k8s\\pytest-job.yaml

                        echo.
                        echo ===== Git Diff =====

                        git diff -- k8s\\pytest-job.yaml
                    '''
                }
            }
        }


        // ============================================================
        // 7. Commit GitOps Changes
        // ============================================================
        stage('Commit GitOps Changes') {

            steps {

                echo '=========================================='
                echo 'Committing GitOps Changes'
                echo '=========================================='

                dir('gitops-repo') {

                    bat '''
                        echo ===== Git Status =====
                        git status

                        echo.
                        echo ===== Git Add =====

                        git add k8s\\pytest-job.yaml

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
        // 8. Push GitOps Changes
        // ============================================================
        stage('Push GitOps Changes') {

            steps {

                timeout(time: 3, unit: 'MINUTES') {

                    echo '=========================================='
                    echo 'Pushing GitOps Changes'
                    echo '=========================================='

                    dir('gitops-repo') {

                        withCredentials([
                            usernamePassword(
                                credentialsId: 'github-gitops-creds',
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
                                    echo if not errorlevel 1 ^(
                                    echo     echo %%GIT_USERNAME%%
                                    echo ^) else ^(
                                    echo     echo %%GIT_PASSWORD%%
                                    echo ^)
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
        // 9. Load Docker Image into Kind
        // ============================================================
        stage('Load Docker Image into Kind') {

            steps {

                echo '=========================================='
                echo 'Loading Docker Image into Kind'
                echo '=========================================='

                bat '''
                    echo ===== Docker Image =====

                    docker images %DOCKER_IMAGE%

                    if errorlevel 1 (
                        echo ERROR: Docker image does not exist.
                        exit /b 1
                    )

                    echo.
                    echo ===== Loading Image into Kind =====

                    "%KIND_EXE%" load docker-image %DOCKER_IMAGE% --name "%KIND_CLUSTER%"

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
        // 10. Prepare Kubernetes Job
        // ============================================================
        stage('Prepare Kubernetes Job') {

            steps {

                echo '=========================================='
                echo 'Preparing Kubernetes Job'
                echo '=========================================='

                dir('gitops-repo') {

                    bat '''
                        echo ===== Kubernetes Context =====

                        kubectl config current-context

                        echo.
                        echo ===== Delete Previous Job If Present =====

                        kubectl delete job %K8S_JOB_NAME% ^
                            -n %K8S_NAMESPACE% ^
                            --ignore-not-found=true

                        echo.
                        echo ===== Create Job From GitOps Manifest =====

                        powershell -NoProfile -Command ^
                        "(Get-Content 'k8s\\pytest-job.yaml') -replace 'name: wifi-pytest-job', 'name: %K8S_JOB_NAME%' | kubectl apply -f -"

                        if errorlevel 1 (
                            echo ERROR: Kubernetes Job creation failed.
                            exit /b 1
                        )

                        echo.
                        echo ===== Kubernetes Job Created =====

                        kubectl get job %K8S_JOB_NAME% -n %K8S_NAMESPACE%
                    '''
                }
            }
        }


        // ============================================================
        // 11. Run Pytest in Kubernetes
        // ============================================================
        stage('Run Pytest in Kubernetes') {

            steps {

                echo '=========================================='
                echo 'Running Pytest in Kubernetes'
                echo '=========================================='

                timeout(time: 10, unit: 'MINUTES') {

                    bat '''
                        echo ===== Waiting For Kubernetes Job =====

                        kubectl wait ^
                            --for=condition=complete ^
                            job/%K8S_JOB_NAME% ^
                            -n %K8S_NAMESPACE% ^
                            --timeout=8m

                        if errorlevel 1 (
                            echo.
                            echo ERROR: Kubernetes Job did not complete successfully.

                            echo.
                            echo ===== Job Status =====
                            kubectl get job %K8S_JOB_NAME% -n %K8S_NAMESPACE% -o wide

                            echo.
                            echo ===== Pods =====
                            kubectl get pods -n %K8S_NAMESPACE% -l job-name=%K8S_JOB_NAME% -o wide

                            echo.
                            echo ===== Pod Description =====
                            kubectl describe pods -n %K8S_NAMESPACE% -l job-name=%K8S_JOB_NAME%

                            echo.
                            echo ===== Job Logs =====
                            kubectl logs job/%K8S_JOB_NAME% -n %K8S_NAMESPACE%

                            exit /b 1
                        )

                        echo.
                        echo ==========================================
                        echo Kubernetes Job Completed Successfully
                        echo ==========================================

                        echo.
                        echo ===== Job Status =====
                        kubectl get job %K8S_JOB_NAME% -n %K8S_NAMESPACE%

                        echo.
                        echo ===== Pytest Logs =====
                        kubectl logs job/%K8S_JOB_NAME% -n %K8S_NAMESPACE%
                    '''
                }
            }
        }


        // ============================================================
        // 12. Create Reports Reader
        // ============================================================
        stage('Create Reports Reader') {

            steps {

                echo '=========================================='
                echo 'Creating Reports Reader'
                echo '=========================================='

                bat '''
                    echo ===== Kubernetes Pods =====

                    kubectl get pods -n %K8S_NAMESPACE% ^
                        -l job-name=%K8S_JOB_NAME% -o wide

                    echo.
                    echo ===== Kubernetes Job Details =====

                    kubectl describe job %K8S_JOB_NAME% ^
                        -n %K8S_NAMESPACE%
                '''
            }
        }


        // ============================================================
        // 13. Collect Kubernetes Reports
        // ============================================================
        stage('Collect Kubernetes Reports') {

            steps {

                echo '=========================================='
                echo 'Collecting Kubernetes Reports'
                echo '=========================================='

                bat '''
                    if not exist reports mkdir reports

                    echo ===== Finding Pytest Pod =====

                    for /f "tokens=1" %%P in ('kubectl get pods -n %K8S_NAMESPACE% -l job-name=%K8S_JOB_NAME% --no-headers -o custom-columns^=NAME:.metadata.name') do (

                        echo Found Pod: %%P

                        echo.
                        echo ===== Pod Logs =====

                        kubectl logs %%P -n %K8S_NAMESPACE% > reports\\kubernetes-pytest.log

                        echo.
                        echo ===== Copy Reports From Pod =====

                        kubectl cp ^
                            %K8S_NAMESPACE%/%%P:/app/reports/. ^
                            reports\\

                        if errorlevel 1 (
                            echo WARNING: kubectl cp failed.
                        )
                    )

                    echo.
                    echo ===== Local Reports =====

                    dir reports
                '''
            }
        }


        // ============================================================
        // 14. Verify Reports
        // ============================================================
        stage('Verify Reports') {

            steps {

                echo '=========================================='
                echo 'Verifying Test Reports'
                echo '=========================================='

                bat '''
                    echo ===== Reports Directory =====

                    if not exist reports (
                        echo ERROR: Reports directory does not exist.
                        exit /b 1
                    )

                    dir reports

                    echo.
                    echo ===== JUnit XML =====

                    if exist reports\\junit-results.xml (
                        echo JUnit report found.
                    ) else (
                        echo ERROR: JUnit report not found.
                        exit /b 1
                    )

                    echo.
                    echo ===== HTML Report =====

                    if exist reports\\wlan_test_report.html (
                        echo HTML report found.
                    ) else (
                        echo WARNING: HTML report not found.
                    )

                    echo.
                    echo ===== Pytest Kubernetes Log =====

                    if exist reports\\kubernetes-pytest.log (
                        echo Kubernetes log found.
                    )

                    echo.
                    echo ==========================================
                    echo Report Verification Completed
                    echo ==========================================
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

                if (fileExists('reports/junit-results.xml')) {

                    echo 'Publishing JUnit results.'

                    junit(
                        testResults: 'reports/junit-results.xml',
                        allowEmptyResults: true,
                        keepLongStdio: true
                    )

                } else {

                    echo 'JUnit report not available.'
                }
            }


            // --------------------------------------------------------
            // Archive reports
            // --------------------------------------------------------
            archiveArtifacts(
                artifacts: 'reports/**/*',
                allowEmptyArchive: true,
                fingerprint: true
            )
        }


        success {

            echo '=========================================='
            echo 'PIPELINE SUCCESSFUL'
            echo '=========================================='

            echo "Build Number: ${BUILD_NUMBER}"
            echo "Docker Image: ${DOCKER_IMAGE}"
            echo "Kubernetes Job: ${K8S_JOB_NAME}"

            echo '=========================================='
        }


        failure {

            echo '=========================================='
            echo 'PIPELINE FAILED'
            echo '=========================================='

            echo "Build Number: ${BUILD_NUMBER}"
            echo 'Check the failed stage above.'

            echo '=========================================='
        }


        cleanup {

            echo '=========================================='
            echo 'Cleanup'
            echo '=========================================='

            script {

                bat '''
                    echo ===== Kubernetes Jobs =====

                    kubectl get jobs -A || exit /b 0

                    echo.
                    echo ===== Kubernetes Pods =====

                    kubectl get pods -A || exit /b 0

                    echo.
                    echo ===== Workspace Cleanup =====

                    if exist gitops-repo\\git-askpass.cmd (
                        del /q gitops-repo\\git-askpass.cmd
                    )

                    echo Cleanup completed.
                '''
            }
        }
    }
}

