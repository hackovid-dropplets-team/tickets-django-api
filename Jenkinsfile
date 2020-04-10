node {
    stage('Build image') {
        sh("docker build -t hackovid-dropplets-team/tickets-backend tickets-backend")
    }
    stage('Publish image') {
        sh("docker push hackovid-dropplets-team/tickets-backend")
    }
}