pipeline {
  agent any
  stages {
    stage('Lint using pylint') {
      steps {
        sh 'pylint src/banpt_report_generator'
      }
    }
    stage('Run tests') {
      steps {
        sh 'docker-compose -f docker-compose.test.yml up --abort-on-container-exit | grep FAIL; test $? -eq 1'
      }
    }
    stage('Zip report generator module') {
      steps {
        sh 'zip -r banpt_report_generator.zip src/banpt_report_generator'
      }
    }
  }
}