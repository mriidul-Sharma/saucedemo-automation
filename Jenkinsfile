pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out source code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Setting up Python virtual environment and installing packages...'
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate.bat
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Executing Pytest test suite...'
                bat '''
                call venv\\Scripts\\activate.bat
                pytest -v --junitxml=reports/test-results.xml
                '''
            }
        }
    }

    post {
        always {
            echo 'Archiving test results...'
            junit testResults: 'reports/test-results.xml', allowEmptyResults: true
        }
    }
}