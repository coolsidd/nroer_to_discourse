pipeline {
    agent {
        dockerfile{
            args "-it -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker"
        }
   }
    stages {
        stage('build') {
            steps {
                sh '/project/discourse_docker/discourse-setup'
            }
        }
    }
}
