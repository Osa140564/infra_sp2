API_YAMDB

REST API проект для сервиса YaMDb — сбор отзывов о фильмах, книгах или музыке.

Описание

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен.

Как запустить проект:
  Клонируем репозиторий и переходим в него:
  Переходим в папку с файлом docker-compose.yaml:
  cd infra
  Поднимаем контейнеры (infra_db_1, infra_web_1, infra_nginx_1):
  docker-compose up -d --build
  Выполняем миграции:
  docker-compose exec web python manage.py makemigrations reviews
  docker-compose exec web python manage.py migrate
  Создаем суперпользователя:
  docker-compose exec web python manage.py createsuperuser
  Србираем статику:
  docker-compose exec web python manage.py collectstatic --no-input
  Создаем дамп базы данных (нет в текущем репозитории):
  docker-compose exec web python manage.py dumpdata > dumpPostrgeSQL.json
  Останавливаем контейнеры:
  docker-compose down -v
