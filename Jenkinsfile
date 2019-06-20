pipeline {
    agent {
        dockerfile{
            args "-it -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker --user root -p 8000:80"
        }
   }
    stages {
        stage('build') {
            steps {
                sh '/project/discourse_docker/discourse-setup'
            }
        }
        stage('run') {
            steps {
                sh '/project/nroer_to_discourse/setup_discourse.sh'
            }
        }
    }
}
