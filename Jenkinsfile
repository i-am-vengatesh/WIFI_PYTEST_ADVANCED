pipeline {

    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {

    DOCKER_IMAGE     = 'wifi-pytest-advanced'
    DOCKER_HUB_IMAGE = 'vengateshbabu1605/wifi-pytest-advanced'

    KIND_CLUSTER  = 'kind'
    K8S_NAMESPACE = 'default'

    KIND_EXE = 'C:\\Users\\USER\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe\\kind.exe'

    KUBECTL_EXE = 'C:\\Program Files\\Docker\\Docker\\resources\\bin\\kubectl.exe'
    DOCKER_EXE  = 'C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe'

    // Jenkins-specific Kubernetes configuration
    KUBECONFIG = 'C:\\ProgramData\\Jenkins\\.kube\\config'

    GITOPS_REPO        = 'https://github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git'
    GITOPS_CREDENTIALS = 'github-gitops-creds'

    K8S_JOB_NAME = "wifi-pytest-job-${BUILD_NUMBER}"

    HTML_REPORT  = 'reports\\wlan_test_report.html'
    JUNIT_REPORT = 'reports\\junit-results.xml'
}

    stages {

        // ============================================================
        // 1. Clean Workspace
        // ============================================================
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        // ============================================================
        // 2. Checkout Pytest Project
        // ============================================================
        stage('Checkout') {
            steps {
                checkout scm

                bat '''
                    echo.
                    echo ==========================================
                    echo Pytest Project Checkout
                    echo ==========================================
                    git --version
                    git rev-parse --short HEAD
                    git log -1 --oneline
                '''
            }
        }

        // ============================================================
        // 3. Test GitOps Repository Access
        // ============================================================
        stage('Test GitOps Repository Access') {
            steps {

                dir('gitops-test') {

                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            url: "${GITOPS_REPO}",
                            credentialsId: "${GITOPS_CREDENTIALS}"
                        ]]
                    ])

                    bat '''
                        echo.
                        echo ==========================================
                        echo GitOps Repository Access Successful
                        echo ==========================================
                        git log -1 --oneline
                    '''
                }
            }
        }

        // ============================================================
        // 4. Verify Environment / Kubernetes
        // ============================================================
        stage('Verify Environment') {
            steps {

                bat '''
                    echo.
                    echo ==========================================
                    echo Jenkins User
                    echo ==========================================
                    whoami

                    echo.
                    echo ==========================================
                    echo Docker Version
                    echo ==========================================
                    "%DOCKER_EXE%" --version

                    echo.
                    echo ==========================================
                    echo Kubectl Version
                    echo ==========================================
                    "%KUBECTL_EXE%" version --client

                    echo.
                    echo ==========================================
                    echo Kind Version
                    echo ==========================================
                    "%KIND_EXE%" version

                    echo.
                    echo ==========================================
                    echo Kubernetes Context
                    echo ==========================================
                    "%KUBECTL_EXE%" config current-context

                    echo.
                    echo ==========================================
                    echo Kubernetes Nodes
                    echo ==========================================
                    "%KUBECTL_EXE%" get nodes -o wide

                    echo.
                    echo ==========================================
                    echo Kubernetes Namespaces
                    echo ==========================================
                    "%KUBECTL_EXE%" get namespaces
                '''
            }
        }

        // ============================================================
        // 5. Build Docker Image
        // ============================================================
        stage('Build Docker Image') {
            steps {

                bat '''
                    echo.
                    echo ==========================================
                    echo Building Docker Image
                    echo ==========================================

                    "%DOCKER_EXE%" build ^
                        -t %DOCKER_IMAGE%:%BUILD_NUMBER% ^
                        -t %DOCKER_HUB_IMAGE%:%BUILD_NUMBER% ^
                        .
                '''
            }
        }

        // ============================================================
        // 6. Push Docker Image
        // ============================================================
        stage('Push Docker Image') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {

                    bat '''
                        echo.
                        echo ==========================================
                        echo Docker Hub Login
                        echo ==========================================

                        echo %DOCKER_PASSWORD% | "%DOCKER_EXE%" login ^
                            -u "%DOCKER_USERNAME%" ^
                            --password-stdin

                        echo.
                        echo ==========================================
                        echo Pushing Docker Image
                        echo ==========================================

                        "%DOCKER_EXE%" push ^
                            %DOCKER_HUB_IMAGE%:%BUILD_NUMBER%

                        echo.
                        echo ==========================================
                        echo Docker Logout
                        echo ==========================================

                        "%DOCKER_EXE%" logout
                    '''
                }
            }
        }

        // ============================================================
        // 7. Update GitOps Repository
        // ============================================================
        stage('Update GitOps Repository') {
            steps {

                dir('gitops-repo') {

                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            url: "${GITOPS_REPO}",
                            credentialsId: "${GITOPS_CREDENTIALS}"
                        ]]
                    ])

                    bat '''
                        echo.
                        echo ==========================================
                        echo GitOps Repository Before Update
                        echo ==========================================
                        git log -1 --oneline

                        echo.
                        echo ==========================================
                        echo Updating Kubernetes Manifest
                        echo ==========================================

                        powershell -NoProfile -ExecutionPolicy Bypass -Command ^
                        "(Get-Content 'k8s\\pytest-job.yaml') ^
                        -replace 'wifi-pytest-job-[0-9]+', 'wifi-pytest-job-%BUILD_NUMBER%' ^
                        -replace 'vengateshbabu1605/wifi-pytest-advanced:[0-9]+', 'vengateshbabu1605/wifi-pytest-advanced:%BUILD_NUMBER%' ^
                        | Set-Content 'k8s\\pytest-job.yaml'"

                        echo.
                        echo ==========================================
                        echo Updated Manifest
                        echo ==========================================

                        type k8s\\pytest-job.yaml

                        echo.
                        echo ==========================================
                        echo Git Commit
                        echo ==========================================

                        git config user.name "Jenkins CI"
                        git config user.email "jenkins@localhost"

                        git add k8s\\pytest-job.yaml

                        git commit -m "Update Pytest image to build %BUILD_NUMBER%"
                    '''

                    // ------------------------------------------------
                    // IMPORTANT:
                    // Do NOT use:
                    //
                    // git push https://username:password@github.com/...
                    //
                    // Use GIT_ASKPASS so the PAT is not placed
                    // directly in the Git command.
                    // ------------------------------------------------

                    withCredentials([
                        usernamePassword(
                            credentialsId: "${GITOPS_CREDENTIALS}",
                            usernameVariable: 'GIT_USERNAME',
                            passwordVariable: 'GIT_PASSWORD'
                        )
                    ]) {

                        bat '''
                            echo.
                            echo ==========================================
                            echo Pushing GitOps Changes
                            echo ==========================================

                            set "GIT_ASKPASS=%WORKSPACE%\\git-askpass.bat"

                            (
                                echo @echo off
                                echo echo %%~1 ^| findstr /I "Username" ^>nul
                                echo if not errorlevel 1 ^(
                                echo     echo %%GIT_USERNAME%%
                                echo     exit /b 0
                                echo ^)
                                echo echo %%GIT_PASSWORD%%
                            ) > "%GIT_ASKPASS%"

                            git push origin HEAD:main

                            set "PUSH_RESULT=%ERRORLEVEL%"

                            del "%GIT_ASKPASS%" >nul 2>&1

                            if not "%PUSH_RESULT%"=="0" (
                                echo.
                                echo ==========================================
                                echo GitOps Push FAILED
                                echo ==========================================
                                exit /b %PUSH_RESULT%
                            )

                            echo.
                            echo ==========================================
                            echo GitOps Push Successful
                            echo ==========================================
                        '''
                    }
                }
            }
        }

        // ============================================================
        // 8. Load Docker Image into Kind
        // ============================================================
        stage('Load Docker Image into Kind') {
            steps {

                bat '''
                    echo.
                    echo ==========================================
                    echo Loading Docker Image into Kind
                    echo ==========================================

                    "%KIND_EXE%" load docker-image ^
                        %DOCKER_HUB_IMAGE%:%BUILD_NUMBER% ^
                        --name %KIND_CLUSTER%
                '''
            }
        }

        // ============================================================
        // 9. Prepare Kubernetes Job
        // ============================================================
        stage('Prepare Kubernetes Job') {
            steps {

                bat '''
                    echo.
                    echo ==========================================
                    echo Preparing Kubernetes Job
                    echo ==========================================

                    "%KUBECTL_EXE%" delete job %K8S_JOB_NAME% ^
                        -n %K8S_NAMESPACE% ^
                        --ignore-not-found=true

                    echo.
                    echo Applying GitOps Manifest
                    echo ==========================================

                    "%KUBECTL_EXE%" apply ^
                        -f gitops-repo\\k8s\\pytest-job.yaml ^
                        -n %K8S_NAMESPACE%

                    echo.
                    echo Kubernetes Jobs
                    echo ==========================================

                    "%KUBECTL_EXE%" get jobs ^
                        -n %K8S_NAMESPACE%
                '''
            }
        }

        // ============================================================
        // 10. Run Pytest in Kubernetes
        // ============================================================
        stage('Run Pytest in Kubernetes') {
            steps {

                bat '''
                    echo.
                    echo ==========================================
                    echo Waiting for Kubernetes Job
                    echo ==========================================

                    "%KUBECTL_EXE%" wait ^
                        --for=condition=complete ^
                        job/%K8S_JOB_NAME% ^
                        -n %K8S_NAMESPACE% ^
                        --timeout=10m

                    echo.
                    echo ==========================================
                    echo Kubernetes Job Status
                    echo ==========================================

                    "%KUBECTL_EXE%" get job %K8S_JOB_NAME% ^
                        -n %K8S_NAMESPACE%

                    echo.
                    echo ==========================================
                    echo Pod Status
                    echo ==========================================

                    "%KUBECTL_EXE%" get pods ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=%K8S_JOB_NAME%

                    echo.
                    echo ==========================================
                    echo Pytest Logs
                    echo ==========================================

                    "%KUBECTL_EXE%" logs ^
                        job/%K8S_JOB_NAME% ^
                        -n %K8S_NAMESPACE%
                '''
            }
        }

        // ============================================================
        // 11. Collect Kubernetes Reports
        // ============================================================
        stage('Collect Kubernetes Reports') {
            steps {

                bat '''
                    echo.
                    echo ==========================================
                    echo Finding Completed Pod
                    echo ==========================================

                    "%KUBECTL_EXE%" get pods ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=%K8S_JOB_NAME% ^
                        -o wide

                    echo.
                    echo ==========================================
                    echo Getting Pod Name
                    echo ==========================================

                    for /f "tokens=1" %%P in ('"%KUBECTL_EXE%" get pods -n %K8S_NAMESPACE% -l job-name=%K8S_JOB_NAME% -o jsonpath="{.items[0].metadata.name}"') do (
                        set "POD_NAME=%%P"
                    )

                    echo POD_NAME=%POD_NAME%

                    echo.
                    echo ==========================================
                    echo Creating Reports Directory
                    echo ==========================================

                    if not exist reports mkdir reports

                    echo.
                    echo ==========================================
                    echo Copying JUnit XML
                    echo ==========================================

                    "%KUBECTL_EXE%" cp ^
                        %K8S_NAMESPACE%/%POD_NAME%:/app/reports/junit-results.xml ^
                        reports\\junit-results.xml

                    echo.
                    echo ==========================================
                    echo Copying HTML Report
                    echo ==========================================

                    "%KUBECTL_EXE%" cp ^
                        %K8S_NAMESPACE%/%POD_NAME%:/app/reports/wlan_test_report.html ^
                        reports\\wlan_test_report.html
                '''
            }
        }

        // ============================================================
        // 12. Verify Reports
        // ============================================================
        stage('Verify Reports') {
            steps {

                bat '''
                    echo.
                    echo ==========================================
                    echo Report Files
                    echo ==========================================

                    dir reports

                    echo.
                    echo ==========================================
                    echo JUnit XML
                    echo ==========================================

                    if exist reports\\junit-results.xml (
                        echo JUnit report found
                    ) else (
                        echo ERROR: JUnit report not found
                        exit /b 1
                    )

                    echo.
                    echo ==========================================
                    echo HTML Report
                    echo ==========================================

                    if exist reports\\wlan_test_report.html (
                        echo HTML report found
                    ) else (
                        echo ERROR: HTML report not found
                        exit /b 1
                    )
                '''
            }
        }
    }

    // ================================================================
    // POST ACTIONS
    // ================================================================
    post {

        always {

            script {

                if (fileExists('reports/junit-results.xml')) {

                    junit(
                        testResults: 'reports/junit-results.xml',
                        allowEmptyResults: false
                    )

                } else {

                    echo 'JUnit report not available.'
                }
            }

            archiveArtifacts(
                artifacts: 'reports/*.html,reports/*.xml',
                allowEmptyArchive: true
            )
        }

        success {
            echo '''
            ==========================================
            PIPELINE SUCCESS
            ==========================================
            Pytest completed successfully.
            Docker image pushed.
            GitOps repository updated.
            Kubernetes Job completed.
            Reports collected.
            ==========================================
            '''
        }

        failure {
            echo '''
            ==========================================
            PIPELINE FAILED
            ==========================================
            Check the failed stage and Jenkins console log.
            ==========================================
            '''
        }

        aborted {
            echo '''
            ==========================================
            PIPELINE ABORTED
            ==========================================
            '''
        }

        cleanup {
            cleanWs()
        }
    }
}