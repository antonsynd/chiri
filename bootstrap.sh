#!/usr/bin/env sh
set -eux -o pipefail

./build_tools/bin/build_chiri install

echo "Add ~/.chiri/bin to PATH"
