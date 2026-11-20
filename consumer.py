"""Wyświetla zmiany PostgreSQL z topicu Debezium. Uruchom: python consumer.py"""
import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "shop.public.products",
    bootstrap_servers="localhost:9092",
    group_id="demo-consumer-v1",
    auto_offset_reset="earliest",
    value_deserializer=lambda raw: json.loads(raw.decode("utf-8")) if raw else None,
)

print("Nasłuchiwanie zmian w shop.public.products (Ctrl+C kończy)...")
try:
    for msg in consumer:
        if msg.value is None:
            print("[TOMBSTONE] Rekord z wartością null (kompakcja Kafka)")
            continue
        data = msg.value.get("payload", msg.value)
        op, before, after = data.get("op"), data.get("before"), data.get("after")
        if op == "r":
            print("[SNAPSHOT]", after)
        elif op == "c":
            print("[INSERT]", after)
        elif op == "u":
            print("[UPDATE] przed=", before, "po=", after)
        elif op == "d":
            print("[DELETE]", before)
        else:
            print("[OTHER]", data)
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
