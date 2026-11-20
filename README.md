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

## Troubleshooting
- `port is already allocated`: port 5432, 9092 lub 8083 jest zajęty przez inny proces.
- `connection refused` (Python): poczekaj aż Kafka wystartuje, sprawdź `docker compose ps` oraz `docker compose logs kafka`.
- Konektor nie jest `RUNNING`: `docker compose logs connect` i `curl.exe http://localhost:8083/connectors/shop-connector/status`.
- Jeśli po zmianie `init.sql` chcesz całkowicie odtworzyć bazę i stan: `docker compose down -v` i `docker compose up -d` (usuwa dane demo).
- Używamy uproszczonego formatu JSON (bez schema envelope), przy czym `NUMERIC` może mieć reprezentację zależną od ustawień konektora; w demo wypisujemy surowe dane.
- Uwaga: obrazy i hasła przeznaczone do lokalnego demo, nie do produkcji.

Źródła: https://debezium.io/documentation/reference/stable/connectors/postgresql.html oraz https://debezium.io/documentation/reference/stable/architecture.html
