#-------------- Base Image -------------------
FROM jupyter/minimal-notebook:python-3.10 as BASE

ARG CODE_DIR=/tmp/code
ARG POETRY_VERSION=1.8.2

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    CODE_DIR=$CODE_DIR

ENV PATH="${POETRY_HOME}/bin:$PATH"

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python - \
    && poetry self add poetry-plugin-export

USER ${NB_UID}

WORKDIR $CODE_DIR

COPY --chown=${NB_UID}:${NB_GID} poetry.lock pyproject.toml ./

RUN poetry export --no-interaction --no-ansi --with=docs --without=dev -f requirements.txt --output requirements.txt \
    && pip install --no-cache-dir --requirement requirements.txt

COPY --chown=${NB_UID}:${NB_GID} src/ src/
COPY --chown=${NB_UID}:${NB_GID} README.md .

# Build code
RUN poetry build

#-------------- Main Image -------------------
FROM jupyter/minimal-notebook:python-3.10 as MAIN

ARG CODE_DIR=/tmp/code

ENV DEBIAN_FRONTEND=noninteractive\
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    CODE_DIR=$CODE_DIR

# ENV PATH="${CODE_DIR}/.venv/bin:$PATH"

USER root

# pandoc needed for docs, see https://nbsphinx.readthedocs.io/en/0.7.1/installation.html?highlight=pandoc#pandoc
# gh-pages action uses rsync
# opengl and ffmpeg needed for rendering envs
RUN apt-get update \
    && apt-get -y --no-install-recommends install pandoc git-lfs rsync ffmpeg x11-xserver-utils \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

WORKDIR ${CODE_DIR}

# Copy conda directory from base image
COPY --from=BASE "${CONDA_DIR}" "${CONDA_DIR}"
# Copy built package from base image
COPY --from=BASE ${CODE_DIR}/dist ${CODE_DIR}/dist
# Install the built package
RUN pip install --no-cache-dir dist/*.whl
# Install kernel
RUN ipython kernel install --name "tfl-training-ml-control" --user

############## Start of HACK
# the home directory is overwritten by a mount when a jhub server is started off this image
# Thus, we create a jovyan-owned directory to which we copy the code and then move it to the home dir as part
# of the entrypoint
COPY --chown=${NB_UID}:${NB_GID} entrypoint.sh /usr/local/bin/

RUN chmod +x "/usr/local/bin/entrypoint.sh"
# Unfortunately, we cannot use ${CODE_DIR} in the ENTRYPOINT directive, so we have to hardcode it
# Keep in sync with the value of CODE_DIR above
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

############## End of HACK

WORKDIR "${CODE_DIR}"

# Copy notebooks
COPY --chown=${NB_UID}:${NB_GID} . .
# Trust all notebooks
RUN find notebooks -name '*.ipynb' -exec jupyter trust {} \;

WORKDIR "${HOME}"