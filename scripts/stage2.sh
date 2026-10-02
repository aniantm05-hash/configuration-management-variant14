#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python3 -m src.fixtures || exit 1
failed=0
check() {
    expected=$1
    shift
    python3 -m src.main "$@"
    actual=$?
    if [ "$actual" -ne "$expected" ]; then
        echo "FAIL: expected $expected, got $actual" >&2
        failed=1
    fi
}
check 0 --vfs .generated/deep --script examples/stage2.txt --batch
check 1 --vfs .generated/deep --script examples/stage2-error1.txt --batch
check 1 --vfs .generated/deep --script examples/stage2-error2.txt --batch
check 1 --vfs .generated/deep --script examples/stage2-error3.txt --batch
check 0 --help
check 0 --batch
check 0 --script examples/stage2.txt --batch
check 1 --script missing-script.txt --batch
check 1 --vfs missing-vfs --batch
check 2 --unknown-option
exit "$failed"
