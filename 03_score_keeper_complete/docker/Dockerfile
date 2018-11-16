FROM python:3.6-slim-stretch

ARG ENVIRONMENT=dev
ARG LOG_LEVEL=INFO
ARG GIT_HASH=
ARG JENKINS_BUILD=
ARG API_VERSION=
ARG EVEREST_ENVIRONMENT=

ENV APP_DIR=/app \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=0 \
    EVEREST_GIT_HASH=${GIT_HASH} \
    API_VERSION=${API_VERSION} \
    EVEREST_JENKINS_BUILD=${JENKINS_BUILD} \
    EVEREST_ENVIRONMENT=${ENVIRONMENT} \
    EVEREST_LOG_LEVEL=${LOG_LEVEL} \
    APP_COMMIT=${GIT_HASH} \
    APP_ENVIRONMENT=${EVEREST_ENVIRONMENT} \
    APP_RELEASE=${API_VERSION} \
    DJANGO_SETTINGS_MODULE=config.settings \
    DJANGO_STATIC_ROOT=/static \
    LD_LIBRARY_PATH=/usr/lib

# Expose the gunicorn port.
EXPOSE 80

# Set up health check.
HEALTHCHECK CMD curl -f http://127.0.0.1/health-check/ || exit 1

VOLUME ["/etc/nginx/conf.d", "${DJANGO_STATIC_ROOT}"]

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
RUN set -ex \
    && install_packages $BUILD_DEPS \
        python-psycopg2 \
        > /dev/null 2>&1 \
    && pip install -U pipenv \
    && pipenv install --deploy --system \
    && rm Pipfile Pipfile.lock \
    && pip uninstall -y pipenv \
    && remove_packages $BUILD_DEPS > /dev/null 2>&1 \
    && apt-get clean \
    && rm -rf \
        $APP_DIR/.cache \
        $APP_DIR/reports \
        /usr/games \
        /usr/lib/debug \
        /usr/lib/gcc \
        /usr/local/share/.cache \
        /usr/share/doc/ \
        /usr/share/info \
        /usr/share/lintian \
        /usr/share/man/ \
        /var/lib/apt/lists/ \
        /var/log/* \
        /var/tmp/* \
        /tmp/*

# Copy service files
COPY . .
COPY docker/docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

# Upgrade system packages to get latest security updates.
RUN set -ex \
    upgrade_packages \
    && apt-get clean \
    && rm -rf \
        /var/cache/
