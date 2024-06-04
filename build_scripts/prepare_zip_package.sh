#!/usr/bin/env bash

set -euo pipefail

function usage() {
  cat > /dev/stdout <<EOF
Usage:
  prepare_zip_package.sh [FLAGS]

  Prepares the zip package for the training. Will also run jupyter-book and include
  the rendered notebooks in the zip package.

  Optional flags:
    -h, --help              Show this information and exit
EOF
}

while [[ $# -gt 0 ]]
do
  key="$1"
  case $key in
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

  echo "Validating build prerequisites..."

  check_notebooks_for_non_executed_load

  echo "Building exercise notebooks with jupyter-book..."
  bash build_scripts/build_docs.sh
  echo "Done"

  echo "Done. Building the zip package..."

  echo "Adding source files to training_ml_control_content.zip"
  git archive --output=./training_ml_control_content.zip --format=zip HEAD
  echo "Adding documentation in html to training_ml_control_content.zip"
  zip -ur training_ml_control_content.zip _build/html
  echo "Done"
)