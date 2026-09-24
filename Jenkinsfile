pipeline {

    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    environment {

        // ============================================================
        // Local Tools
        // ============================================================

        PYTHON_EXE = 'C:\\Users\\USER\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'

        KIND_EXE = 'C:\\Users\\USER\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe\\kind.exe'


        // ============================================================
        // Docker
        // ============================================================

        IMAGE_NAME = 'vengateshbabu1605/wifi-pytest-advanced'


        // ============================================================
        // GitOps
        // ============================================================

        GITOPS_REPO = 'https://github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git'

        GITOPS_CREDENTIALS = 'github-gitops-creds'
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
                    echo ===== Select Kind Context =====

                    kubectl config use-context kind-kind

                    if errorlevel 1 (
                        echo ERROR: Unable to select kind-kind context.
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

                    "%KIND_EXE%" get nodes --name "kind"

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
                    echo %IMAGE_NAME%:%BUILD_NUMBER%

                    echo.
                    echo ===== Docker Build =====

                    docker build ^
                        -t %IMAGE_NAME%:%BUILD_NUMBER% ^
                        .

                    if errorlevel 1 (
                        echo ERROR: Docker image build failed.
                        exit /b 1
                    )


                    echo.
                    echo ===== Docker Image Created =====

                    docker images %IMAGE_NAME%


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

                dir('gitops-repo') {

                    deleteDir()

                    bat '''
                        echo ===== Clone GitOps Repository =====

                        git clone "%GITOPS_REPO%" .

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
                echo ===== Git Branch =====

                git branch


                echo.
                echo ===== Local HEAD =====

                git rev-parse HEAD


                echo.
                echo ===== Origin Main =====

                git rev-parse refs/remotes/origin/main


                echo.
                echo ===== Latest Commit =====

                git log -1 --oneline


                echo.
                echo ===== Git Status =====

                git status --short


                echo.
                echo ==========================================
                echo GitOps Repository Verification Successful
                echo ==========================================
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

                        powershell -NoProfile -Command "(Get-Content 'k8s\\pytest-job.yaml') -replace 'image: vengateshbabu1605/wifi-pytest-advanced:[^ ]+', 'image: vengateshbabu1605/wifi-pytest-advanced:%BUILD_NUMBER%' | Set-Content 'k8s\\pytest-job.yaml'"

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
                                rem Create a simple Git AskPass helper.
                                rem Username is embedded in the GitHub URL.
                                rem Git therefore only needs the password/token.
                                rem ------------------------------------------------

                                > git-askpass.cmd echo @echo off
                                >> git-askpass.cmd echo echo %%GIT_PASSWORD%%


                                set "GIT_ASKPASS=%CD%\\git-askpass.cmd"
                                set "GIT_TERMINAL_PROMPT=0"


                                echo AskPass helper created.


                                echo.
                                echo ===== Configure GitHub Remote =====

                                git remote set-url origin https://%GIT_USERNAME%@github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git


                                echo.
                                echo ===== Git Remote After Authentication Setup =====

                                git remote -v


                                echo.
                                echo ===== Git Push =====

                                git push origin main

                                if errorlevel 1 (
                                    echo ERROR: Git push failed.
                                    exit /b 1
                                )


                                echo.
                                echo ===== Git Push Successful =====


                                echo.
                                echo ===== Verify Remote Commit =====

                                git ls-remote origin refs/heads/main

                                if errorlevel 1 (
                                    echo ERROR: Remote verification failed.
                                    exit /b 1
                                )


                                echo.
                                echo GitOps push completed successfully.


                                echo.
                                echo ===== Remove AskPass Helper =====

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

                    docker images %IMAGE_NAME%:%BUILD_NUMBER%


                    echo.
                    echo ===== Loading Image into Kind =====

                    "%KIND_EXE%" load docker-image ^
                        %IMAGE_NAME%:%BUILD_NUMBER% ^
                        --name kind

                    if errorlevel 1 (
                        echo ERROR: Failed to load Docker image into Kind.
                        exit /b 1
                    )


                    echo.
                    echo ===== Verify Kind Node =====

                    kubectl get nodes -o wide


                    echo.
                    echo ==========================================
                    echo Docker Image Loaded Into Kind Successfully
                    echo ==========================================
                '''
            }
        }


        // ============================================================
        // 10. PREPARE KUBERNETES JOB
        // ============================================================

        stage('Prepare Kubernetes Job') {

            steps {

                dir('gitops-repo') {

                    bat '''
                        echo ==========================================
                        echo Preparing Kubernetes Job
                        echo ==========================================

                        set "JOB_NAME=wifi-pytest-job-%BUILD_NUMBER%"


                        echo.
                        echo ===== Expected Job Name =====

                        echo %JOB_NAME%


                        echo.
                        echo ===== Delete Existing Job With Same Name =====

                        kubectl delete job "%JOB_NAME%" ^
                            -n default ^
                            --ignore-not-found=true


                        echo.
                        echo ===== Create Runtime Manifest =====

                        powershell -NoProfile -ExecutionPolicy Bypass -Command "$path='k8s\\pytest-job.yaml'; $out='k8s\\pytest-job-runtime.yaml'; $c=Get-Content $path -Raw; $c=[regex]::Replace($c,'(?m)^([ \\t]*)generateName:[^\\r\\n]*\\r?\\n','$1name: wifi-pytest-job-%BUILD_NUMBER%'); $c=[regex]::Replace($c,'(?m)^([ \\t]*)name:[ \\t]*wifi-pytest-job(?:-[^ \\t\\r\\n]+)?[ \\t]*$','$1name: wifi-pytest-job-%BUILD_NUMBER%'); if ($c -notmatch '(?m)^metadata:\\r?\\n[ \\t]+name:') { $c=[regex]::Replace($c,'(?m)^metadata:[ \\t]*$',"metadata:`r`n  name: wifi-pytest-job-%BUILD_NUMBER%") }; $c=[regex]::Replace($c,'(?m)^([ \\t]*imagePullPolicy:[ \\t]*).*$','$1Never'); Set-Content -Path $out -Value $c -Encoding UTF8"


                        if errorlevel 1 (
                            echo ERROR: Failed to create runtime Kubernetes manifest.
                            exit /b 1
                        )


                        echo.
                        echo ===== Runtime Manifest =====

                        findstr /N /C:"name:" /C:"generateName:" /C:"image:" /C:"imagePullPolicy:" k8s\\pytest-job-runtime.yaml


                        echo.
                        echo ===== Apply Kubernetes Job =====

                        kubectl apply -f k8s\\pytest-job-runtime.yaml

                        if errorlevel 1 (
                            echo ERROR: Kubernetes Job creation failed.
                            exit /b 1
                        )


                        echo.
                        echo ===== Verify Exact Job =====

                        kubectl get job "%JOB_NAME%" -n default

                        if errorlevel 1 (
                            echo ERROR: Expected Kubernetes Job was not created.
                            echo Expected Job: %JOB_NAME%

                            echo.
                            echo ===== Existing Jobs =====

                            kubectl get jobs -n default

                            exit /b 1
                        )


                        echo.
                        echo ==========================================
                        echo Kubernetes Job Prepared Successfully
                        echo ==========================================
                    '''
                }
            }
        }


        // ============================================================
        // 11. RUN PYTEST IN KUBERNETES
        // ============================================================

        stage('Run Pytest in Kubernetes') {

            steps {

                dir('gitops-repo') {

                    catchError(
                        buildResult: 'FAILURE',
                        stageResult: 'FAILURE'
                    ) {

                        bat '''
                            set "JOB_NAME=wifi-pytest-job-%BUILD_NUMBER%"


                            echo ==========================================
                            echo Running Pytest Kubernetes Job
                            echo ==========================================


                            echo.
                            echo ===== Kubernetes Job =====

                            kubectl get job "%JOB_NAME%" -n default


                            echo.
                            echo ===== Kubernetes Pod =====

                            kubectl get pods ^
                                -n default ^
                                -l job-name=%JOB_NAME% ^
                                -o wide


                            echo.
                            echo ===== Wait For Job Completion =====

                            kubectl wait ^
                                --for=condition=complete ^
                                job/"%JOB_NAME%" ^
                                -n default ^
                                --timeout=10m


                            if errorlevel 1 (

                                echo.
                                echo ==========================================
                                echo Kubernetes Pytest Job FAILED
                                echo ==========================================


                                echo.
                                echo ===== Job Description =====

                                kubectl describe job "%JOB_NAME%" -n default


                                echo.
                                echo ===== Pod Status =====

                                kubectl get pods ^
                                    -n default ^
                                    -l job-name=%JOB_NAME% ^
                                    -o wide


                                echo.
                                echo ===== Pod Logs =====

                                kubectl logs ^
                                    job/"%JOB_NAME%" ^
                                    -n default ^
                                    --all-containers=true


                                exit /b 1
                            )


                            echo.
                            echo ===== Kubernetes Pytest Logs =====

                            kubectl logs ^
                                job/"%JOB_NAME%" ^
                                -n default ^
                                --all-containers=true


                            echo.
                            echo ==========================================
                            echo Kubernetes Pytest Job Completed Successfully
                            echo ==========================================
                        '''
                    }
                }
            }
        }


        // ============================================================
        // 12. CREATE REPORTS READER
        // ============================================================

        stage('Create Reports Reader') {

            steps {

                dir('gitops-repo') {

                    bat '''
                        echo ==========================================
                        echo Preparing Kubernetes Report Collection
                        echo ==========================================


                        if not exist reports mkdir reports

                        if not exist reports\\kubernetes mkdir reports\\kubernetes


                        set "JOB_NAME=wifi-pytest-job-%BUILD_NUMBER%"


                        echo.
                        echo ===== Find Kubernetes Test Pod =====


                        for /f "delims=" %%P in ('kubectl get pods -n default -l job-name=%JOB_NAME% -o jsonpath="{.items[0].metadata.name}"') do set "POD_NAME=%%P"


                        if not defined POD_NAME (

                            echo ERROR: Kubernetes test pod was not found.

                            kubectl get pods -n default

                            exit /b 1
                        )


                        echo.
                        echo Kubernetes Test Pod:
                        echo %POD_NAME%


                        echo %POD_NAME% > reports\\kubernetes\\pod-name.txt


                        echo.
                        echo Report collection preparation completed.
                    '''
                }
            }
        }


        // ============================================================
        // 13. COLLECT KUBERNETES REPORTS
        // ============================================================

        stage('Collect Kubernetes Reports') {

            steps {

                dir('gitops-repo') {

                    bat '''
                        echo ==========================================
                        echo Collecting Kubernetes Test Reports
                        echo ==========================================


                        set /p POD_NAME=<reports\\kubernetes\\pod-name.txt


                        echo.
                        echo ===== Kubernetes Pod =====

                        echo %POD_NAME%


                        echo.
                        echo ===== Collect Pytest Console Log =====

                        kubectl logs ^
                            "%POD_NAME%" ^
                            -n default ^
                            > reports\\kubernetes\\pytest.log 2>&1


                        echo.
                        echo ===== Copy Pytest Reports From Pod =====

                        kubectl cp ^
                            "%POD_NAME%:/app/reports/." ^
                            "reports\\kubernetes"


                        if errorlevel 1 (

                            echo WARNING: kubectl cp could not copy /app/reports.

                            echo Checking pod filesystem...

                            kubectl exec ^
                                "%POD_NAME%" ^
                                -n default ^
                                -- ls -la /app/reports


                            echo.
                            echo Report copy failed.

                            exit /b 1
                        )


                        echo.
                        echo ===== Collected Reports =====

                        dir /s /b reports


                        echo.
                        echo ==========================================
                        echo Kubernetes Reports Collected
                        echo ==========================================
                    '''
                }
            }
        }


        // ============================================================
        // 14. VERIFY REPORTS
        // ============================================================

        stage('Verify Reports') {

            steps {

                dir('gitops-repo') {

                    bat '''
                        echo ==========================================
                        echo Verifying Test Reports
                        echo ==========================================


                        echo.
                        echo ===== Report Files =====

                        dir /s /b reports


                        echo.
                        echo ===== Verify JUnit XML =====


                        if exist reports\\kubernetes\\junit-results.xml (

                            echo JUnit XML found:
                            echo reports\\kubernetes\\junit-results.xml

                        ) else (

                            echo ERROR: JUnit XML report was not found.

                            echo.
                            echo Available files:

                            dir /s /b reports

                            exit /b 1
                        )


                        echo.
                        echo ===== Verify HTML Report =====


                        if exist reports\\kubernetes\\wlan_test_report.html (

                            echo HTML report found:
                            echo reports\\kubernetes\\wlan_test_report.html

                        ) else (

                            echo WARNING: HTML report was not found.
                            echo JUnit report is available.
                        )


                        echo.
                        echo ==========================================
                        echo Test Report Verification Completed
                        echo ==========================================
                    '''
                }
            }
        }
    }


    // ================================================================
    // POST ACTIONS
    // ================================================================

    post {

        always {

            script {

                echo '=========================================='
                echo 'Pipeline Post Actions'
                echo '=========================================='


                // ----------------------------------------------------
                // Publish JUnit
                // ----------------------------------------------------

                junit(
                    testResults: 'gitops-repo/reports/**/junit-results.xml',
                    allowEmptyResults: true
                )


                // ----------------------------------------------------
                // Archive Reports
                // ----------------------------------------------------

                archiveArtifacts(
                    artifacts: 'gitops-repo/reports/**/*',
                    allowEmptyArchive: true
                )


                // ----------------------------------------------------
                // Kubernetes Diagnostics + Cleanup
                //
                // IMPORTANT:
                // returnStatus:true prevents cleanup failures from
                // changing an already-established build result.
                // ----------------------------------------------------

                echo '=========================================='
                echo 'Kubernetes Diagnostics / Cleanup'
                echo '=========================================='


                bat(
                    returnStatus: true,
                    script: '''
                        echo ===== Kubernetes Jobs =====

                        kubectl get jobs -A ^
                            || echo WARNING: Unable to query Kubernetes jobs.


                        echo.
                        echo ===== Kubernetes Pods =====

                        kubectl get pods -A ^
                            || echo WARNING: Unable to query Kubernetes pods.


                        echo.
                        echo ===== Current Build Job =====

                        kubectl get job ^
                            wifi-pytest-job-%BUILD_NUMBER% ^
                            -n default ^
                            || echo WARNING: Current build job not found.


                        echo.
                        echo ===== Current Build Pod =====

                        kubectl get pods ^
                            -n default ^
                            -l job-name=wifi-pytest-job-%BUILD_NUMBER% ^
                            -o wide ^
                            || echo WARNING: Current build pod not found.


                        echo.
                        echo ===== Workspace Cleanup =====


                        if exist gitops-repo\\git-askpass.cmd (
                            del /q gitops-repo\\git-askpass.cmd
                        )


                        if exist gitops-repo\\k8s\\pytest-job-runtime.yaml (
                            del /q gitops-repo\\k8s\\pytest-job-runtime.yaml
                        )


                        echo.
                        echo ===== Delete Current Kubernetes Job =====

                        kubectl delete job ^
                            wifi-pytest-job-%BUILD_NUMBER% ^
                            -n default ^
                            --ignore-not-found=true ^
                            || echo WARNING: Kubernetes cleanup failed.


                        echo.
                        echo Cleanup completed.
                    '''
                )
            }
        }


        success {

            echo '=========================================='
            echo 'PIPELINE SUCCESSFUL'
            echo '=========================================='

            echo "Build Number: ${env.BUILD_NUMBER}"

            echo 'Pytest Docker image built.'

            echo 'GitOps repository updated and pushed.'

            echo 'Docker image loaded into Kind.'

            echo 'Kubernetes Pytest Job completed.'

            echo 'JUnit/HTML reports collected.'
        }


        failure {

            echo '=========================================='
            echo 'PIPELINE FAILED'
            echo '=========================================='

            echo "Build Number: ${env.BUILD_NUMBER}"

            echo 'Check the failed stage above.'

            echo 'Kubernetes diagnostics and available reports were collected where possible.'
        }
    }
}