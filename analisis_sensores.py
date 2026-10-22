
from pyspark.sql import SparkSession
from pyspark.sql.functions import min, max, avg, round, col, to_timestamp

spark = SparkSession.builder \
    .appName("AnalisisEstadisticoSensores") \
    .master("local[*]") \
    .getOrCreate()

ruta = "/home/vboxuser/bigdata_tarea3/datos/preprocessed/*.csv"

datos = spark.read \
    .option("header", True) \
    .option("inferSchema", False) \
    .option("sep", ";") \
    .csv(ruta)

datos = datos.withColumn(
    "Temperature", col("Temperature").cast("double")
).withColumn(
    "Humidity", col("Humidity").cast("double")
)

print("TOTAL DE REGISTROS:", datos.count())

print("\nCOLUMNAS DETECTADAS:")
datos.printSchema()

print("\nESTADISTICAS DE TEMPERATURA Y HUMEDAD")

datos.select(
    round(avg("Temperature"), 2).alias("Temperatura_promedio"),
    round(min("Temperature"), 2).alias("Temperatura_minima"),
    round(max("Temperature"), 2).alias("Temperatura_maxima"),
    round(avg("Humidity"), 2).alias("Humedad_promedio"),
    round(min("Humidity"), 2).alias("Humedad_minima"),
    round(max("Humidity"), 2).alias("Humedad_maxima")
).show(truncate=False)

print("\nPRIMEROS REGISTROS CON FECHA Y HORA:")
datos.select("Date", "Time", "Temperature", "Humidity").show(5, truncate=False)

spark.stop()

