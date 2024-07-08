
# see https://docs.docker.com/docker-cloud/builds/advanced/
# using ARG in FROM requires min v17.05.0-ce
ARG QGIS_DOCKER_TAG=latest

FROM  qgis/qgis:${QGIS_DOCKER_TAG}
MAINTAINER Denis Rouzaud <denis@opengis.ch>

RUN curl https://bootstrap.pypa.io/get-pip.py | python3

WORKDIR /root

RUN pip install --break-system-packages --upgrade sphinx-rtd-theme numpydoc

RUN mkdir /root/pyqgis
COPY . /root/pyqgis
WORKDIR /root/pyqgis
