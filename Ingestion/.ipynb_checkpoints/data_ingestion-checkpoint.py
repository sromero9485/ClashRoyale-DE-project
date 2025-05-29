import requests
import json 
from time import sleep, time

with open("token.txt", "r") as file:
    token = file.read().strip('\n')

base_url = "https://api.clashroyale.com/v1"

headers = {"Authorization": f"Bearer {token}"}

# Archivo donde guardaremos los resultados
output_file = "clanes_data.json"

# Lista de tags de clanes (ejemplo)
clan_tags = ["#2PP", "#8YL8Y9L", "#ABC123"]  # Reemplaza con tus tags reales

def get_clan_data(clan_tag):
    endpoint = f"/clans/{clan_tag.replace('#', '%23')}"  # Codificar el # como %23
    url = base_url + endpoint
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        sleep(0.1)  # Pequeña pausa para evitar rate limiting
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos del clan {clan_tag}: {e}")
        return None

def fetch_all_clans_data(tags, output_file):
    start_time = time()  # Iniciar medición de tiempo
    all_data = {}
    total_clans = len(tags)
    
    for i, tag in enumerate(tags, 1):
        print(f"Obteniendo datos del clan {tag} ({i}/{total_clans})...")
        clan_data = get_clan_data(tag)
        
        if clan_data is not None:
            all_data[tag] = clan_data
    
    # Guardar todos los datos
    with open(output_file, "w") as f:
        json.dump(all_data, f, indent=4)
    
    # Calcular tiempo transcurrido
    elapsed_time = time() - start_time
    mins, secs = divmod(elapsed_time, 60)
    
    print(f"\nProceso completado en {int(mins)} minutos y {secs:.2f} segundos")
    print(f"Datos de {len(all_data)}/{total_clans} clanes guardados en {output_file}")
    
    return all_data

# Ejecutar y medir tiempo
fetch_all_clans_data(clan_tags, output_file)