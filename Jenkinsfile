pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                sh './launch_discourse.sh'
                sh './cleanup.sh ./discourse_docker/rake'
                sh ''
                sh './run_metrics'
            }
        }
    }
}
