#!/bin/bash

shopt -s dotglob

ROOT_DIR="${HOME}"/tfl-training-ml-control

if [ ! -d  "${ROOT_DIR}" ]; then
  echo "Code not found in ${ROOT_DIR}, copying it during entrypoint. With jupyterhub this should happen only once"
  mkdir "${ROOT_DIR}"
  cp -rf "${CODE_DIR}"/* "${ROOT_DIR}/"
  find notebooks -name '*.ipynb' -exec jupyter trust {} \;
fi

cd "${ROOT_DIR}" || exit

# original entrypoint, see https://github.com/jupyter/docker-stacks/blob/main/images/docker-stacks-foundation/Dockerfile#L131
# need -s option for tini to work properly when started not as PID 1
tini -s -g -- start.sh "$@"
