import pandas as pd

# Leer el archivo Excel
df = pd.read_excel('Resultado_UPM_Labels.xlsx')

# Leer el archivo TXT con los datos sensibles
with open('data_collected.txt', 'r') as file:
    datos_sensibles = file.read().splitlines()

# Crear una columna que indica si la aplicación recolecta algún dato sensible
def check_sensitive_data(group):
    for data in group['type_data_collected']:
        if data in datos_sensibles:
            return 'SI'
    return 'NO'

# Aplicar la función a cada grupo de aplicaciones
df_result = df.groupby('apk').apply(check_sensitive_data).reset_index()
df_result.columns = ['apk', 'recolect_personal_data']

# Guardar el resultado en un nuevo archivo Excel
df_result.to_excel('resultados.xlsx', index=False)

print("El archivo 'resultados.xlsx' ha sido creado con éxito.")
