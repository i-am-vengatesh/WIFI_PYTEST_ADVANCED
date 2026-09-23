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

        // ============================================================
        // Python
        // ============================================================
        PYTHON = 'C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'


        // ============================================================
        // Docker
        // Jenkins runs as NT AUTHORITY\SYSTEM, so use explicit path
        // ============================================================
        DOCKER_EXE = 'C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe'


        DOCKER_IMAGE = 'wifi-pytest-advanced'
        DOCKER_HUB_IMAGE = 'vengateshbabu1605/wifi-pytest-advanced'


        // ============================================================
        // Kubernetes
        // ============================================================
        KUBECTL_EXE = 'C:\\Program Files\\Docker\\Docker\\resources\\bin\\kubectl.exe'


        // ============================================================
        // Kind
        // ============================================================
        KIND_EXE = 'C:\\Users\\USER\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe\\kind.exe'

        KIND_CLUSTER = 'kind'


        // ============================================================
        // Kubernetes namespace
        // ============================================================
        K8S_NAMESPACE = 'default'


        // ============================================================
        // GitOps
        // ============================================================
        GITOPS_REPO = 'https://github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git'
        GITOPS_CREDENTIALS = 'github-gitops-creds'


        // ============================================================
        // Reports
        // ============================================================
        HTML_REPORT = 'reports\\wlan_test_report.html'
        JUNIT_REPORT = 'reports\\junit-results.xml'


        // ============================================================
        // Kubernetes Job
        // ============================================================
        K8S_JOB_NAME = "wifi-pytest-job-${BUILD_NUMBER}"
    }


    stages {


        // ============================================================
        // 1. CLEAN WORKSPACE
        // ============================================================
        stage('Clean Workspace') {

            steps {

                echo '===== Cleaning Jenkins Workspace ====='

                deleteDir()

                echo '===== Workspace Cleaned ====='
            }
        }



        // ============================================================
        // 2. CHECKOUT PYTEST PROJECT
        // ============================================================
        stage('Checkout') {

            steps {

                echo '===== Checking Out WIFI_PYTEST_ADVANCED ====='

                checkout scm

                echo '===== Checkout Complete ====='

                bat '''
                    echo.
                    echo ===== Git Information =====

                    git log -1 --oneline

                    echo.
                    git branch

                    echo.
                '''
            }
        }



        // ============================================================
        // 3. TEST GITOPS REPOSITORY ACCESS
        // ============================================================
        stage('Test GitOps Repository Access') {

            steps {

                echo '===== Testing GitOps Repository Access ====='


                dir('gitops-access-test') {

                    git(
                        branch: 'main',
                        credentialsId: 'github-gitops-creds',
                        url: 'https://github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git'
                    )


                    bat '''
                        echo.
                        echo ===== GitOps Repository Access Successful =====

                        git log -1 --oneline

                        echo.
                    '''
                }


                echo '===== GitOps Repository Access Test Complete ====='
            }
        }



        // ============================================================
        // 4. VERIFY KUBERNETES
        // ============================================================
        stage('Verify Kubernetes') {

            steps {

                echo '===== Verifying Kubernetes / Kind ====='


                bat '''
                    echo.
                    echo ============================================================
                    echo                 JENKINS ENVIRONMENT
                    echo ============================================================


                    echo.
                    echo ===== Jenkins User =====

                    whoami


                    echo.
                    echo ===== KUBECONFIG =====

                    echo %KUBECONFIG%


                    echo.
                    echo ============================================================
                    echo                 PYTHON
                    echo ============================================================


                    "%PYTHON%" --version


                    echo.
                    echo ============================================================
                    echo                 DOCKER
                    echo ============================================================


                    "%DOCKER_EXE%" version


                    echo.
                    echo ============================================================
                    echo                 KUBECTL
                    echo ============================================================


                    "%KUBECTL_EXE%" version --client


                    echo.
                    echo ============================================================
                    echo                 KUBERNETES CONTEXT
                    echo ============================================================


                    "%KUBECTL_EXE%" config current-context


                    echo.
                    echo ============================================================
                    echo                 KUBERNETES NODES
                    echo ============================================================


                    "%KUBECTL_EXE%" get nodes -o wide


                    echo.
                    echo ============================================================
                    echo                 KUBERNETES NAMESPACES
                    echo ============================================================


                    "%KUBECTL_EXE%" get namespaces


                    echo.
                    echo ============================================================
                    echo                 KIND
                    echo ============================================================


                    "%KIND_EXE%" version


                    echo.
                '''


                echo '===== Kubernetes Verification Complete ====='
            }
        }



        // ============================================================
        // 5. BUILD DOCKER IMAGE
        // ============================================================
        stage('Build Docker Image') {

            steps {

                echo '===== Building Docker Image ====='


                bat '''
                    echo.
                    echo ===== Docker Version =====

                    "%DOCKER_EXE%" version


                    echo.
                    echo ===== Building Image =====


                    "%DOCKER_EXE%" build ^
                    -t %DOCKER_IMAGE%:%BUILD_NUMBER% .


                    if errorlevel 1 (
                        echo.
                        echo ===== Docker Build FAILED =====
                        exit /b 1
                    )


                    echo.
                    echo ===== Docker Image Created =====


                    "%DOCKER_EXE%" images %DOCKER_IMAGE%


                    echo.
                '''


                echo '===== Docker Build Complete ====='
            }
        }



        // ============================================================
        // 6. PUSH DOCKER IMAGE TO DOCKER HUB
        // ============================================================
        stage('Push Docker Image') {

            steps {

                echo '===== Pushing Docker Image to Docker Hub ====='


                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {


                    bat '''
                        echo.
                        echo ===== Tagging Docker Image =====


                        "%DOCKER_EXE%" tag ^
                        %DOCKER_IMAGE%:%BUILD_NUMBER% ^
                        %DOCKER_HUB_IMAGE%:%BUILD_NUMBER%


                        echo.
                        echo ===== Docker Hub Image =====

                        echo %DOCKER_HUB_IMAGE%:%BUILD_NUMBER%


                        echo.
                        echo ===== Logging Into Docker Hub =====


                        echo %DOCKER_PASSWORD% | "%DOCKER_EXE%" login ^
                        -u %DOCKER_USERNAME% ^
                        --password-stdin


                        if errorlevel 1 (
                            echo.
                            echo ===== Docker Login FAILED =====
                            exit /b 1
                        )


                        echo.
                        echo ===== Pushing Docker Image =====


                        "%DOCKER_EXE%" push ^
                        %DOCKER_HUB_IMAGE%:%BUILD_NUMBER%


                        if errorlevel 1 (
                            echo.
                            echo ===== Docker Push FAILED =====

                            "%DOCKER_EXE%" logout

                            exit /b 1
                        )


                        echo.
                        echo ===== Docker Image Push Complete =====


                        echo.
                        echo ===== Docker Image =====

                        echo %DOCKER_HUB_IMAGE%:%BUILD_NUMBER%


                        echo.
                        echo ===== Docker Logout =====

                        "%DOCKER_EXE%" logout


                        echo.
                    '''
                }


                echo '===== Docker Hub Push Complete ====='
            }
        }



        // ============================================================
        // 7. UPDATE GITOPS REPOSITORY
        // ============================================================
        stage('Update GitOps Repository') {

            steps {

                echo '===== Updating GitOps Repository ====='


                dir('gitops-repo') {


                    // ------------------------------------------------
                    // Clone GitOps Repository
                    // ------------------------------------------------
                    git(
                        branch: 'main',
                        credentialsId: 'github-gitops-creds',
                        url: 'https://github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git'
                    )


                    bat '''
                        echo.
                        echo ===== GitOps Repository Before Update =====

                        git log -1 --oneline


                        echo.
                        echo ===== Current Kubernetes Manifest =====

                        type k8s\\pytest-job.yaml


                        echo.
                        echo ===== Updating Job Name =====


                        powershell -Command "(Get-Content k8s\\pytest-job.yaml) -replace 'name: wifi-pytest-job-[0-9]+', 'name: wifi-pytest-job-%BUILD_NUMBER%' | Set-Content k8s\\pytest-job.yaml"


                        echo.
                        echo ===== Updating Docker Hub Image =====


                        powershell -Command "(Get-Content k8s\\pytest-job.yaml) -replace 'image: [^ ]*wifi-pytest-advanced:[0-9]+', 'image: %DOCKER_HUB_IMAGE%:%BUILD_NUMBER%' | Set-Content k8s\\pytest-job.yaml"


                        echo.
                        echo ===== Updated Kubernetes Manifest =====

                        type k8s\\pytest-job.yaml


                        echo.
                        echo ===== Git Status =====

                        git status


                        echo.
                    '''


                    // ------------------------------------------------
                    // Git Configuration
                    // ------------------------------------------------
                    bat '''

                        echo.
                        echo ===== Configuring Git =====

                        git config user.name "Jenkins CI"

                        git config user.email "jenkins@localhost"

                        echo.

                    '''


                    // ------------------------------------------------
                    // Commit
                    // ------------------------------------------------
                    bat '''

                        echo.
                        echo ===== Committing GitOps Change =====

                        git add k8s\\pytest-job.yaml

                        git commit -m "Update Pytest image to build %BUILD_NUMBER%"

                        if errorlevel 1 (
                            echo.
                            echo ===== Git Commit FAILED =====
                            exit /b 1
                        )

                        echo.
                        echo ===== Commit Created =====

                        git log -1 --oneline

                        echo.

                    '''


                    // ------------------------------------------------
                    // Push
                    // ------------------------------------------------
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'github-gitops-creds',
                            usernameVariable: 'GIT_USERNAME',
                            passwordVariable: 'GIT_PASSWORD'
                        )
                    ]) {


                        timeout(time: 2, unit: 'MINUTES') {

                            bat '''

                                echo.
                                echo ============================================================
                                echo                    GITOPS PUSH
                                echo ============================================================


                                echo.
                                echo ===== Current Remote =====

                                git remote -v


                                echo.
                                echo ===== Pushing GitOps Commit =====


                                git push ^
                                https://%GIT_USERNAME%:%GIT_PASSWORD%@github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git ^
                                HEAD:main


                                if errorlevel 1 (
                                    echo.
                                    echo ===== GitOps Push FAILED =====
                                    exit /b 1
                                )


                                echo.
                                echo ===== GitOps Push Successful =====


                                echo.
                                echo ===== Latest GitOps Commit =====

                                git log -1 --oneline


                                echo.

                            '''
                        }
                    }


                    // ------------------------------------------------
                    // Restore Remote
                    // ------------------------------------------------
                    bat '''

                        echo.
                        echo ===== Restoring Clean Git Remote =====

                        git remote set-url origin https://github.com/i-am-vengatesh/WIFI_PYTEST_GITOPS.git


                        echo.
                        echo ===== Remote After Cleanup =====

                        git remote -v


                        echo.

                    '''
                }


                echo '===== GitOps Repository Update Complete ====='
            }
        }



        // ============================================================
        // 8. LOAD DOCKER IMAGE INTO KIND
        // ============================================================
        stage('Load Docker Image into Kind') {

            steps {

                echo '===== Loading Docker Image into Kind ====='


                bat '''

                    echo.
                    echo ===== Loading Docker Hub Tagged Image =====


                    "%KIND_EXE%" load docker-image ^
                    %DOCKER_HUB_IMAGE%:%BUILD_NUMBER% ^
                    --name %KIND_CLUSTER%


                    if errorlevel 1 (
                        echo.
                        echo ===== Kind Image Load FAILED =====
                        exit /b 1
                    )


                    echo.
                    echo ===== Images Available Inside Kind =====


                    "%DOCKER_EXE%" exec %KIND_CLUSTER%-control-plane ^
                    crictl images | findstr wifi-pytest


                    echo.

                '''


                echo '===== Docker Image Loaded Into Kind ====='
            }
        }



        // ============================================================
        // 9. PREPARE KUBERNETES JOB
        // ============================================================
        stage('Prepare Kubernetes Job') {

            steps {

                echo '===== Preparing Kubernetes Job ====='


                bat '''

                    echo.
                    echo ===== Kubernetes Job Manifest =====


                    type gitops-repo\\k8s\\pytest-job.yaml


                    echo.
                    echo ===== Validating Kubernetes Manifest =====


                    "%KUBECTL_EXE%" apply ^
                    --dry-run=client ^
                    -f gitops-repo\\k8s\\pytest-job.yaml ^
                    -n %K8S_NAMESPACE%


                    if errorlevel 1 (
                        echo.
                        echo ===== Kubernetes Manifest Validation FAILED =====
                        exit /b 1
                    )


                    echo.
                    echo ===== Kubernetes Manifest Validation Successful =====


                    echo.

                '''
            }
        }



        // ============================================================
        // 10. RUN PYTEST IN KUBERNETES
        // ============================================================
        stage('Run Pytest in Kubernetes') {

            steps {

                echo '===== Running Pytest in Kubernetes ====='


                bat '''

                    echo.
                    echo ============================================================
                    echo             APPLYING PYTEST KUBERNETES JOB
                    echo ============================================================


                    "%KUBECTL_EXE%" apply ^
                    -f gitops-repo\\k8s\\pytest-job.yaml ^
                    -n %K8S_NAMESPACE%


                    if errorlevel 1 (
                        echo.
                        echo ===== Kubernetes Job Apply FAILED =====
                        exit /b 1
                    )


                    echo.
                    echo ===== Waiting For Job Completion =====


                    "%KUBECTL_EXE%" wait ^
                    --for=condition=complete ^
                    job/%K8S_JOB_NAME% ^
                    -n %K8S_NAMESPACE% ^
                    --timeout=10m


                    if errorlevel 1 (

                        echo.
                        echo ============================================================
                        echo              KUBERNETES JOB FAILED
                        echo ============================================================


                        echo.
                        echo ===== Job Status =====


                        "%KUBECTL_EXE%" get job ^
                        %K8S_JOB_NAME% ^
                        -n %K8S_NAMESPACE% ^
                        -o yaml


                        echo.
                        echo ===== Pod Status =====


                        "%KUBECTL_EXE%" get pods ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=%K8S_JOB_NAME% ^
                        -o wide


                        echo.
                        echo ===== Pod Logs =====


                        "%KUBECTL_EXE%" logs ^
                        -n %K8S_NAMESPACE% ^
                        -l job-name=%K8S_JOB_NAME% ^
                        --tail=200


                        echo.

                        exit /b 1
                    )


                    echo.
                    echo ============================================================
                    echo              KUBERNETES JOB COMPLETED
                    echo ============================================================


                    echo.
                    echo ===== Kubernetes Job Status =====


                    "%KUBECTL_EXE%" get job ^
                    %K8S_JOB_NAME% ^
                    -n %K8S_NAMESPACE%


                    echo.
                    echo ===== Kubernetes Pods =====


                    "%KUBECTL_EXE%" get pods ^
                    -n %K8S_NAMESPACE% ^
                    -l job-name=%K8S_JOB_NAME% ^
                    -o wide


                    echo.
                    echo ===== Pytest Logs =====


                    "%KUBECTL_EXE%" logs ^
                    -n %K8S_NAMESPACE% ^
                    -l job-name=%K8S_JOB_NAME%


                    echo.

                '''
            }
        }



        // ============================================================
        // 11. COLLECT KUBERNETES REPORTS
        // ============================================================
        stage('Collect Kubernetes Reports') {

            steps {

                echo '===== Collecting Kubernetes Test Reports ====='


                bat '''

                    echo.
                    echo ===== Creating K8s Report Directory =====


                    if not exist reports\\k8s mkdir reports\\k8s


                    echo.
                    echo ===== Finding Completed Pytest Pod =====


                    "%KUBECTL_EXE%" get pods ^
                    -n %K8S_NAMESPACE% ^
                    -l job-name=%K8S_JOB_NAME% ^
                    -o wide


                    echo.
                    echo ===== Getting Pod Name =====


                    for /f "tokens=*" %%P in ('"%KUBECTL_EXE%" get pods -n %K8S_NAMESPACE% -l job-name=%K8S_JOB_NAME% -o jsonpath="{.items[0].metadata.name}"') do (

                        echo.
                        echo ===== Pytest Pod: %%P =====


                        echo.
                        echo ===== Copying JUnit XML =====


                        "%KUBECTL_EXE%" cp ^
                        -n %K8S_NAMESPACE% ^
                        %%P:/app/reports/junit-results.xml ^
                        reports\\k8s\\junit-results-k8s.xml


                        if errorlevel 1 (
                            echo.
                            echo ===== JUnit Copy FAILED =====
                            exit /b 1
                        )


                        echo.
                        echo ===== Copying HTML Report =====


                        "%KUBECTL_EXE%" cp ^
                        -n %K8S_NAMESPACE% ^
                        %%P:/app/reports/wlan_test_report.html ^
                        reports\\k8s\\wlan_test_report-k8s.html


                        if errorlevel 1 (
                            echo.
                            echo ===== HTML Report Copy FAILED =====
                            exit /b 1
                        )

                    )


                    echo.
                    echo ===== Kubernetes Reports =====


                    dir reports\\k8s


                    echo.

                '''
            }
        }



        // ============================================================
        // 12. VERIFY REPORTS
        // ============================================================
        stage('Verify Reports') {

            steps {

                echo '===== Verifying Test Reports ====='


                bat '''

                    echo.
                    echo ===== JUnit XML =====


                    if exist reports\\k8s\\junit-results-k8s.xml (

                        echo JUnit report found.

                        dir reports\\k8s\\junit-results-k8s.xml

                    ) else (

                        echo JUnit report NOT FOUND.

                    )


                    echo.
                    echo ===== HTML Report =====


                    if exist reports\\k8s\\wlan_test_report-k8s.html (

                        echo HTML report found.

                        dir reports\\k8s\\wlan_test_report-k8s.html

                    ) else (

                        echo HTML report NOT FOUND.

                    )


                    echo.

                '''
            }
        }
    }



    // ================================================================
    // POST ACTIONS
    // ================================================================
    post {

        always {

            echo '===== Jenkins Post Actions ====='


            // --------------------------------------------------------
            // Publish JUnit only if report exists
            // --------------------------------------------------------
            script {

                if (fileExists('reports/k8s/junit-results-k8s.xml')) {

                    echo '===== Publishing JUnit Results ====='

                    junit(
                        testResults: 'reports/k8s/junit-results-k8s.xml',
                        allowEmptyResults: false
                    )

                } else {

                    echo '===== No Kubernetes JUnit report found ====='

                }
            }


            // --------------------------------------------------------
            // Archive reports
            // --------------------------------------------------------
            archiveArtifacts(
                artifacts: 'reports/k8s/*.xml,reports/k8s/*.html,reports/*.log',
                allowEmptyArchive: true
            )


            echo '===== Reports Processed ====='
        }



        success {

            echo '''
            ============================================================
                            PIPELINE SUCCESS
            ============================================================

            Jenkins CI completed successfully.

            Docker image:
              Built
              Pushed to Docker Hub

            GitOps:
              Manifest updated
              Git commit created
              Git push successful

            Kubernetes:
              Pytest Job completed

            Reports:
              JUnit XML collected
              HTML report collected

            ============================================================
            '''
        }



        failure {

            echo '''
            ============================================================
                            PIPELINE FAILED
            ============================================================

            Check the failed stage above.

            Important areas:
              1. Docker build
              2. Docker Hub authentication
              3. Docker Hub push
              4. GitOps Git push
              5. Kubernetes Job
              6. Pytest execution
              7. Report collection

            ============================================================
            '''
        }



        aborted {

            echo '''
            ============================================================
                            PIPELINE ABORTED
            ============================================================

            The Jenkins pipeline was aborted or timed out.

            If GitOps Push is running:
              Check GitHub authentication first.

            ============================================================
            '''
        }



        cleanup {

            echo '===== Cleaning Jenkins Workspace ====='

            cleanWs()

            echo '===== Workspace Cleanup Complete ====='
        }
    }
}