import groovy.json.JsonOutput
//git env vars
env.git_url = 'git@github.com:cspark777/Realtime-Data-analysist-platform.git'
env.git_branch = '*/master'
//slack env vars
env.slack_url = 'https://Realtime-Data-analysist-platform.slack.com/services/hooks/jenkins-ci?token=XXXXXXXXXXXXXX'
env.notification_channel = '-infra-alerts'
//jenkins env vars
env.jenkins_server_url = 'http://100.194.74.126/'
env.jenkins_workspace_path = "/var/lib/jenkins/workspace/${JOB_NAME}"
env.jenkins_node_label = 'master'

def notifySlack(text, channel) {
    def payload = JsonOutput.toJson(
      [
        text: text,
        channel: channel,
        username: "Jenkins-CI"
      ]
    )
    sh "curl -X POST --data-urlencode \'payload=${payload}\' ${slack_url}"
}

pipeline {
    agent {
      node {
        label "$jenkins_node_label"
      }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    environment {
        REGION = 'eu-west-1'
        ECR_URI = "041202610208.dkr.ecr.eu-west-1.amazonaws.com"
        PROJECT_NAME = "Realtime-Data-analysist-platform"
        VERSION = "stable"
    }

    stages {
        
        stage('BUILD'){
            stages {
                stage('Start Build'){
                    steps {
                        script {
                            notifySlack("DATA Admin GUI job is started to build! Build logs from jenkins server $jenkins_server_url/job/$JOB_NAME/$BUILD_NUMBER/console", notification_channel)
                        }
                    }
                }
                stage('Cleanup Workspace') {
                    steps {
                        cleanWs()
                    }
                }
                stage('Checkout') {
                    steps {
                        checkout([$class: 'GitSCM',
                        branches: [[name: "$git_branch"]],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [],
                        submoduleCfg: [],
                        userRemoteConfigs: [
                        [
                        url: "$git_url"]]])
                    }
                }
                stage('Login AWS ECR') {
                    steps {
                        sh '''
                            echo 'Authenticate to the ECR repo.'
                            eval \$(aws ecr get-login --region ${REGION} --no-include-email) &>/dev/null
                        '''
                    }
                }
                stage('Unit Test') {
                    steps {
                        sh'''
                            #!/bin/bash
                            echo -e "Running Unit Test.\n"
                            bash ./deployment/scripts/test.sh
                        '''
                    }
                }
                stage('Build Image') {
                    steps {
                        sh '''
                            docker build --no-cache  -t ${ECR_URI}/${PROJECT_NAME}:${VERSION} .
                        '''
                    }
                }
                stage('Push Image') {
                    steps {
                        sh '''
                            docker push ${ECR_URI}/${PROJECT_NAME}:${VERSION}
                        '''
                    }
                }
                stage('End Build'){
                    steps {
                        script {
                            notifySlack("DATA Admin GUI job is completed BUILD PHASE! Build logs from jenkins server $jenkins_server_url/job/$JOB_NAME/$BUILD_NUMBER/console", notification_channel)
                        }
                    }
                }
            }
        }
        
        stage ('DEPLOY') {
            steps {
                build job: 'DATA-Infratructure', parameters: [
                    string(name: 'REGION', value: "eu-west-1"),
                    string(name: 'ENV', value: "dev"),
                    string(name: 'OPTION', value: "Deploy App Containers")
                ]
            }
        }

        // stage('VALIDATE') {
        //     stages {
        //         stage('Start Validate'){
        //             steps {
        //                 script {
        //                     notifySlack("DATA Admin GUI job is validating service! Build logs from jenkins server $jenkins_server_url/job/$JOB_NAME/$BUILD_NUMBER/console", notification_channel)
        //                 }
        //             }
        //         }
        //         stage('Validate Service on DEV') {
        //             steps {
        //                 sh '''
        //                     bash ./deployment/scripts/validate.sh eu-west-1
        //                 '''
        //             }
        //         }
        //         stage('End Validate'){
        //             steps {
        //                 script {
        //                     notifySlack("DATA Admin GUI job is completed VALIDATE PHASE! Build logs from jenkins server $jenkins_server_url/job/$JOB_NAME/$BUILD_NUMBER/console", notification_channel)
        //                 }
        //             }
        //         }
        //     }
        // }
    }
    post {
        success {
            slackSend channel: "$notification_channel", color: 'good', message: "Job: ${JOB_NAME}-${BUILD_NUMBER} was successful."
        }
        failure {
            slackSend channel: "$notification_channel", color: 'danger', message: "Job: ${JOB_NAME}-${BUILD_NUMBER} was finished with some error. Please watch the Jenkins Console Output: ${JOB_URL}${BUILD_ID}/consoleFull"
        }
        unstable {
            slackSend channel: "$notification_channel", color: 'warning', message: "Job: ${JOB_NAME}-${BUILD_NUMBER} was finished with some error. Please watch the Jenkins Console Output: ${JOB_URL}${BUILD_ID}/console."
        }
    }
}
