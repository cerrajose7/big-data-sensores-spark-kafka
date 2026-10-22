# Análisis de temperatura y humedad con Apache Spark y Kafka

## 1. Introducción

Este proyecto consiste en analizar datos de temperatura y humedad registrados por sensores de una cámara frigorífica, se utilizan Python, Apache Spark y Apache Kafka para realizar procesamiento por lotes (batch) y procesamiento en tiempo real.

## 2. Objetivo general

Analizar los registros de temperatura y humedad mediante herramientas de Big Data para obtener estadísticas, identificar valores extremos y visualizar el comportamiento de las mediciones.

## 3. Conjunto de datos

Se utilizó un conjunto de datos público de mediciones de temperatura y humedad de sensores de una cámara frigorífica, obtenido de Zenodo, se procesaron nueve archivos con un total de 1.411.515 registros.

## 4. Tecnologías utilizadas

- Python
- Apache Spark 3.5.8
- Apache Kafka 3.9.2
- Java 17
- Pandas y Matplotlib
- Ubuntu en VirtualBox

## 5. Archivos del proyecto

- `analisis_sensores.py`: procesamiento batch y estadísticas generales.
- `extremos_sensores.py`: identificación de valores extremos.
- `graficos_sensores.py`: generación de gráficos.
- `kafka_producer.py`: generación y envío de datos simulados a Kafka.
- `prueba_spark.py`: prueba de funcionamiento de Spark.
- `spark_streaming_consumer.py`: consumo y análisis de datos en tiempo real.

## 6. Resultados del procesamiento batch

Los resultados obtenidos fueron:

- Temperatura promedio: 9,56 °C.
- Temperatura mínima: 4,8 °C.
- Temperatura máxima: 42,2 °C.
- Humedad promedio: 76,65 %.
- Humedad mínima: 26,1 %.
- Humedad máxima: 99,9 %.

Se generaron gráficos de temperatura promedio, humedad promedio, evolución de la temperatura y relación entre temperatura y humedad.

## 7. Procesamiento en tiempo real

Se configuró el topic `sensor_data` en Kafka. Un productor genera datos simulados de temperatura y humedad, y una aplicación con Spark Streaming consume los mensajes y calcula estadísticas sobre los registros recibidos.

## 8. Instrucciones de ejecución

Para ejecutar el análisis batch desde la carpeta del proyecto:

```bash
/opt/spark/bin/spark-submit analisis_sensores.py
```

Para el procesamiento en tiempo real, se deben iniciar previamente los servicios de Kafka y ejecutar el productor y el consumidor de Spark Streaming según la configuración del entorno.

## 9. Referencias

- Apache Spark. https://spark.apache.org/
- Apache Kafka. https://kafka.apache.org/
- Zenodo. https://zenodo.org/

## 10. Jose Fernando Cerra Montes

Componente práctico de Big Data.
