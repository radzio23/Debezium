# Debezium CDC — demo

Wymaga: Docker Desktop, Docker Compose, Python 3.10+.

## 1. Start kontenerów
```powershell
docker compose up -d
docker compose ps
```
Poczekaj, aż Kafka Connect będzie dostępny (np. `curl.exe http://localhost:8083/`).

## 2. Rejestracja konektora
```powershell
curl.exe -X POST http://localhost:8083/connectors -H "Content-Type: application/json" --data-binary "@connector.json"
curl.exe http://localhost:8083/connectors/shop-connector/status
```
Stan konektora i taska powinien wynosić `RUNNING`. Jeżeli Connect jeszcze startuje, ponów polecenie.

## 3. Python consumer
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python consumer.py
```
Pierwsze zdarzenie (op=r) pochodzi ze snapshotu danych inicjalnych.

## 4. Drugie okno terminala: SQL
```powershell
docker compose exec postgres psql -U demo -d shop
```
W psql wykonaj pojedynczo:
```sql
INSERT INTO products(name, price) VALUES ('Laptop Lenovo', 3500);
UPDATE products SET price = 2999 WHERE name = 'Laptop Lenovo';
DELETE FROM products WHERE name = 'Laptop Lenovo';
```
Zobacz w terminalu Pythona `INSERT`, `UPDATE` i `DELETE`.

Źródła: https://debezium.io/documentation/reference/stable/connectors/postgresql.html oraz https://debezium.io/documentation/reference/stable/architecture.html
