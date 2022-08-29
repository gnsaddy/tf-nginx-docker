FROM jenkins/jenkins:lts-jdk11
USER root
RUN apt update && \
    apt install -y --no-install-recommends gnupg curl ca-certificates apt-transport-https && \
    curl -sSfL https://apt.octopus.com/public.key | apt-key add - && \
    sh -c "echo deb https://apt.octopus.com/ stable main > /etc/apt/sources.list.d/octopus.com.list" && \
    apt update && apt install -y octopuscli

RUN jenkins-plugin-cli --plugins octopusdeploy:3.1.6

# install wget and unzip
RUN apt-get update && apt-get install -y wget unzip

# install terraform
RUN wget https://releases.hashicorp.com/terraform/1.2.8/terraform_1.2.8_linux_amd64.zip
RUN unzip terraform_1.2.8_linux_amd64.zip
RUN mv terraform /usr/local/bin/
RUN rm terraform_1.2.8_linux_amd64.zip

USER jenkins