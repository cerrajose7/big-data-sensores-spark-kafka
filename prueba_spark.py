from pyspark.sql import SparkSession

spark = SparkSession.builder \
.appName("PruebaDatosSensores") \
.master("local[*]") \
.getOrCreate()

ruta = "/home/vboxuser/bigdata_tarea3/datos/preprocessed/*.csv"

df = spark.read.option("header", True).option("inferSchema", True).csv(ruta)

print("Cantidad de registros:", df.count())
print("Columnas encontradas:")
df.printSchema()

print("Primeros registros:")
df.show(5, truncate=False)

spark.stop()
