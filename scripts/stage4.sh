#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
python3 -m src.fixtures
python3 -m src.main --vfs .generated/deep \
  --script examples/stage4.txt --batch
if python3 -m src.main --vfs .generated/deep \
  --script examples/stage4-errors.txt --batch; then
  echo "Expected command errors" >&2
  exit 1
else
  status=$?
  test "$status" -eq 1
fi
