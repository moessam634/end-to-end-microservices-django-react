# Jenkins CI/CD Pipeline Documentation

## Overview

This repository includes a comprehensive Jenkins CI/CD pipeline for the Gig Router Backend Django application. The pipeline automates the entire software delivery process from code checkout to Docker image deployment.

## Pipeline Stages

The Jenkins pipeline consists of 13 stages:

### 1. Checkout Code
- Clones the repository from GitHub
- Supports parameterized Git URL and branch selection
- Uses Git credentials configured in Jenkins

### 2. Setup Test Infrastructure
- Starts PostgreSQL 15-alpine container for database tests
- Starts Redis 7-alpine container for caching tests
- Uses dynamic port allocation based on build number to avoid conflicts
- Waits for services to be ready before proceeding

### 3. Build
- Creates Python virtual environment
- Installs all dependencies from `requirements.txt`
- Installs additional testing and security tools (pytest-cov, flake8, bandit, safety)

### 4. Run Migrations
- Applies Django database migrations to test database
- Configures DATABASE_URL with dynamic PostgreSQL port
- Sets up required environment variables

### 5. Unit Test
- Runs pytest with coverage reporting
- Generates JUnit XML for Jenkins integration
- Creates HTML coverage reports
- Can be skipped via SKIP_TESTS parameter
- Handles exit code 5 (no tests found) gracefully

### 6. Code Quality Analysis
- **Flake8**: Lints Python code for style issues
- **Bandit**: Scans for security vulnerabilities in Python code
- Generates reports in both JSON and text formats
- Archives all reports as build artifacts

### 7. SonarQube Analysis
- Performs comprehensive code quality and security analysis
- Excludes migrations, tests, and static files
- Includes code coverage and test results
- Can be skipped via SKIP_SONARQUBE parameter
- Requires SonarQube Scanner tool configured as 'SonarScanner'

