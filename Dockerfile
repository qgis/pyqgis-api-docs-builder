
# see https://docs.docker.com/docker-cloud/builds/advanced/
# using ARG in FROM requires min v17.05.0-ce
ARG QGIS_DOCKER_TAG=latest

FROM  qgis/qgis:${QGIS_DOCKER_TAG}
MAINTAINER Denis Rouzaud <denis@opengis.ch>

RUN curl https://bootstrap.pypa.io/get-pip.py | python3

WORKDIR /app

RUN apt-get update \
  && apt-get install -y graphviz

# Remove GRASS plugins that can't load (libgrass_gis not available) to avoid noisy warnings
RUN rm -f /usr/lib/qgis/plugins/libplugin_grass*.so /usr/lib/qgis/plugins/libprovider_grass*.so

RUN pip install --break-system-packages --upgrade sphinx-rtd-theme numpydoc

RUN mkdir /app/pyqgis
COPY . /app/pyqgis
WORKDIR /app/pyqgis
