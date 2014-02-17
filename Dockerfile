FROM ubuntu
MAINTAINER yourname
RUN sudo apt-get update
RUN sudo apt-get install -y python-yaml python-jinja2 git
RUN git clone http://github.com/ansible/ansible.git /tmp/ansible
WORKDIR /tmp/ansible
ENV PATH /tmp/ansible/bin:/sbin:/usr/sbin:/usr/bin
ENV ANSIBLE_LIBRARY /tmp/ansible/library
ENV PYTHONPATH /tmp/ansible/lib:$PYTHON_PATH
ADD deploy.yml ~/deploy.yml
ADD inventory ~/inventory
WORKDIR ~/
RUN ansible-playbook deploy.yml -c local -i ~/inventory
EXPOSE 22 3000
EXPOSE 8080 8080
