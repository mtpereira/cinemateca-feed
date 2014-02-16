FROM ubuntu
MAINTAINER yourname
RUN apt-get -y update
RUN apt-get install -y python-yaml python-jinja2 git pip
RUN pip install ansible
ADD deploy.yml ~/deploy.yml
ADD inventory ~/inventory
WORKDIR ~/
RUN ansible-playbook deploy.yml -c local -i ~/inventory
EXPOSE 22 3000
EXPOSE 8080 8080
