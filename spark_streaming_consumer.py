
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_json, from_unixtime, to_timestamp,
    window, avg, count
)
from pyspark.sql.types import (
    StructType, StructField, IntegerType,
    DoubleType, LongType
)

spark = SparkSession.builder \
    .appName("KafkaSparkStreamingSensores") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Estructura de los mensajes enviados por Kafka
schema = StructType([
    StructField("sensor_id", IntegerType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("timestamp", LongType(), True)
])

# Lectura de los datos en tiempo real desde Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor_data") \
    .option("startingOffsets", "latest") \
    .load()

# Convertir los mensajes JSON a columnas
datos = df.select(
    from_json(col("value").cast("string"), schema).alias("dato")
).select("dato.*")

# Convertir la marca de tiempo Unix a fecha y hora
datos = datos.withColumn(
    "event_time",
    to_timestamp(from_unixtime(col("timestamp")))
)

# Calcular estadísticas por sensor en ventanas de un minuto
estadisticas = datos \
    .withWatermark("event_time", "2 minutes") \
    .groupBy(
        window(col("event_time"), "1 minute"),
        col("sensor_id")
    ) \
    .agg(
        avg("temperature").alias("temperatura_promedio"),
        avg("humidity").alias("humedad_promedio"),
        count("*").alias("cantidad_registros")
    )

# Mostrar los resultados en la consola
consulta = estadisticas.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

consulta.awaitTermination()
