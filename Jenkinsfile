pipeline {
    agent any

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
                sshagent(credentials: ['debianssh']) {
                    sh '''
                        ssh $DEPLOY_USER@$DEPLOY_HOST "echo połączono && docker --version"
                    '''
                }
            }
        }
    }
}