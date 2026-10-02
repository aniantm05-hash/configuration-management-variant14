$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
python -m src.fixtures
python -m src.main --vfs .generated/deep --script examples/stage3.txt --batch
python -m src.main --vfs .generated/deep --script examples/stage3-error1.txt --batch
python -m src.main --vfs .generated/deep --script examples/stage3-error2.txt --batch
python -m src.main --help
python -m src.main --vfs .generated/minimal --script examples/load.txt --batch
python -m src.main --vfs .generated/files --script examples/load.txt --batch
python -m src.main --vfs .generated/deep --script examples/load.txt --batch
python -m src.main --vfs missing-vfs --batch
python -m src.main --vfs examples/load.txt --batch