### 8. Quality Gate
- Waits for SonarQube quality gate results
- Timeout set to 5 minutes
- Continues pipeline with warning if quality gate fails (doesn't block deployment)

### 9. OWASP Dependency Scan
- Uses Safety to check Python dependencies for known vulnerabilities
- Generates vulnerability reports
- Archives reports for review

### 10. Push Artifact to Nexus
- Creates tarball of backend application
- Generates SHA256 checksum
- Archives artifacts in Jenkins
- Uploads to Nexus repository (when configured)

### 11. Build Docker Image
- Builds Docker image using Backend-Dockerfile
- Tags with build version and 'latest'
- Uses multi-stage build for optimization

### 12. Trivy Image Scan
- Scans Docker image for vulnerabilities
- Focuses on HIGH and CRITICAL severity issues
- Generates reports in JSON and table formats
- Auto-installs Trivy if not present

### 13. Push to Docker Hub
- Authenticates with Docker Hub using credentials
- Pushes both versioned and latest tags
- Logs out securely after push

## Pipeline Parameters

The pipeline supports the following build parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| GIT_REPO_URL | String | `https://github.com/moessam634/end-to-end-microservices-django-react.git` | Git repository URL |
| GIT_BRANCH | String | `main` | Git branch to build |
| SKIP_TESTS | Boolean | `false` | Skip running tests |
| SKIP_SONARQUBE | Boolean | `false` | Skip SonarQube analysis |

## Environment Variables

### Application Configuration
```groovy
APP_NAME = 'gig-router-backend'
DOCKER_IMAGE_NAME = 'mohamedessam122002/backend-django-app'
BACKEND_DIR = 'backend'
SONARQUBE_SERVER_NAME = 'sonar'
```

### Dynamic Port Allocation
```groovy
POSTGRES_PORT = 5432 + BUILD_NUMBER
REDIS_PORT = 6379 + BUILD_NUMBER
```

### Database Configuration
```groovy
DB_NAME = 'gig_router_test'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'localhost'
```

## Required Jenkins Credentials

Configure the following credentials in Jenkins:

| Credential ID | Type | Description |
|---------------|------|-------------|
| `git-creds` | Username/Password | Git repository access (if needed) |
| `sonar` | Secret Text | SonarQube authentication token |
| `nexus-maven-creds` | Username/Password | Nexus repository credentials |
| `docker-creds-id` | Username/Password | Docker Hub credentials |

## Required Jenkins Plugins

- Pipeline
- Git Plugin
- Docker Pipeline
- SonarQube Scanner
- JUnit Plugin
- HTML Publisher Plugin
- Credentials Plugin
- Credentials Binding Plugin

## Jenkins Tool Configuration

### SonarQube Scanner
1. Go to **Manage Jenkins** > **Global Tool Configuration**
2. Find **SonarQube Scanner** section
3. Click **Add SonarQube Scanner**
4. Set **Name** to `SonarScanner`
5. Check **Install automatically**
6. Select latest version
7. Save configuration

### SonarQube Server
1. Go to **Manage Jenkins** > **Configure System**
2. Find **SonarQube servers** section
3. Click **Add SonarQube**
4. Set **Name** to `sonar`
5. Set **Server URL** to `http://192.168.10.128:9000`
6. Select **Server authentication token** credential
7. Save configuration

## Test Infrastructure

### PostgreSQL Container
- **Image**: postgres:15-alpine
- **Port**: 5432 + BUILD_NUMBER (dynamic)
- **Database**: gig_router_test
- **User**: postgres
- **Password**: postgres

### Redis Container
- **Image**: redis:7-alpine
- **Port**: 6379 + BUILD_NUMBER (dynamic)

## Post-Build Actions

The pipeline includes comprehensive cleanup in the `post` section:

### Always (runs regardless of build result)
- Stops and removes PostgreSQL test container
- Stops and removes Redis test container
- Prunes dangling Docker images

### Success
- Prints build version
- Prints Docker image tag

### Failure
- Prints failure message
- Directs to logs for debugging

### Unstable
- Prints warning message
- Indicates some tests or quality checks failed

## Build Artifacts

The following artifacts are archived:

1. **Test Results**: JUnit XML format
2. **Coverage Report**: HTML format
3. **Flake8 Report**: Text format
4. **Bandit Report**: JSON and text formats
5. **Safety Report**: JSON and text formats
6. **Trivy Report**: JSON and table formats
7. **Application Tarball**: Compressed backend application
8. **SHA256 Checksum**: For tarball verification

## Running the Pipeline

### Via Jenkins UI
1. Navigate to the pipeline job
2. Click **Build with Parameters**
3. Set desired parameters
4. Click **Build**

### Via Jenkins CLI
```bash
java -jar jenkins-cli.jar -s http://jenkins-url/ build CI-pipeline \
  -p GIT_BRANCH=main \
  -p SKIP_TESTS=false \
  -p SKIP_SONARQUBE=false
```

### Via Webhook (GitHub)
Configure a GitHub webhook to trigger builds on push:
1. Go to GitHub repository settings
2. Navigate to **Webhooks**
3. Add webhook with URL: `http://jenkins-url/github-webhook/`
4. Select events: Push, Pull Request

## Pipeline Workspace

- **Jenkins Workspace**: `/var/lib/jenkins/workspace/CI-pipeline`
- **Backend Directory**: `/var/lib/jenkins/workspace/CI-pipeline/backend`

## Test Execution Details

### pytest Configuration
The pipeline auto-generates `pytest.ini` with the following configuration:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = gig_router.settings
python_files = tests.py test_*.py *_tests.py
addopts = -v --tb=short --strict-markers
testpaths = .
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

### Coverage Reporting
- **Format**: XML (for SonarQube), HTML (for viewing), Terminal (for quick review)
- **Report Paths**: 
  - XML: `coverage.xml`
  - HTML: `htmlcov/`
  - JUnit: `test-results/junit.xml`

## Troubleshooting

### Pipeline Fails at Checkout
- Verify Git credentials are configured correctly
- Check network connectivity to GitHub
- Ensure branch name is correct

### Tests Fail
- Check PostgreSQL container is running: `docker ps | grep postgres-test`
- Verify database connection: `docker exec postgres-test-<BUILD_NUM> pg_isready`
- Review test logs in Jenkins console output

### SonarQube Analysis Fails
- Verify SonarQube Scanner tool is configured
- Check SonarQube server is accessible
- Validate sonar token credential

### Docker Build Fails
- Verify Backend-Dockerfile exists in backend directory
- Check Docker daemon is running
- Review build context and dependencies

### Docker Push Fails
- Verify Docker Hub credentials
- Check image was built successfully
- Ensure sufficient permissions on Docker registry

## Security Considerations

1. **Credentials Management**: All sensitive credentials are stored in Jenkins Credential Store
2. **Secret Scanning**: Bandit checks for hardcoded secrets
3. **Dependency Scanning**: Safety checks for vulnerable dependencies
4. **Image Scanning**: Trivy scans Docker images for vulnerabilities
5. **Code Quality**: SonarQube performs security analysis

## Performance Optimization

1. **Dynamic Port Allocation**: Prevents port conflicts in concurrent builds
2. **Virtual Environment**: Isolates Python dependencies
3. **Docker Layer Caching**: Speeds up Docker builds
4. **Parallel Test Execution**: pytest runs tests in parallel when possible
5. **Conditional Stages**: Skip tests or SonarQube via parameters

## Maintenance

### Regular Tasks
- Update tool versions in Global Tool Configuration
- Review and update dependency versions
- Monitor SonarQube quality gate rules
- Clean up old Docker images periodically
- Archive old build artifacts

### Version Updates
- Update Python dependencies in `requirements.txt`
- Update Docker base images
- Update Jenkins plugins
- Update SonarQube Scanner version

## Integration with CI/CD Workflow

```
Developer Push → GitHub Webhook → Jenkins Pipeline
                                        ↓
                                   Code Checkout
                                        ↓
                                   Test & Build
                                        ↓
                                   Quality Analysis
                                        ↓
                                   Security Scanning
                                        ↓
                                   Artifact Creation
                                        ↓
                                   Docker Image Build
                                        ↓
                                   Image Scanning
                                        ↓
                                   Push to Registry
                                        ↓
                                   Deployment (future stage)
```

## Support and Contact

For issues or questions regarding the CI/CD pipeline:
- Review Jenkins console output for detailed logs
- Check this documentation for configuration details
- Contact DevOps team for infrastructure issues

## License

This pipeline configuration is part of the Gig Router project and follows the same license.

---

**Last Updated**: 2024
**Pipeline Version**: 1.0
**Maintained By**: DevOps Team
