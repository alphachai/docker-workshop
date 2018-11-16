FROM python:3.6-slim-stretch

# *  Ensure that Python outputs everything that's printed inside
#    the application rather than buffering it.
# *  Also don't cache pip packages (pip uses falsey values like 0 to indicate a flag is set).
ENV APP_DIR=/app \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=0

# Expose the gunicorn port.
EXPOSE 80

# Set up health check.
HEALTHCHECK CMD curl -f http://127.0.0.1/health-check/ || exit 1

VOLUME ["/etc/nginx/conf.d", "/static"]

WORKDIR ${APP_DIR}

ARG BUILD_DEPS=" \
    apt-utils \
    gcc \
    g++ \
    gosu \
    lsb-release \
"

# Add package management scripts
COPY docker/install_packages.sh /usr/bin/install_packages
COPY docker/upgrade_packages.sh /usr/bin/upgrade_packages
COPY docker/remove_packages.sh /usr/bin/remove_packages

COPY config/dpkg/01_nodoc /etc/dpkg/dpkg.cfg.d/01_nodoc
COPY Pipfile Pipfile.lock ./

# Install dependencies & clean.
RUN install_packages $BUILD_DEPS python-psycopg2

RUN pip install -U pipenv
RUN pipenv install --deploy --system

RUN rm Pipfile Pipfile.lock
RUN pip uninstall -y pipenv
RUN remove_packages $BUILD_DEPS

# Copy service files
COPY . .
COPY docker/docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
