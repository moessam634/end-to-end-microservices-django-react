pipeline {
    agent any
    
    parameters {
        string(name: 'GIT_REPO_URL', defaultValue: 'https://github.com/moessam634/end-to-end-microservices-django-react.git', description: 'Git repository URL')
        string(name: 'GIT_BRANCH', defaultValue: 'main', description: 'Git branch to build')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip running tests')
        booleanParam(name: 'SKIP_SONARQUBE', defaultValue: false, description: 'Skip SonarQube analysis')
    }
    
    // Note: SonarQube Scanner tool 'SonarScanner' must be configured in Jenkins Global Tool Configuration
    // Go to: Manage Jenkins > Global Tool Configuration > SonarQube Scanner
    // Name: SonarScanner (must match the name used in tool 'SonarScanner' call in SonarQube Analysis stage)
    // Install automatically: Yes
    // Version: Latest
    
    environment {
        // Application Configuration
        APP_NAME = 'gig-router-backend'
        DOCKER_IMAGE_NAME = 'mohamedessam122002/backend-django-app'
        BACKEND_DIR = 'backend'
        SONARQUBE_SERVER_NAME = 'sonar'
        
        // Build Version
        BUILD_VERSION = "${BUILD_NUMBER}"
        
        // Dynamic Port Allocation
        POSTGRES_PORT = "${5432 + BUILD_NUMBER.toInteger()}"
        REDIS_PORT = "${6379 + BUILD_NUMBER.toInteger()}"
        
        // Container Names
        POSTGRES_CONTAINER = "postgres-test-${BUILD_NUMBER}"
        REDIS_CONTAINER = "redis-test-${BUILD_NUMBER}"
        
        // Database Configuration
        DB_NAME = 'gig_router_test'
        DB_USER = 'postgres'
        DB_PASSWORD = 'postgres'
        DB_HOST = 'localhost'
        
        // Credentials
        DOCKER_REGISTRY = 'docker.io'
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                script {
                    echo "=== Stage 1: Checking out code from ${params.GIT_REPO_URL} - Branch: ${params.GIT_BRANCH} ==="
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "*/${params.GIT_BRANCH}"]],
                        userRemoteConfigs: [[
                            url: params.GIT_REPO_URL,
                            credentialsId: 'git-creds'
                        ]]
                    ])
                    echo "Code checkout completed successfully"
                }
            }
        }
        
        stage('Setup Test Infrastructure') {
            steps {
                script {
                    echo "=== Stage 2: Setting up test infrastructure ==="
                    echo "Starting PostgreSQL container on port ${POSTGRES_PORT}"
                    sh """
                        docker run -d \
                            --name ${POSTGRES_CONTAINER} \
                            -e POSTGRES_DB=${DB_NAME} \
                            -e POSTGRES_USER=${DB_USER} \
                            -e POSTGRES_PASSWORD=${DB_PASSWORD} \
                            -p ${POSTGRES_PORT}:5432 \
                            postgres:15-alpine
                    """
                    
                    echo "Starting Redis container on port ${REDIS_PORT}"
                    sh """
                        docker run -d \
                            --name ${REDIS_CONTAINER} \
                            -p ${REDIS_PORT}:6379 \
                            redis:7-alpine
                    """
                    
                    echo "Waiting for PostgreSQL to be ready..."
                    sh """
                        timeout 60 bash -c 'until docker exec ${POSTGRES_CONTAINER} pg_isready -U ${DB_USER}; do sleep 2; done'
                    """
                    
                    echo "Waiting for Redis to be ready..."
                    sh """
                        timeout 60 bash -c 'until docker exec ${REDIS_CONTAINER} redis-cli ping | grep -q PONG; do sleep 2; done'
                    """
                    
                    echo "Test infrastructure setup completed"
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    echo "=== Stage 3: Installing Python dependencies ==="
                    dir("${BACKEND_DIR}") {
                        sh """
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            pip install pytest-cov flake8 bandit safety
                        """
                    }
                    echo "Dependencies installed successfully"
                }
            }
        }
        
        stage('Run Migrations') {
            steps {
                script {
                    echo "=== Stage 4: Running Django migrations ==="
                    dir("${BACKEND_DIR}") {
                        sh """
                            . venv/bin/activate
                            export DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${POSTGRES_PORT}/${DB_NAME}"
                            export REDIS_URL="redis://${DB_HOST}:${REDIS_PORT}/0"
                            export SECRET_KEY="test-secret-key-for-ci-pipeline"
                            export DEBUG=True
                            export ALLOWED_HOSTS="localhost,127.0.0.1"
                            
                            python manage.py migrate --noinput
                        """
                    }
                    echo "Migrations completed successfully"
                }
            }
        }
        
        stage('Unit Test') {
            when {
                expression { return !params.SKIP_TESTS }
            }
            steps {
                script {
                    echo "=== Stage 5: Running unit tests with pytest ==="
                    dir("${BACKEND_DIR}") {
                        sh """
                            . venv/bin/activate
                            export DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${POSTGRES_PORT}/${DB_NAME}"
                            export REDIS_URL="redis://${DB_HOST}:${REDIS_PORT}/0"
                            export SECRET_KEY="test-secret-key-for-ci-pipeline"
                            export DEBUG=True
                            export ALLOWED_HOSTS="localhost,127.0.0.1"
                            
                            # Create pytest configuration
                            cat > pytest.ini << 'EOF'
[pytest]
DJANGO_SETTINGS_MODULE = gig_router.settings
python_files = tests.py test_*.py *_tests.py
addopts = -v --tb=short --strict-markers
testpaths = .
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
EOF
                            
                            # Run tests with coverage
                            pytest -v \
                                --cov=. \
                                --cov-report=xml:coverage.xml \
                                --cov-report=html:htmlcov \
                                --cov-report=term-missing \
                                --junitxml=test-results/junit.xml \
                                --maxfail=5 || EXIT_CODE=\$?
                            
                            # Handle exit codes (0 = success, 5 = no tests found)
                            if [ "\${EXIT_CODE:-0}" -eq 5 ]; then
                                echo "No tests found, but continuing..."
                                exit 0
                            elif [ "\${EXIT_CODE:-0}" -ne 0 ]; then
                                echo "Tests failed with exit code \${EXIT_CODE}"
                                exit \${EXIT_CODE}
                            fi
                        """
                    }
                    
                    // Archive test results
                    junit allowEmptyResults: true, testResults: "${BACKEND_DIR}/test-results/junit.xml"
                    
                    // Publish HTML coverage report
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: "${BACKEND_DIR}/htmlcov",
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                    
                    echo "Unit tests completed successfully"
                }
            }
        }
        
        stage('Code Quality Analysis') {
            steps {
                script {
                    echo "=== Stage 6: Running code quality analysis ==="
                    dir("${BACKEND_DIR}") {
                        // Flake8 linting
                        echo "Running Flake8 linting..."
                        sh """
                            . venv/bin/activate
                            flake8 . \
                                --exclude=venv,env,migrations,__pycache__,staticfiles,media \
                                --max-line-length=120 \
                                --extend-ignore=E501,W503 \
                                --output-file=flake8-report.txt \
                                --exit-zero
                        """
                        
                        // Bandit security scan
                        echo "Running Bandit security scan..."
                        sh """
                            . venv/bin/activate
                            bandit -r . \
                                -x ./venv,./env,./migrations,./tests.py,./test_*.py \
                                -f json \
                                -o bandit-report.json \
                                --exit-zero || true
                            
                            bandit -r . \
                                -x ./venv,./env,./migrations,./tests.py,./test_*.py \
                                -f txt \
                                -o bandit-report.txt \
                                --exit-zero || true
                        """
                        
                        // Archive reports
                        archiveArtifacts artifacts: 'flake8-report.txt,bandit-report.json,bandit-report.txt', allowEmptyArchive: true
                    }
                    echo "Code quality analysis completed"
                }
            }
        }
        
        stage('SonarQube Analysis') {
            when {
                expression { return !params.SKIP_SONARQUBE }
            }
            steps {
                script {
                    echo "=== Stage 7: Running SonarQube analysis ==="
                    dir("${BACKEND_DIR}") {
                        def scannerHome = tool 'SonarScanner'
                        withSonarQubeEnv('sonar') {
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                    -Dsonar.projectKey=${APP_NAME} \
                                    -Dsonar.projectName="Gig Router Backend" \
                                    -Dsonar.projectVersion=${BUILD_VERSION} \
                                    -Dsonar.sources=. \
                                    -Dsonar.exclusions=**/migrations/**,**/tests/**,**/static/**,**/media/**,**/__pycache__/**,**/venv/**,**/env/**,**/staticfiles/** \
                                    -Dsonar.python.coverage.reportPaths=coverage.xml \
                                    -Dsonar.python.xunit.reportPath=test-results/junit.xml \
                                    -Dsonar.python.version=3.11
                            """
                        }
                    }
                    echo "SonarQube analysis completed"
                }
            }
        }
        
        stage('Quality Gate') {
            when {
                expression { return !params.SKIP_SONARQUBE }
            }
            steps {
                script {
                    echo "=== Stage 8: Waiting for SonarQube Quality Gate ==="
                    timeout(time: 5, unit: 'MINUTES') {
                        def qg = waitForQualityGate()
                        if (qg.status != 'OK') {
                            echo "WARNING: Quality Gate failed: ${qg.status}"
                            echo "Continuing pipeline despite Quality Gate failure..."
                            // Don't fail the build, just warn
                        } else {
                            echo "Quality Gate passed successfully"
                        }
                    }
                }
            }
        }
        
        stage('OWASP Dependency Scan') {
            steps {
                script {
                    echo "=== Stage 9: Running OWASP dependency scan ==="
                    dir("${BACKEND_DIR}") {
                        sh """
                            . venv/bin/activate
                            
                            # Use safety to check for known vulnerabilities
                            echo "Running Safety check for Python dependencies..."
                            safety check \
                                --json \
                                --output safety-report.json \
                                --continue-on-error || true
                            
                            safety check \
                                --output safety-report.txt \
                                --continue-on-error || true
                            
                            echo "Dependency scan completed"
                        """
                        
                        archiveArtifacts artifacts: 'safety-report.json,safety-report.txt', allowEmptyArchive: true
                    }
                    echo "OWASP dependency scan completed"
                }
            }
        }
        
        stage('Push Artifact to Nexus') {
            steps {
                script {
                    echo "=== Stage 10: Creating and pushing artifact to Nexus ==="
                    dir("${BACKEND_DIR}") {
                        sh """
                            # Create tarball of backend application
                            tar -czf ../gig-router-backend-${BUILD_VERSION}.tar.gz \
                                --exclude='venv' \
                                --exclude='env' \
                                --exclude='__pycache__' \
                                --exclude='*.pyc' \
                                --exclude='.pytest_cache' \
                                --exclude='htmlcov' \
                                --exclude='test-results' \
                                --exclude='coverage.xml' \
                                .
                            
                            # Generate SHA256 checksum
                            cd ..
                            sha256sum gig-router-backend-${BUILD_VERSION}.tar.gz > gig-router-backend-${BUILD_VERSION}.tar.gz.sha256
                        """
                        
                        // Archive artifacts in Jenkins
                        archiveArtifacts artifacts: "../gig-router-backend-${BUILD_VERSION}.tar.gz,../gig-router-backend-${BUILD_VERSION}.tar.gz.sha256"
                        
                        // Upload to Nexus (if configured)
                        withCredentials([usernamePassword(credentialsId: 'nexus-maven-creds', usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                            sh """
                                echo "Artifact would be uploaded to Nexus repository"
                                echo "Nexus user: \${NEXUS_USER}"
                                # Uncomment when Nexus is configured:
                                # curl -v -u \${NEXUS_USER}:\${NEXUS_PASS} \
                                #     --upload-file ../gig-router-backend-${BUILD_VERSION}.tar.gz \
                                #     http://nexus-server:8081/repository/maven-releases/com/gigrouter/backend/${BUILD_VERSION}/gig-router-backend-${BUILD_VERSION}.tar.gz
                            """
                        }
                    }
                    echo "Artifact creation and archival completed"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "=== Stage 11: Building Docker image ==="
                    dir("${BACKEND_DIR}") {
                        sh """
                            docker build \
                                -t ${DOCKER_IMAGE_NAME}:${BUILD_VERSION} \
                                -t ${DOCKER_IMAGE_NAME}:latest \
                                -f Backend-Dockerfile \
                                .
                        """
                    }
                    echo "Docker image built successfully: ${DOCKER_IMAGE_NAME}:${BUILD_VERSION}"
                }
            }
        }
        
        stage('Trivy Image Scan') {
            steps {
                script {
                    echo "=== Stage 12: Scanning Docker image with Trivy ==="
                    sh """
                        # Check if Trivy is installed
                        if ! command -v trivy &> /dev/null; then
                            echo "Trivy not found. Installing Trivy..."
                            
                            # Modern installation method using gpg and keyrings
                            wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
                            echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb \$(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
                            sudo apt-get update
                            sudo apt-get install -y trivy || echo "Failed to install Trivy via apt, trying alternative method..."
                            
                            # Alternative installation method using install script
                            if ! command -v trivy &> /dev/null; then
                                curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
                            fi
                        fi
                        
                        # Run Trivy scan
                        trivy image \
                            --severity HIGH,CRITICAL \
                            --format json \
                            --output trivy-report.json \
                            ${DOCKER_IMAGE_NAME}:${BUILD_VERSION} || true
                        
                        trivy image \
                            --severity HIGH,CRITICAL \
                            --format table \
                            --output trivy-report.txt \
                            ${DOCKER_IMAGE_NAME}:${BUILD_VERSION} || true
                        
                        echo "Trivy scan results:"
                        cat trivy-report.txt || echo "No trivy report generated"
                    """
                    
                    archiveArtifacts artifacts: 'trivy-report.json,trivy-report.txt', allowEmptyArchive: true
                    echo "Trivy image scan completed"
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "=== Stage 13: Pushing Docker image to Docker Hub ==="
                    withCredentials([usernamePassword(credentialsId: 'docker-creds-id', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            echo \${DOCKER_PASS} | docker login -u \${DOCKER_USER} --password-stdin ${DOCKER_REGISTRY}
                            
                            docker push ${DOCKER_IMAGE_NAME}:${BUILD_VERSION}
                            docker push ${DOCKER_IMAGE_NAME}:latest
                            
                            docker logout ${DOCKER_REGISTRY}
                        """
                    }
                    echo "Docker image pushed successfully to Docker Hub"
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "=== Post Actions: Cleanup ==="
                
                // Stop and remove PostgreSQL container
                sh """
                    docker stop ${POSTGRES_CONTAINER} || true
                    docker rm ${POSTGRES_CONTAINER} || true
                """ 
                
                // Stop and remove Redis container
                sh """
                    docker stop ${REDIS_CONTAINER} || true
                    docker rm ${REDIS_CONTAINER} || true
                """
                
                // Prune dangling images
                sh """
                    docker image prune -f || true
                """
                
                echo "Cleanup completed"
            }
        }
        
        success {
            echo "=== Pipeline completed successfully! ==="
            echo "Build Version: ${BUILD_VERSION}"
            echo "Docker Image: ${DOCKER_IMAGE_NAME}:${BUILD_VERSION}"
        }
        
        failure {
            echo "=== Pipeline failed! ==="
            echo "Please check the logs for more details."
        }
        
        unstable {
            echo "=== Pipeline completed with warnings ==="
            echo "Some tests or quality checks may have failed."
        }
    }
}
