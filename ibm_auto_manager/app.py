######################
#  IBM-Auto-Manager  #
######################

# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import os
import json
import getpass

from bs4 import BeautifulSoup
from pymongo import MongoClient

from ibm_auto_manager.common.util import cls, show
from ibm_auto_manager.general import dashboard_page
from ibm_auto_manager.scout import market_page, league_page
from ibm_auto_manager.trainer import team_page
from ibm_auto_manager.dt import automation
from ibm_auto_manager.stats import calendar_page

# ----- Functions -----
def config():
  """ Obtenemos la configuración de la app desde el fichero solicitado. 
    En caso de que no exista, solictamos los datos necesarios y lo creamos."""
  
  settings = {}
  if os.path.isfile("./ibm_auto_manager/config/settings.json"):
    print(show("config") + "Encontrado fichero configuración")

    with open("./ibm_auto_manager/config/settings.json", 'r') as settings_file:
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

  return settings

def connect():
  """ Realizamos las configuraciones y conexiones necesarias para el 
  funcionamiento de la aplicación y las devolvemos en un diccionario"""

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

  connection = {"settings": settings, "auth": auth, "db": db }

  return connection


# =====================
#     -- Start --
# =====================
def run(arg=""):
  
  connection = connect()

  if arg == "--market" or arg == "-m" or arg == "market":
    """ Ejecución exclusiva del análisis de mercado """
    print("********IBM Auto Manager**********")
    print("\nAnalizando mercado")
    market_page.enter_market(connection["auth"], connection["db"])

  elif arg == "--profile" or arg == "-p" or arg == "profile":
    """ Ejecución exclusiva del análisis del perfil """
    print("********IBM Auto Manager**********")
    print("\nAnalizando perfil")
    id_team = dashboard_page.get_profile_data(
      connection["auth"], connection["db"])
    team_page.enter_team(connection["auth"], connection["db"], id_team)

  elif arg == "--teams" or arg == "-t" or arg == "teams":
    """ Ejecución de analisis de equipos de la parte alta de la competición """
    
    print("********IBM Auto Manager**********")
    print("\nAnalizando competición")
    league_page.enter_competition(connection["auth"], connection["db"], "m")

  elif arg == "--teams-elite" or arg == "-te" or arg == "teams-elite":
    """ Ejecución de analisis de equipos de elite de la competición """
    
    print("********IBM Auto Manager**********")
    print("\nAnalizando competición")
    league_page.enter_competition(connection["auth"], connection["db"], "e")
  
  elif arg == "--teams-full" or arg == "-tf" or arg == "teams-full":
    """ Ejecución de analisis de todos los equipos de la competición"""
    
    print("********IBM Auto Manager**********")
    print("\nAnalizando competición")
    league_page.enter_competition(connection["auth"], connection["db"], "f")

  elif arg == "--teams-mid" or arg == "-tm" or arg == "teams-mid":
    """ Ejecución de analisis delos equipos de 3 y 4 de la competición"""
    
    print("********IBM Auto Manager**********")
    print("\nAnalizando competición")
    league_page.enter_competition(connection["auth"], connection["db"], "2")

  elif arg == "--teams-low" or arg == "-tl" or arg == "teams-low":
    """ Ejecución de analisis delos equipos de 3 y 4 de la competición"""
    
    print("********IBM Auto Manager**********")
    print("\nAnalizando competición")
    league_page.enter_competition(connection["auth"], connection["db"], "3")

  elif arg == "--auto-bid" or arg == "-b" or arg == "auto-bid":
    """ Ejecución de auto_apuesta en la subasta de un jugador"""
    
    print("********IBM Auto Manager**********")
    print("\nAnalizando subasta")
    automation.auto_bid(connection["auth"])

  elif arg == "--auto-offer" or arg == "-o" or arg == "auto-offer":
    """ Ejecución de auto_oferta en la renovación de un jugador"""
    
    print("********IBM Auto Manager**********")
    print("\nAnalizando contrato")
    automation.auto_offer(connection["auth"])

  elif arg == "--calendar" or arg == "-c" or arg == "calendar":
    """ Ejecución de ánalisis del calendario de la última temporada"""
    
    print("********IBM Auto Manager**********")
    print("\nObteniendo calendario de la útlima temporada")
    calendar_page.get_calendar(
      connection["settings"],connection["auth"],connection["db"])

  elif arg == "":
    """ Ejecución normal """
    # Menu
    while True:
      cls()

      print("********IBM Auto Manager**********")
      print("\n[m] Analizar mercado")
      print("\n[p] Analizar perfil") # Provisional
      print("\n[t] Analizar competicion")
      print("\n[b] Realizar apuesta en subasta")
      print("\n[o] Realizar oferta de renovación")
      print("\n[c] Analizar calendario")
      print("\n[0] Salir del programa\n")

      opcion = input("Introduce una opción: > ")

      if opcion == "b":
        automation.auto_bid(connection["auth"])

      if opcion == "c":
        calendar_page.get_calendar(
          connection["settings"],connection["auth"],connection["db"])

      if opcion == "o":
        automation.auto_offer(connection["auth"])

      if opcion == "m":
        market_page.enter_market(connection["auth"], connection["db"])
      
      if opcion == "p":
        id_team = int(dashboard_page.get_profile_data(
          connection["auth"], connection["db"]))
        team_page.enter_team(connection["auth"], connection["db"], id_team)

      if opcion == "m":
        while True:
          cls()

          print("********IBM Auto Manager**********")
          print("****Análisis de Competición******")
          print("\n[e] Elite / 2 divisiones")
          print("\n[m] Parte alta / 4 divisiones")
          print("\n[f] Toda la competicion")
          print("\n[0] Salir de la opcion\n")

          opcion = input("Introduce las divisiones a analizar: > ")
          if opcion == "m":
            league_page.enter_competition(
              connection["auth"], connection["db"], "m")
          elif opcion == "e":
            league_page.enter_competition(
              connection["auth"], connection["db"], "e")
          elif opcion == "f":
            league_page.enter_competition(
              connection["auth"], connection["db"], "f")
          elif opcion == "0":
            cls()
            break
          else:
            print("Opción incorrecta")

      elif opcion == "0":
        print("Cerrando programa!")
        cls()
        break

      else:
        print("Opción incorrecta")

      input("\nPulse para continuar...")

  else:
    print("No se reconoce este comando")

  input("Pulse para salir...")
  cls()