### build docker image with name 'jenkins' and tag 'latest'
docker build -t jenkins:latest .

### run docker image with name 'jenkins' and tag 'latest'
docker run -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins:latest