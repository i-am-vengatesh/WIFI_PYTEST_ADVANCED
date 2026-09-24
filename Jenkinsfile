pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = 'wifi-pytest-advanced'
        HTML_REPORT = 'reports/wlan_test_report.html'
        JUNIT_REPORT = 'reports/junit-results.xml'
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

        stage('Verify Environment') {
            steps {
                bat '''
                    echo ===== Jenkins Environment =====
                    whoami

                    echo.
                    echo ===== Git Version =====
                    git --version

                    echo.
                    echo ===== Docker Version =====
                    docker --version

                    echo.
                    echo ===== Python Version =====
                    python --version
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    echo ===== Building Docker Image =====
                    docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .

                    echo.
                    echo ===== Docker Image Created =====
                    docker images %IMAGE_NAME%
                '''
            }
        }

        stage('Run Pytest in Docker') {
            steps {
                script {
                    catchError(
                        buildResult: 'FAILURE',
                        stageResult: 'FAILURE'
                    ) {
                        bat '''
                            echo ===== Creating Reports Directory =====
                            if not exist reports mkdir reports

                            echo.
                            echo ===== Running Pytest Inside Docker =====

                            docker run --rm ^
                              -v "%WORKSPACE%\\reports:/app/reports" ^
                              %IMAGE_NAME%:%BUILD_NUMBER% ^
                              python -m pytest -v -s ^
                              --html=/app/reports/wlan_test_report.html ^
                              --self-contained-html ^
                              --junitxml=/app/reports/junit-results.xml
                        '''
                    }
                }
            }
        }

        stage('Verify Test Reports') {
            steps {
                bat '''
                    echo ===== Test Reports =====

                    if exist reports\\junit-results.xml (
                        echo JUnit XML found
                    ) else (
                        echo ERROR: JUnit XML not found
                        exit /b 1
                    )

                    if exist reports\\wlan_test_report.html (
                        echo HTML report found
                    ) else (
                        echo ERROR: HTML report not found
                        exit /b 1
                    )

                    echo.
                    echo ===== Report Files =====
                    dir reports
                '''
            }
        }

        stage('Publish JUnit Results') {
            steps {
                junit(
                    testResults: 'reports/junit-results.xml',
                    allowEmptyResults: false
                )
            }
        }
    }

    post {

        always {
            archiveArtifacts(
                artifacts: 'reports/**',
                allowEmptyArchive: true
            )
        }

        success {
            echo '===== CI PIPELINE PASSED ====='
            echo 'Docker build completed successfully.'
            echo 'Pytest completed successfully.'
            echo 'JUnit and HTML reports were published.'
        }

        failure {
            echo '===== CI PIPELINE FAILED ====='
            echo 'Check the Pytest console output and JUnit report.'
        }

        cleanup {
            bat '''
                echo ===== Docker Cleanup =====
                docker image rm %IMAGE_NAME%:%BUILD_NUMBER% || exit /b 0
            '''
        }
    }
}