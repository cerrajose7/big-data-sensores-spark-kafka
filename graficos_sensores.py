import os
import glob
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

carpeta_datos = "datos/preprocessed"
carpeta_resultados = "resultados"

os.makedirs(carpeta_resultados, exist_ok=True)

archivos = sorted(
    glob.glob(os.path.join(carpeta_datos, "*.csv"))
)

if not archivos:
    print("No se encontraron archivos CSV en", carpeta_datos)
    raise SystemExit(1)

lista_datos = []

for archivo in archivos:
    try:
        df = pd.read_csv(archivo, sep=";")
        df.columns = df.columns.str.strip()

        requeridas = ["Date", "Time", "Temperature", "Humidity"]
        if not all(col in df.columns for col in requeridas):
            print("Se omite archivo por columnas diferentes:", archivo)
            continue

        df["sensor"] = os.path.basename(archivo).replace(
            "_preprocessed.csv", ""
        )
        df["fecha_hora"] = pd.to_datetime(
            df["Date"].astype(str) + " " + df["Time"].astype(str),
            dayfirst=True,
            errors="coerce"
        )
        df["Temperature"] = pd.to_numeric(
            df["Temperature"], errors="coerce"
        )
        df["Humidity"] = pd.to_numeric(
            df["Humidity"], errors="coerce"
        )
        lista_datos.append(df)

    except Exception as error:
        print("Error leyendo", archivo, ":", error)

if not lista_datos:
    print("No se pudieron cargar datos válidos.")
    raise SystemExit(1)

datos = pd.concat(lista_datos, ignore_index=True)
datos = datos.dropna(
    subset=["fecha_hora", "Temperature", "Humidity"]
)

# Gráfico 1: temperatura promedio por sensor
temperatura = datos.groupby("sensor")["Temperature"].mean()
plt.figure(figsize=(10, 6))
temperatura.plot(kind="bar")
plt.title("Temperatura promedio por sensor")
plt.xlabel("Sensor")
plt.ylabel("Temperatura (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(carpeta_resultados, "temperatura_promedio.png"))
plt.close()

# Gráfico 2: humedad promedio por sensor
humedad = datos.groupby("sensor")["Humidity"].mean()
plt.figure(figsize=(10, 6))
humedad.plot(kind="bar")
plt.title("Humedad promedio por sensor")
plt.xlabel("Sensor")
plt.ylabel("Humedad (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(carpeta_resultados, "humedad_promedio.png"))
plt.close()

# Gráfico 3: evolución temporal de la temperatura
evolucion = datos.sort_values("fecha_hora")
plt.figure(figsize=(12, 6))
for sensor, grupo in evolucion.groupby("sensor"):
    plt.plot(
        grupo["fecha_hora"],
        grupo["Temperature"],
        label=sensor,
        linewidth=0.7
    )
plt.title("Evolución de la temperatura de los sensores")
plt.xlabel("Fecha")
plt.ylabel("Temperatura (°C)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(carpeta_resultados, "evolucion_temperatura.png"))
plt.close()

# Gráfico 4: relación entre temperatura y humedad
plt.figure(figsize=(10, 6))
plt.scatter(datos["Temperature"], datos["Humidity"], s=3)
plt.title("Relación entre temperatura y humedad")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Humedad (%)")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_resultados, "temperatura_humedad.png"))
plt.close()

print("Gráficos creados correctamente:")
for archivo in sorted(glob.glob(os.path.join(carpeta_resultados, "*.png"))):
    print(archivo)
