pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME   = 'wifi-pytest-advanced'
        HTML_REPORT  = 'reports/wlan_test_report.html'
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
                    echo ==========================================
                    echo Jenkins Environment
                    echo ==========================================

                    echo.
                    echo Jenkins User:
                    whoami

                    echo.
                    echo Git:
                    git --version

                    echo.
                    echo Docker:
                    docker --version

                    echo.
                    echo Docker Engine:
                    docker info --format "Version={{.ServerVersion}} CPUs={{.NCPU}} Memory={{.MemTotal}}"

                    echo.
                    echo Workspace:
                    echo %WORKSPACE%
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    echo ==========================================
                    echo Building Docker Image
                    echo ==========================================

                    docker build ^
                        -t %IMAGE_NAME%:%BUILD_NUMBER% .

                    if errorlevel 1 (
                        echo ERROR: Docker image build failed
                        exit /b 1
                    )

                    echo.
                    echo Docker image created:
                    docker images %IMAGE_NAME%:%BUILD_NUMBER%
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
                            echo ==========================================
                            echo Running Pytest Inside Docker
                            echo ==========================================

                            if not exist reports mkdir reports

                            docker run --rm ^
                                -v "%WORKSPACE%\\reports:/app/reports" ^
                                %IMAGE_NAME%:%BUILD_NUMBER% ^
                                python -m pytest -v -s ^
                                --html=/app/reports/wlan_test_report.html ^
                                --self-contained-html ^
                                --junitxml=/app/reports/junit-results.xml

                            if errorlevel 1 (
                                echo.
                                echo Pytest execution FAILED
                                echo Reports will still be collected.
                                exit /b 1
                            )

                            echo.
                            echo Pytest execution PASSED
                        '''
                    }
                }
            }
        }

        stage('Verify Test Reports') {
            steps {
                bat '''
                    echo ==========================================
                    echo Verifying Test Reports
                    echo ==========================================

                    if not exist reports\\junit-results.xml (
                        echo ERROR: JUnit XML report not found
                        exit /b 1
                    )

                    if not exist reports\\wlan_test_report.html (
                        echo ERROR: HTML report not found
                        exit /b 1
                    )

                    echo.
                    echo Reports successfully generated:

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
            echo '''
==========================================
WLAN PYTEST CI PIPELINE PASSED
==========================================
Docker image build : PASSED
Pytest execution   : PASSED
JUnit report       : PUBLISHED
HTML report        : ARCHIVED
==========================================
'''
        }

        failure {
            echo '''
==========================================
WLAN PYTEST CI PIPELINE FAILED
==========================================
Check:
1. Docker build
2. Pytest console output
3. JUnit results
4. HTML report
==========================================
'''
        }

        cleanup {
            bat '''
                echo ==========================================
                echo Docker Image Cleanup
                echo ==========================================

                docker image rm %IMAGE_NAME%:%BUILD_NUMBER%

                if errorlevel 1 (
                    echo Image cleanup skipped.
                ) else (
                    echo Docker image removed successfully.
                )
            '''
        }
    }
}