pipeline {
  agent any

  stages {
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
