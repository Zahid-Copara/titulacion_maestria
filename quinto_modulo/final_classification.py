import pandas as pd

# Leer los datasets desde los archivos Excel
privacy_policy_classification = pd.read_excel('privacy_policy_classification.xlsx')
collected_data = pd.read_excel('collected_data.xlsx')
permission_data = pd.read_excel('resultados_permission.xlsx')

# Renombrar la columna 'apk' a 'package_name' en el dataset 'collected_data' para poder hacer el merge
collected_data = collected_data.rename(columns={'apk': 'package_name'})
permission_data = permission_data.rename(columns={'apk': 'package_name'})

# Realizar el merge de los datasets basado en 'package_name'
merged_data_collected = pd.merge(privacy_policy_classification, collected_data, on='package_name', how='left')

# Rellenar los valores faltantes en 'recolect_personal_data' con 'NO'
merged_data_collected['recolect_personal_data'] = merged_data_collected['recolect_personal_data'].fillna('NO')

# Realizar el merge del dataset resultante basado en 'package_name'
merged_data = pd.merge(merged_data_collected, permission_data, on='package_name', how='left')

# Rellenar los valores faltantes en 'permission' con 'NO'
merged_data['permission'] = merged_data['permission'].fillna('NO')

# Crear la columna 'cumple_lopd' con las condiciones especificadas
def cumple_lopd(row):
    if row['recolect_personal_data'] == 'NO' and row['permission'] == 'NO':
        if row['is_policy_privacy'] == 'SI':
            return 'NO APLICA'
        elif row['is_policy_privacy'] == 'NO' or row['is_policy_privacy'] == 'NO PRESENTA':
            return 'NO APLICA'
    
    if row['recolect_personal_data'] == 'NO' and row['permission'] == 'SI':
        if row['is_policy_privacy'] == 'SI':
            return 'NO'
        elif row['is_policy_privacy'] == 'NO':
            return 'NO'
        elif row['is_policy_privacy'] == 'NO PRESENTA':
            return 'NO'
    
    if row['recolect_personal_data'] == 'SI' and row['permission'] == 'NO':
        if row['is_policy_privacy'] == 'SI':
            return 'SI'
        elif row['is_policy_privacy'] == 'NO' or row['is_policy_privacy'] == 'NO PRESENTA':
            return 'NO'
    
    if row['recolect_personal_data'] == 'SI' and row['permission'] == 'SI':
        if row['is_policy_privacy'] == 'SI':
            return 'SI'
        elif row['is_policy_privacy'] == 'NO' or row['is_policy_privacy'] == 'NO PRESENTA':
            return 'NO'
    
    return 'NO APLICA'

merged_data['cumple_lopd'] = merged_data.apply(cumple_lopd, axis=1)

# Guardar el resultado en un nuevo archivo Excel
merged_data.to_excel('resultados.xlsx', index=False)

print("El archivo 'resultados.xlsx' ha sido creado exitosamente.")
