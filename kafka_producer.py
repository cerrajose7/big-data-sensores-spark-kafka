
import time
import json
import random
from kafka import KafkaProducer

def generate_sensor_data():
    return {
        "sensor_id": random.randint(1, 9),
        "temperature": round(random.uniform(4.0, 15.0), 2),
        "humidity": round(random.uniform(26.0, 100.0), 2),
        "timestamp": int(time.time())
    }

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

print("Enviando datos de sensores a Kafka. Presiona Ctrl+C para detener.")

try:
    while True:
        sensor_data = generate_sensor_data()
        producer.send("sensor_data", value=sensor_data)
        producer.flush()
        print(f"Enviado: {sensor_data}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProductor detenido.")
finally:
    producer.close()
