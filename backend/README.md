source .venv/Scripts/activate -- for active env
uvicorn app.main:app --reload
alembic revision --autogenerate -m "create stock transactions table"
alembic upgrade head
docker exec -it smartretail-postgres psql -U postgres -d smartretail
\dt
ecr -login
