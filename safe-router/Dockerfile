FROM ubuntu:18.04

ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
ARG DEBIAN_FRONTEND=noninteractive 	

RUN apt-get update --fix-missing
RUN apt-get install -y wget \
	ca-certificates \
	build-essential \
	curl \
        debconf-utils \
	pkg-config \
	python3-dev \
	python3-pip \
	python3-setuptools \
	software-properties-common \
	llvm \
        rsyslog




RUN apt-get install --yes --no-install-recommends --allow-unauthenticated python3-matplotlib

RUN touch /etc/apt/sources.list.d/docker.list

# Populate the file with the to links to the graph-tool server
RUN echo "deb http://downloads.skewed.de/apt/bionic bionic universe" >> /etc/apt/sources.list.d/docker.list
RUN echo "deb-src http://downloads.skewed.de/apt/bionic bionic universe" >> /etc/apt/sources.list.d/docker.list

# Verify the package and update
RUN apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25
RUN apt-key list
RUN apt-get update
RUN apt-get install --yes --no-install-recommends --allow-unauthenticated python3-graph-tool

WORKDIR /var/app
COPY . .
COPY getRoute.py .
COPY utils.py .
COPY requirements.txt .
COPY my_graph.xml.gz .
COPY gunicorn_conf.py .


RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


EXPOSE 4000

# Start the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:4000", "--timeout","120", "--config","gunicorn_conf.py"]
