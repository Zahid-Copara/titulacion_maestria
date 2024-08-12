import pandas as pd

# Leer el archivo Excel
df = pd.read_excel('resultado_permisos.xlsx')

# Leer el archivo TXT con los datos sensibles
with open('permisos_sensibles.txt', 'r') as file:
    datos_sensibles = file.read().splitlines()

# Crear una columna que indica si la aplicación recolecta algún dato sensible
def check_permission(group):
    for data in group['permission']:
        if data in datos_sensibles:
            return 'SI'
    return 'NO'

# Aplicar la función a cada grupo de aplicaciones
df_result = df.groupby('apk').apply(check_permission).reset_index()
df_result.columns = ['apk', 'permission']

# Guardar el resultado en un nuevo archivo Excel
df_result.to_excel('resultados.xlsx', index=False)

print("El archivo 'resultados.xlsx' ha sido creado con éxito.")
