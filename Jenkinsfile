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
        sh './test.sh'
      }
    }
    stage('Zip report generator module') {
      steps {
        sh 'zip -r banpt_report_generator.zip src/banpt_report_generator'
      }
    }
  }
}