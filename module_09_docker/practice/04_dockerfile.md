## 9.4

1. Добавьте в ответ от сервиса имя админа, который занимается его поддержкой. Чтобы знать, к кому бежать в случае чего. Тут как нельзя кстати будет указать это через переменную окружения. Запустите несколько экземпляров приложения с разными именами. Проверьте, что всё работает.
2. Попробуйте удалить команду `RUN mkdir /app` из `Dockerfile`. Проверьте, что всё работает. Ответьте себе на вопрос: почему?
3. Разбейте `Dockerfile` на два: первый (базовый), где вы установите все зависимости, и второй, где вы используете первый как базовый, и продолжите установку сервиса: копирование файла с приложением и определение точки входа.

Это задание не нужно отправлять на проверку.