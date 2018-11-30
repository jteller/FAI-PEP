#!/bin/bash

set -ex

BAZEL_DIR=/tmp/bazel
BAZEL=bazel-0.18.1-installer-linux-x86_64.sh
REPO_DIR=/tmp/tensorflow

sudo apt-get -y install wget pkg-config g++ zlib1g-dev python zip unzip
if [ ! -z ${BAZEL_DIR} ]; then
  mkdir -p ${BAZEL_DIR}
fi
if [ ! -f ${BAZEL_DIR}/${BAZEL} ]; then
  wget -q -O ${BAZEL_DIR}/${BAZEL} https://github.com/bazelbuild/bazel/releases/download/0.18.1/${BAZEL}
fi
chmod +x ${BAZEL_DIR}/${BAZEL}
${BAZEL_DIR}/${BAZEL} --user
export PATH="$PATH:$HOME/bin"

rm -rf ${REPO_DIR}
git clone --recursive --quiet https://github.com/tensorflow/tensorflow.git "$REPO_DIR"