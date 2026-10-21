pipeline {
    agent any
    triggers {
    pollSCM('H/2 * * * *')
    }
    environment {
        DEPLOY_USER = 'milosz'
        DEPLOY_HOST = '192.168.100.137'
        APP_NAME    = 'weather_dashboard'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy') {
            steps {
                sshagent(credentials: ['deploy-server-ssh']) {
                    sh '''
                        ssh $DEPLOY_USER@$DEPLOY_HOST "cd ~/weather_dashboard && git fetch && git checkout $GIT_COMMIT && docker compose up -d --build"
                    '''
                }
            }
        }
    }
}