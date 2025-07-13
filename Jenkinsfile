pipeline {
  agent any

  stages {
    stage('Clone') {
      steps {
        git 'https://github.com/joepettinelli7/CV-Algs-Apps-2ED.git'
      }
    }
    stage('Build Docker Image') {
      steps {
        script {
          dockerImage = docker.build("test_container")
        }
      }
    }
    stage('Run Tests') {
      steps {
        script {
          dockerImage.run('--rm')
        }
      }
    }
  }
}
