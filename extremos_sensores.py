
from pyspark.sql import SparkSession
from pyspark.sql.functions import max as spark_max, col, input_file_name

spark = SparkSession.builder \
    .appName("ValoresExtremosSensores") \
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
).withColumn(
    "archivo", input_file_name()
)

print("\nREGISTROS CON LA TEMPERATURA MAS ALTA:")

max_temp = datos.agg(
    spark_max("Temperature").alias("maximo")
).first()["maximo"]

datos.filter(col("Temperature") == max_temp) \
    .select("archivo", "Date", "Time", "Temperature", "Humidity") \
    .show(20, truncate=False)

print("\nREGISTROS CON LA HUMEDAD MAS ALTA:")

max_humedad = datos.agg(
    spark_max("Humidity").alias("maximo")
).first()["maximo"]

datos.filter(col("Humidity") == max_humedad) \
    .select("archivo", "Date", "Time", "Temperature", "Humidity") \
    .show(20, truncate=False)

spark.stop()

