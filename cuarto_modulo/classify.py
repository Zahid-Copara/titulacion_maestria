import google.generativeai as genai
import os
import pandas as pd
import time
# --------------------------------------------------
#                   GLOBAL VARIABLES
# --------------------------------------------------
actual_directory = os.getcwd()
genai.configure(api_key="")
excel_file = actual_directory+'\\input\\result\\doc_file.xlsx'
files_path = actual_directory+"\\input\\result"
final_results = []
# ------------------------------------------------------------------
#                     LOG CONFIGURATION
# ------------------------------------------------------------------
import logging as log
from pythonjsonlogger import jsonlogger
log_directory=actual_directory+'\\logs'
# log agent initialization
def init_logger(file):
    global handler, logger
    handler = log.FileHandler(file)
    format_str = '%(levelname)s%(asctime)s%(filename)s%(funcName)s%(lineno)d%(message)'
    formatter = jsonlogger.JsonFormatter(format_str)
    handler.setFormatter(formatter)
    logger = log.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(log.DEBUG)
    return logger
# log agent termination
def stop_logger():
    logger.removeHandler(handler)
    handler.close()
# log agent definition
logger = init_logger(log_directory+'\\logs-privacy-policy.log')
# Read CSV file
def read_excel():
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        reason = 'error while reading excel file'
        logger.error("error on pandas library", 
                     extra={'exception_message':str(e), 'reason':reason})
    else:
        return df
# Define function to get the text
def get_response(prompt,model='gemini-1.0-pro-latest'):
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
    except Exception as e:
        reason = 'error while using Gemini service'
        logger.error("error on Gemini", 
                     extra={'exception_message':str(e), 'reason':reason})
        return 'NO RESPUESTA'
    else:
        if response.text == 'SI' or response.text == 'NO':
            return response.text
        else:
            return ''
# Function to read local path and extract text
def extract_data(filename):
    try:
        privacyPolicyText = ''
        current_file = files_path+'\\'+filename+'.txt'
        if not os.path.isfile(current_file):
            logger.error(f"file '{filename}'.txt not found")
        with open(current_file, 'r', encoding='utf-8') as file:
            privacyPolicyText = file.read()
    except Exception as e:
        reason = 'error in extract data '
        logger.error("error in filename", 
                     extra={'exception_message':str(e), 'reason':reason})
    else:
        return privacyPolicyText
# Function to check if a string is null or empty
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
# Function that process dataset information
def process_dataset(dataset):
    results=[]
    count = 0
    try:
        for index, row in dataset.iterrows():
            row_num = dataset.shape[0]
            nombreApp = row['nombre_app']
            categoria = row['categoria']
            numeroDescargas = row['numero_descargas']
            packageName = row['package_name']
            ubicacion = row['ubicacion']
            privacyPolicyUrl = row['policy_privacy_url']
            archivoPolitica = row['policy_privacy_name']
            if isNullorEmpty(archivoPolitica) == False:
                privacyPolicyText = extract_data(archivoPolitica)
                if isNullorEmpty(privacyPolicyText) == False:
                    prompt = f"Necesito que me digas si el siguiente texto en comillas puede clasificarse en SI o NO con respecto a que es una politica de privacidad, lo unico que quiero es que me digas la respuesta directa es decir SI o NO, a continuación la política '{privacyPolicyText}'"
                    policyPrivacyClassification = get_response(prompt)
                    if policyPrivacyClassification:
                        results.append((nombreApp, categoria, numeroDescargas, packageName, ubicacion, archivoPolitica, privacyPolicyUrl, policyPrivacyClassification))
                    else:
                        logger.error("error while receiving gemini info")
                        print("No response from gemini")
                        results.append((nombreApp, categoria, numeroDescargas, packageName, ubicacion, archivoPolitica, privacyPolicyUrl, 'NO RESPUESTA'))
                    time.sleep(5)
                else:
                    results.append((nombreApp, categoria, numeroDescargas, packageName, ubicacion, archivoPolitica, privacyPolicyUrl, 'NO PRESENTA'))
            else:
                results.append((nombreApp, categoria, numeroDescargas, packageName, ubicacion, archivoPolitica, privacyPolicyUrl, 'NO PRESENTA'))
            count = count + 1
            print(f"{count}/{row_num} processed!")
    except Exception as e:
        reason = 'error while proccesing dataset'
        logger.error("error in processing dataset", 
                     extra={'exception_message':str(e), 'reason':reason})
        results.append((nombreApp, categoria, numeroDescargas, packageName, ubicacion, archivoPolitica, privacyPolicyUrl, 'NO RESPUESTA'))
    else: 
        return results
def save_dataset(results):
    results_df = pd.DataFrame(results, columns=['nombre_app','categoria','numero_descargas','package_name', 'ubicacion', 'policy_privacy_url', 'policy_privacy_name','is_policy_privacy'])
    output_file = actual_directory+'\\aplicaciones_clasificadas.xlsx'
    results_df.to_excel(output_file, index=False)
def main():
    print('Initializing program')
    data_set = read_excel()
    num_rows = data_set.shape[0]
    print(f"There are {num_rows} rows!")
    logger.info('Program has been initialized')
    final_results = process_dataset(data_set)
    save_dataset(final_results)
    logger.info('Program has finished!')

main()
logger = stop_logger()