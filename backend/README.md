source .venv/Scripts/activate -- for active env
uvicorn app.main:app --reload
alembic revision --autogenerate -m "create stock transactions table"
alembic upgrade head
docker exec -it smartretail-postgres psql -U postgres -d smartretail
\dt
ecr -login
Ollama server running hona chahiye. Agar nahi hai:

& "E:\Ollama\ollama.exe" serve

Is terminal ko open rehne do.

3. AI Engine wale terminal mein:

uvicorn app.main:app --reload --port 8001

4. Swagger kholo:

http://127.0.0.1:8001/docs

5. Pending pod test karo:

namespace:
default
pod_name:
smartretail-5dc89764b7-9qrvs

Uvicorn running on http://127.0.0.1:8000 --- for swaager pod

https://madhavisharma0023.atlassian.net/browse/SRAI-3

