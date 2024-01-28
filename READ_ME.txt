Nizomiddinga :
Blog, About, terms, subscribe, Search
Abdullohga:
Account info, filter, sort by
Mahliyo:
add to cart, Cart, Download
Isomiddin:
License, contact, submit free templates, Reviews, discussion

.env ga qo'shish kerak bo'lgan ma'lumotlar
SENDER_EMAIL = email
SMTP_CODE = code => 16 talik smtp cod


postgresql ni to'xtataish kk =============================

sudo systemctl stop postgresql

docker run >>> ============================
sudo docker compose up --build




docker migratsiya qilish >>> ================================

sudo docker-compose -f docker-compose.yml exec fastapi alembic revision --autogenerate -m "YourMigrationMessage"

sudo docker-compose -f docker-compose.yml exec fastapi alembic upgrade head



.env ==============================================

POSTGRES_HOST = db

DB ni hammasini POSTGRES ga almashtirish kerak

