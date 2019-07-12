######################
#  IBM-Auto-Manager  #
######################

# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import os
import time
import json
import getpass

from bs4 import BeautifulSoup
from pymongo import MongoClient

from ibm_auto_manager.common.util import cls, show
from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.general import profile

# ----- Functions -----
def config():
  """ Obtenemos la configuración de la app desde el fichero solicitado. 
    En caso de que no exista, solictamos los datos necesarios y lo creamos."""
  
  settings = {}
  if os.path.isfile('./ibm_auto_manager/config/settings.json'):
    print(show("config") + "Encontrado fichero configuración")

    with open("./ibm_auto_manager/config/settings.json", "r") as settings_file:
      settings = json.load(settings_file)
    settings_file.close

    print(show("config") + "Configuración cargada con éxito")
  else :
    print(show("config") + "! No se encuentra fichero de configuración")
    print(show("config") + "! Se va a proceder a generar el fichero")
    print(show("config") + "! Se realizaran múltiples preguntas")
    
    print("\n" + show("config") + "Configuración de conexión")
    settings["mongodb"] = ""
    while settings["mongodb"] == "":
      settings["mongodb"] = input(" Introduce la cadena de conexión a la BD: ")
    settings["proxy"] = input(" Introduce la cadena del proxy (opcional): ")

    print("\n" + show("config") + "Configuración de usuario")
    settings["user"] = {}
    settings["user"]["alias"] = ""
    while settings["user"]["alias"] == "":
      settings["user"]["alias"] = input(" Introduce tu Alias del juego: ")
    settings["user"]["password"] = ""
    while settings["user"]["password"] ==  "":
      settings["user"]["password"] = getpass.getpass(" Introduce tu Password: ")

    print("\n" + show("config") + "Configuración de automatización (Tienda)")
    settings["shop"] = {}
    settings["shop"]["llaveros"] = input(" Introduce cantidad de Llaveros (6400): ") or "6400"
    settings["shop"]["banderolas"] = input(" Introduce cantidad de Banderolas (6400): ") or "6400"
    settings["shop"]["balones"] = input(" Introduce cantidad de Balones (6400): ") or "6400"
    settings["shop"]["camisetas"] = input(" Introduce cantidad de Camisetas (6400): ") or "6400"
    settings["shop"]["zapatillas"] = input(" Introduce cantidad de Zapatillas (6400): ") or "6400"

    print("\n" + show("config") + "Configuración de automatización (Catering)")
    settings["catering"] = {}
    settings["catering"]["refrescos"] = input(" Introduce cantidad de Refrescos (2000): ") or "2000"
    settings["catering"]["frankfurts"] = input(" Introduce cantidad de Frankfurts (1000): ") or "1000"
    settings["catering"]["pipas"] = input(" Introduce cantidad de Pipas (1000): ") or "1000"
    settings["catering"]["bocadillo"] = input(" Introduce cantidad de Bocadillos (1000): ") or "1000"
    settings["catering"]["cerveza"] = input(" Introduce cantidad de Cerveza (1250): ") or "1250"
    settings["catering"]["patatas"] = input(" Introduce cantidad de Bolsa de Patatas (1000): ") or "1000"
    settings["catering"]["berberechos"] = input(" Introduce cantidad de Berberechos (1000): ") or "1000"
    settings["catering"]["canapes"] = input(" Introduce cantidad de Canapés (1250): ") or "1250"
    settings["catering"]["arroz"] = input(" Introduce cantidad de Arroz Frito (1000): ") or "1000"
    settings["catering"]["vino"] = input(" Introduce cantidad de Vino (2000): ") or "2000"
    settings["catering"]["spaguetti"] = input(" Introduce cantidad de Spaguetti (1250): ") or "120"
    settings["catering"]["ensalada"] = input(" Introduce cantidad de Ensalada (1000): ") or "1000"
    settings["catering"]["cava"] = input(" Introduce cantidad de Cava (1000): ") or "1000"
    settings["catering"]["gnocchi"] = input(" Introduce cantidad de Gnocci (1250): ") or "1250"
    settings["catering"]["sushi"] = input(" Introduce cantidad de Sushi (1000): ") or "1000"
    settings["catering"]["bistec"] = input(" Introduce cantidad de Bistec (1250): ") or "1250"
    settings["catering"]["risotto"] = input(" Introduce cantidad de Risotto (1250): ") or "1250"
    settings["catering"]["rodaballo"] = input(" Introduce cantidad de Rodaballo (1750): ") or "1750"
    settings["catering"]["solomillo"] = input(" Introduce cantidad de Solomillo (1000): ") or "1000"
    settings["catering"]["caviar"] = input(" Introduce cantidad de Caviar (1000): ") or "1000"
    
    # Creamos el fichero de configuración
    print(show("config") + "Fichero de configuración creado con éxito")

    with open("./ibm_auto_manager/config/settings.json", "w") as settings_file:
      json.dump(settings, settings_file, indent=4, ensure_ascii=False)
    settings_file.close

    print(show("config") + "Configuración cargada con éxito")
  
  # Aplicamos la configuración
  if settings["proxy"] != "":
    os.environ["http_proxy"] = settings["proxy"] 
    os.environ["HTTP_PROXY"] = settings["proxy"]
    os.environ["https_proxy"] = settings["proxy"]
    os.environ["HTTPS_PROXY"] = settings["proxy"]

  print(show("config") + "Configuración aplicada con éxito")
  input(" Pulse para continuar...")

  return settings

def analyze_market():
  """ Obtenemos las ofertas del mercado """


# def save_profile(db, money):
#   db.profile.delete_many({})
#   pf = profile.Profile(1, money)
#   db.profile.insert_one(pf.to_db_collection())

#   if (db.profile.find_one({"id": 1}) is not None):
#     pfe = db.profile.find_one({"id": 1})
#     print(pfe)
#   else:
#     print("Error")


# =====================
#     -- Start --
# =====================
def run():
  
  cls()

  # Obtenemos la configuración
  settings = config()
  cls()

  # Login
  auth = {
    "alias": settings["user"]["alias"], 
    "pass": settings["user"]["password"], 
    "dest": None
  }

  # Database
  mongoClient = MongoClient(settings["mongodb"])
  db = mongoClient['ibm-auto-manager']

  session = login(auth)
    
# # Probamos el login obteniendo el dinero
  # r = session.get("http://es.ibasketmanager.com/inicio.php")
  # load_status = 0
  # while load_status != 200:
  #   load_status = r.status_code

  # soup = BeautifulSoup(r.content, "html.parser")

  # money = str(soup.find("a", {"id": "dineros"}).text
  #   ).replace("€", "").replace(".", "").replace(" ", "")

  # print(money + " €.")

  # # Probamos la conexion a BD guardando el dinero
  # save_profile(db, money)

  input("Pulse para salir...")
  cls()