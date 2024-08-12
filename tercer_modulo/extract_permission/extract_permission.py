import pandas as pd
import re

# Check if a row is null or empty
def isNullorEmpty(s):
    salida = True
    if s is None:
        salida = True
    elif not s:
        salida = True
    else:
        salida = False
    if pd.notna(s) == False:
        salida = True
    if s == "null\n":
        salida = True
    return salida

# Leer el archivo Excel
file_path = "UPM_Download_logs.xlsx"
df = pd.read_excel(file_path)

# Crear listas para almacenar los resultados
apk_list = []
permissions_list = []

# Iterar sobre las filas del DataFrame
for index, row in df.iterrows():
    apk = row['apk']
    metadata = row['metadata_details']
    if isNullorEmpty(metadata) == False:
        
        pattern = re.compile(r'permission": \[(.*?)\]', re.DOTALL)
        match = pattern.search(metadata.replace("'",'"'))

        if match:
            permissions_text = match.group(1)
            permissions = [perm.strip().strip('"') for perm in permissions_text.split(',')]

        # Agregar a las listas
        for permission in permissions:
            permission_result = permission.split('.')
            apk_list.append(apk)
            permissions_list.append(permission_result[-1])

# Crear un nuevo DataFrame con los resultados
result_df = pd.DataFrame({
    'apk': apk_list,
    'permission': permissions_list
})

# Guardar el DataFrame en un nuevo archivo Excel
result_file_path = "resultado_permisos.xlsx"
result_df.to_excel(result_file_path, index=False)

print("El archivo 'resultado_permisos.xlsx' ha sido creado exitosamente.")
