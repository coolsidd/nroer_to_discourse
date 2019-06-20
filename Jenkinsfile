pipeline {
    agent {
        dockerfile{
            args "-it -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker"
            label "doer_jenkins"
        }
   }
    stages {
        stage('build') {
            steps {
                sh '/projects/launch_discourse.sh'
            }
        }
    }
}
