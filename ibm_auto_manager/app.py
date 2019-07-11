######################
#  IBM-Auto-Manager  #
######################

# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import os
import json
import getpass

# ----- Functions -----
def cls():
  os.system('cls' if os.name=='nt' else 'clear')

def config(settings):
  """ Obtenemos la configuración de la app desde el fichero solicitado. 
    En caso de que no exista, solictamos los datos mínimos y lo creamos."""

  if os.path.isfile('./ibm_auto_manager/config/settings.json'):
    print("[config] Encontrado fichero configuración")

    with open('./ibm_auto_manager/config/settings.json') as settings_file:
      settings = json.load(settings_file)
    settings_file.close

    print("[config] Configuración cargada con éxito")
  else :
    print("[config] ! No se encuentra fichero de configuración")
    
    settings['mongodb'] = ""
    while settings['mongodb'] == "":
      settings['mongodb'] = input(" Introduce la cadena de conexión a la BD: ")
    settings['proxy'] = input(" Introduce la cadena del proxy (opcional): ")

    settings['user'] = {}
    settings['user']['alias'] = ""
    while settings['user']['alias'] == "":
      settings['user']['alias'] = input(" Introduce tu Alias del juego: ")
    settings['user']['password'] = ""
    while settings['user']['password'] ==  "":
      settings['user']['password'] = getpass.getpass(" Introduce tu Password: ")
    
    # Creamos el fichero de configuración
    print("[config] Fichero de configuración creado con éxito")

    with open('./ibm_auto_manager/config/settings.json', 'w') as settings_file:
      json.dump(settings, settings_file, indent=4, ensure_ascii=False)
    settings_file.close

    print("[config] Configuración cargada con éxito")
  
  # Aplicamos la configuración
  if settings['proxy'] != "":
    os.environ['http_proxy'] = settings['proxy'] 
    os.environ['HTTP_PROXY'] = settings['proxy']
    os.environ['https_proxy'] = settings['proxy']
    os.environ['HTTPS_PROXY'] = settings['proxy']

  print("[config] Configuración aplicada con éxito")
  input(" Pulse para continuar...")


# =====================
#     -- Start --
# =====================
def run():
  
  cls()

  # Obtenemos la configuración
  settings = {}
  config(settings)
  cls()
    