@echo off
cd /d "%~dp0.."
python -m src.main --vfs sample --script examples/stage2.txt --batch
python -m src.main --vfs sample --script examples/stage2-error1.txt --batch
python -m src.main --vfs sample --script examples/stage2-error2.txt --batch
python -m src.main --vfs sample --script examples/stage2-error3.txt --batch
python -m src.main --help
python -m src.main --batch
python -m src.main --script examples/stage2.txt --batch
python -m src.main --script missing-script.txt --batch
