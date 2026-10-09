# Демонстрация

Создайте учебные папки: `python3 -m src.fixtures`.
Откройте окно: `python3 -m src.main --vfs .generated/deep`.
Вводите команды из раздела проверки в README.

Автоматические сценарии: `sh scripts/stage2.sh`,
`sh scripts/stage3.sh`, `sh scripts/stage4.sh`, `sh scripts/stage5.sh`.
Скрипт stage3 очищает только учебный источник; stage4 создаёт его заново.

Для проверки ранних версий используйте соответствующий коммит из истории.

Смена владельца: `ls -l /readme.txt`, затем
`chown student:students /readme.txt` и повторный `ls -l /readme.txt`.
