
pipeline {
    agent none

    options {
        skipDefaultCheckout(true)
    }

    environment {
        IMAGE_NAME = "abhinavvv11/cca2-task-tracker"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            agent { label 'aws-linux' }
            steps {
                checkout scm
                stash name: 'source',
                      includes: '**/*',
                      excludes: '.git/**,.venv/**'
            }
        }

        stage('Build and Test') {
            agent { label 'aws-linux' }
            steps {
                unstash 'source'
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    python -m unittest discover -s tests -v
                '''
            }
        }

        stage('Docker Build') {
            agent { label 'aws-linux' }
            steps {
                unstash 'source'
                sh '''
                    docker build \
                      -t "$IMAGE_NAME:$IMAGE_TAG" \
                      -t "$IMAGE_NAME:latest" .
                '''
            }
        }

        stage('Push Image') {
            agent { label 'aws-linux' }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        set +x
                        echo "$DOCKER_PASS" | docker login \
                          -u "$DOCKER_USER" --password-stdin
                        docker push "$IMAGE_NAME:$IMAGE_TAG"
                        docker push "$IMAGE_NAME:latest"
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            agent { label 'win-minikube' }
            steps {
                unstash 'source'

                writeFile file: 'deploy.ps1', text: '''
$ErrorActionPreference = 'Stop'

$kubectl = Join-Path $env:USERPROFILE 'kubectl.exe'
if (-not (Test-Path $kubectl)) {
    throw "kubectl.exe not found at $kubectl"
}

$image = "$($env:IMAGE_NAME):$($env:IMAGE_TAG)"
$deploymentPath = Join-Path (Get-Location).Path 'k8s\\deployment.yaml'
$generatedPath = Join-Path (Get-Location).Path 'k8s\\deployment-ci.yaml'
$yaml = [System.IO.File]::ReadAllText($deploymentPath)

if (-not $yaml.Contains('IMAGE_PLACEHOLDER')) {
    throw 'IMAGE_PLACEHOLDER was not found in deployment.yaml'
}

$yaml = $yaml.Replace('IMAGE_PLACEHOLDER', $image)
$encoding = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($generatedPath, $yaml, $encoding)

& $kubectl apply -f $generatedPath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $kubectl apply -f (Join-Path (Get-Location).Path 'k8s\\service.yaml')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $kubectl rollout status deployment/task-tracker --timeout=180s
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
'''

                bat 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File deploy.ps1'
            }
        }

        stage('Verify') {
            agent { label 'win-minikube' }
            steps {
                bat '''
                    "%USERPROFILE%\\kubectl.exe" get pods -o wide
                    if errorlevel 1 exit /b %errorlevel%

                    "%USERPROFILE%\\kubectl.exe" get deployment task-tracker
                    if errorlevel 1 exit /b %errorlevel%

                    "%USERPROFILE%\\kubectl.exe" get service task-tracker
                    if errorlevel 1 exit /b %errorlevel%
                '''
            }
        }
    }

    post {
        always {
            echo 'CCA 2 CI/CD pipeline finished. Check the stage results above.'
        }
    }
}
