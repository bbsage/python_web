podTemplate(
  label: 'python-and-jnlp',
  containers: [
    containerTemplate(
      name: 'jnlp',
      image: 'jenkins/inbound-agent:latest',
      args: '${computer.jnlpmac} ${computer.name}'
    ),
    containerTemplate(
      name: 'python',
      image: 'python:3.12-slim',
      command: 'sleep',
      args: '1d'
    ),
    containerTemplate(
      name: 'docker',
      image: 'docker:24.0-dind',
      privileged: true,
      command: 'dockerd-entrypoint.sh',
      args: ''
    ),
    containerTemplate(
      name: 'kubectl',
      image: 'bitnami/kubectl:latest',
      command: 'cat',
      ttyEnabled: true
    )
  ]
) {
  node('python-and-jnlp') {

    def VENV_DIR = '.venv'
    def IMAGE_NAME = "localhost:32000/python-web:latest"

    stage('Checkout') {
      checkout scm
    }

    stage('Setup Python Env') {
      container('python') {
        sh """
          python3 -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          pip install -r requirements-dev.txt
        """
      }
    }

    stage('Lint') {
      container('python') {
        sh """
          . ${VENV_DIR}/bin/activate
          black --check .
          mypy .
        """
      }
    }

    stage('Run Tests') {
      container('python') {
        sh """
          . ${VENV_DIR}/bin/activate
          pytest --junitxml=report.xml
        """
      }
    }

    stage('Build Docker Image') {
      container('docker') {
        sh """
          docker build -t ${IMAGE_NAME} .
          docker push ${IMAGE_NAME}
        """
      }
    }

    stage('Deploy') {
      container('kubectl') {
        sh """
          kubectl create namespace demo
          kubectl create deployment python-web --image=python-web:latest -n demo
          kubectl create deployment python-web --image=nginx:latest -n demo
          kubectl expose deployment/python-web --port 8080 -n demo
        """
      }
    }

    stage('Post Deploy Test') {
      container('kubectl') {
        sh """
          # 你可以寫一個簡單的健康檢查，例如curl到service
          kubectl rollout status deployment/python-web -n demo
          curl -f http://python-web.demo.svc.cluster.local || exit 1
        """
      }
    }
  }
}
