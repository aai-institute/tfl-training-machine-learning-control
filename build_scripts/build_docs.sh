#!/usr/bin/env bash

set -euo pipefail

function usage() {
  cat > /dev/stdout <<EOF
Usage:
  build_docs.sh [FLAGS]

  Updates and builds the documentation. In order to include the executed notebooks
  into the documentation, it is recommended to execute them and push them first.

  Optional flags:
    -h, --help              Show this information and exit
    --cleanup               Clean up html files in the docs/_static directory before building the docs.
                            Use with caution, these files are typically committed to the repository.
    --skip-nb-validation    Skip the validation of the notebooks. You should only use this if you know what you
                            are doing.
EOF
}


EXECUTE_FLAG=""
CLEANUP=false
VALIDATE_NB=true

while [[ $# -gt 0 ]]
do
  key="$1"
  case $key in
      --cleanup)
        CLEANUP=true
        shift
      ;;
      --skip-nb-validation)
        VALIDATE_NB=false
        shift
      ;;
      -h|--help)
        usage
        exit 0
      ;;
      -*)
        >&2 echo "Unknown option: $1"
        usage
        exit 255
      ;;
      *)
        >&2 echo "This script takes no positional arguments but got: $1"
        exit 255
      ;;
  esac
done


BUILD_DIR=$(dirname "$0")

(
  cd "${BUILD_DIR}/.." || (echo "Unknown error, could not find directory ${BUILD_DIR}" && exit 255)
  source build_scripts/utils.sh

  if [ "$CLEANUP" = true ] ; then
    echo "Cleaning up html files"
    jupyter book clean --all .
  fi

  if [ "$VALIDATE_NB" = true ] ; then
      echo "Validating notebooks"
      # from utils.sh
      check_notebooks_for_non_executed_load
  fi

  echo "Building documentation with jupyter-book"
  jupyter-book build . --verbose --all
)
