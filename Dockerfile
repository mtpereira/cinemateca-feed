FROM ubuntu
MAINTAINER yourname
RUN sudo apt-get -y update
RUN sudo apt-get install -y python-yaml python-jinja2 git pip
RUN sudo pip install ansible
ADD deploy.yml ~/deploy.yml
ADD inventory ~/inventory
WORKDIR ~/
RUN ansible-playbook deploy.yml -c local -i ~/inventory
EXPOSE 22 3000
EXPOSE 8080 8080
