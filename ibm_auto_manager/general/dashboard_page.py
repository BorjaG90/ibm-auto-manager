# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from bs4 import BeautifulSoup
from bson import ObjectId

from ibm_auto_manager.common.util import show
from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.general import profile


def get_profile_data(auth, db):
  """ Obtenemos los datos del perfil del usuario actual
    Devolvemos el id del equipo

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
  """

  id_team, user, team, money, color_prim, color_sec = analyze_init(auth, db)
  id_user, seats, fans, ranking, streak = analyze_team_page(auth, db, id_team)

  
  v_profile = profile.Profile(
    id_user, user, id_team, team, money, color_prim, 
    color_sec, seats, fans, ranking, streak
  )

  if (db.profiles.find_one({"team_id": ObjectId(id_team.zfill(24))}) is not None):
    db.profiles.replace_one(
      {"team_id": ObjectId(id_team.zfill(24))}, v_profile.to_db_collection())
  else:
    db.profiles.insert_one(v_profile.to_db_collection())

  print(show("profile") + " > Perfil actualizado")

  return id_team


def analyze_init(auth, db):
  """ Analizamos la pagina de inicio

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
  """
  session = login(auth)

  url = "http://es.ibasketmanager.com/inicio.php"
  r = session.get(url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code
  
  print(show("profile") + " > Analizando perfil inicial")

  soup = BeautifulSoup(r.content, "html.parser")
  a = soup.find_all("a", {"class": "color_skin"})
  camisetas = soup.find_all("div", {"class": "camiseta"}, style=True)
  color_prim = camisetas[0]["style"].split(":")[1].strip()
  color_sec = camisetas[1]["style"].split(":")[1].strip()
  # print(a)
  username = a[0].text
  id_team = a[2]["href"].split("=")[1].strip()
  team_name = a[2].text.strip()
  money = a[3].text.replace('€','').replace('.','').strip()

  return [id_team, username, team_name, money, color_prim, color_sec]

def analyze_team_page(auth, db, id_team):
  """ Analizamos la pagina del equipo

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
  """
  session = login(auth)

  url = "http://es.ibasketmanager.com/equipo.php?id=" + id_team
  r = session.get(url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code
  
  print(show("profile") + " > Analizando perfil del equipo")

  soup = BeautifulSoup(r.content, "html.parser")
  
  trs2 = soup.find_all("tr", {"class": "tipo2"})

  id_user = trs2[0].find("a")["href"].split("=")[1]
  streak = trs2[2].find_all("td")[1].text
  club_seats = trs2[3].find_all("td")[1].text.replace(".","").strip()
  ranking = trs2[4].find_all("td")[1].text.replace("Ranking","").strip()
  
  trs1 = soup.find_all("tr", {"class": "tipo1"})
  fans = trs1[3].find_all("td")[1].text.replace(".","").strip()

  return [id_user, club_seats, fans, ranking, streak]

def get_season(auth):
  """ Obtenemos la temporada actual en juego

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
  """
  session = login(auth)

  # Obtenemos id de la liga actual
  url = "http://es.ibasketmanager.com/inicio.php"

  r = session.get(url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code

  soup = BeautifulSoup(r.content, "html.parser")
  
  menu = soup.find("div", {"id": "menu1"})
  id_league = menu.find_all("div")[2].find("a")["href"].split("=")[1].strip()
  
  # Obtenemos la temporada
  url = "http://es.ibasketmanager.com/liga.php?id_liga=" + str(id_league)

  r = session.get(url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code

  soup = BeautifulSoup(r.content, "html.parser")
  
  menu = soup.find_all("div", {"class": "caja2 final"})[0]
  season = menu.find_all("div", {"class": "selector"})[2].find("span").text

  return season