pipeline {

    agent any

    environment {
        PYTHON_EXE = 'C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'

        DOCKER_IMAGE = 'vengateshbabu1605/wifi-pytest-advanced'
        GITOPS_REPO = 'https://github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git'

        GITOPS_CREDENTIALS = 'github-gitops-creds'

        KIND_CLUSTER = 'kind'
        K8S_NAMESPACE = 'default'
        K8S_JOB_NAME = 'wifi-pytest-job'

        IMAGE_TAG = "${BUILD_NUMBER}"
        FULL_IMAGE = "vengateshbabu1605/wifi-pytest-advanced:${BUILD_NUMBER}"
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

                    echo.
                    echo ===== Docker =====
                    docker --version

                    echo.
                    echo ===== Kind =====
                    kind version

                    echo.
                    echo ===== Kubectl =====
                    kubectl version --client

                    echo.
                    echo ===== Kubernetes Context =====
                    kubectl config current-context

                    echo.
                    echo ===== Kubernetes Nodes =====
                    kubectl get nodes -o wide

                    echo.
                    echo ===== Kind Nodes =====
                    kind get nodes

                    echo.
                    echo ===== Docker Info =====
                    docker info --format "CPUs={{.NCPU}} Memory={{.MemTotal}}"
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
                    echo %FULL_IMAGE%

                    echo.
                    echo ===== Docker Build =====

                    docker build ^
                        -t %FULL_IMAGE% ^
                        .

                    if errorlevel 1 (
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
        // 5. VERIFY GITOPS REPOSITORY
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
        // 6. UPDATE GITOPS MANIFEST
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
                        "(Get-Content 'k8s\\pytest-job.yaml') -replace 'image: vengateshbabu1605/wifi-pytest-advanced:[^ ]+', 'image: %FULL_IMAGE%' | Set-Content 'k8s\\pytest-job.yaml'"

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
        // 7. COMMIT GITOPS CHANGES
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
        // 8. PUSH GITOPS CHANGES
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

                                rem ------------------------------------------------
                                rem Create temporary Git AskPass script.
                                rem Git invokes this script when it needs the
                                rem password.
                                rem ------------------------------------------------

                                (
                                    echo @echo off
                                    echo echo %%GIT_PASSWORD%%
                                ) > git-askpass.cmd

                                set GIT_ASKPASS=%CD%\\git-askpass.cmd
                                set GIT_TERMINAL_PROMPT=0

                                rem ------------------------------------------------
                                rem Put username in remote URL.
                                rem PAT remains supplied through GIT_ASKPASS.
                                rem ------------------------------------------------

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
                    docker images %FULL_IMAGE%

                    echo.
                    echo ===== Loading Image into Kind =====

                    kind load docker-image %FULL_IMAGE% --name %KIND_CLUSTER%

                    if errorlevel 1 (
                        echo ERROR: Failed to load Docker image into Kind.
                        exit /b 1
                    )

                    echo.
                    echo ===== Image Loaded Successfully =====

                    docker exec %KIND_CLUSTER%-control-plane \
                        crictl images | findstr wifi-pytest
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

                dir('gitops-repo') {

                    bat '''
                        echo ===== Kubernetes Manifest =====

                        type k8s\\pytest-job.yaml

                        echo.
                        echo ===== Delete Existing Job =====

                        kubectl delete job %K8S_JOB_NAME% ^
                            -n %K8S_NAMESPACE% ^
                            --ignore-not-found=true

                        echo.
                        echo ===== Apply Kubernetes Job =====

                        kubectl apply ^
                            -f k8s\\pytest-job.yaml

                        if errorlevel 1 (
                            echo ERROR: Kubernetes Job creation failed.
                            exit /b 1
                        )

                        echo.
                        echo ===== Kubernetes Job =====

                        kubectl get job ^
                            %K8S_JOB_NAME% ^
                            -n %K8S_NAMESPACE%
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

                timeout(time: 10, unit: 'MINUTES') {

                    bat '''
                        echo ===== Waiting for Kubernetes Job =====

                        kubectl wait ^
                            --for=condition=complete ^
                            job/%K8S_JOB_NAME% ^
                            -n %K8S_NAMESPACE% ^
                            --timeout=600s

                        if errorlevel 1 (
                            echo.
                            echo WARNING: Kubernetes Job did not complete successfully.

                            echo.
                            echo ===== Job Status =====
                            kubectl get job %K8S_JOB_NAME% -n %K8S_NAMESPACE%

                            echo.
                            echo ===== Pod Status =====
                            kubectl get pods -n %K8S_NAMESPACE% -l job-name=%K8S_JOB_NAME%

                            echo.
                            echo ===== Pod Logs =====
                            kubectl logs -n %K8S_NAMESPACE% -l job-name=%K8S_JOB_NAME% --tail=200

                            exit /b 1
                        )

                        echo.
                        echo ===== Kubernetes Job Completed =====

                        kubectl get job %K8S_JOB_NAME% -n %K8S_NAMESPACE%

                        echo.
                        echo ===== Pytest Logs =====

                        kubectl logs ^
                            -n %K8S_NAMESPACE% ^
                            -l job-name=%K8S_JOB_NAME%
                    '''
                }
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
                    echo ===== Kubernetes Pods =====

                    kubectl get pods ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=%K8S_JOB_NAME%

                    echo.
                    echo ===== Reports Reader =====

                    kubectl run pytest-reports-reader ^
                        -n %K8S_NAMESPACE% ^
                        --image=busybox:1.36 ^
                        --restart=Never ^
                        --command -- sleep 300

                    if errorlevel 1 (
                        echo WARNING: Reports reader creation failed.
                    )
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
                    echo ===== Kubernetes Jobs =====

                    kubectl get jobs -A

                    echo.
                    echo ===== Kubernetes Pods =====

                    kubectl get pods -A -o wide

                    echo.
                    echo ===== Pytest Job Logs =====

                    kubectl logs ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=%K8S_JOB_NAME% ^
                        --tail=500
                '''
            }
        }


        // ============================================================
        // 14. VERIFY REPORTS
        // ============================================================

        stage('Verify Reports') {
            steps {

                echo '=========================================='
                echo 'Verifying Kubernetes Test Results'
                echo '=========================================='

                bat '''
                    echo ===== Job Status =====

                    kubectl get job ^
                        %K8S_JOB_NAME% ^
                        -n %K8S_NAMESPACE%

                    echo.
                    echo ===== Pod Status =====

                    kubectl get pods ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=%K8S_JOB_NAME%

                    echo.
                    echo ===== Final Test Logs =====

                    kubectl logs ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=%K8S_JOB_NAME% ^
                        --tail=500
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

                    echo 'JUnit report found.'
                    junit 'reports/junit-results.xml'

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

            echo '=========================================='
            echo 'PIPELINE SUCCESS'
            echo '=========================================='

            echo "Build Number: ${BUILD_NUMBER}"
            echo "Docker Image: ${FULL_IMAGE}"
        }


        failure {

            echo '=========================================='
            echo 'PIPELINE FAILED'
            echo '=========================================='

            echo "Build Number: ${BUILD_NUMBER}"
            echo 'Check the failed stage above.'
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

