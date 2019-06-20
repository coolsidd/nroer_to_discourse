pipeline {
    agent { dockerfile true }
    stages {
        stage('build') {
            steps {
                sh '/projects/launch_discourse.sh'
            }
        }
    }
}
