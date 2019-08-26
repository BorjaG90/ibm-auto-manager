# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import datetime
import time
import re

from bs4 import BeautifulSoup
from bson import ObjectId

from ibm_auto_manager.common.util import show
from ibm_auto_manager.common import text
from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.scout import roster_page, player_page
from ibm_auto_manager.trainer import team


def enter_team(auth, db, team_id, get_prog = True):
  """ Recorremos las páginas de plantilla y cantera del equipo
    y registra los atributos de los jugadores para
    la posterior comprobación de la progresión

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
    team_id -- Id del equipo
    get_prog -- 
  """
  session = login(auth)

  # http://es.ibasketmanager.com/equipo.php?id=1643
  team_url = "http://es.ibasketmanager.com/" + \
    "equipo.php?id=" + str(team_id)

  r = session.get(team_url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code

  # Analizo el progreso del equipo
  print(show("team_info") + "   > Analizando Equipo: " + str(team_id))
  team_info = analyze_team(team_id, r.content)
  print(show("team") + "    -> Equipo: " + str(team_id))
  insert_team_data(team_info, db)

  # Seniors
  print(show("roster") + "    -> Plantilla: " + str(team_id))
  players_ids = roster_page.enter_senior_roster(team_id, auth, session)
  insert_players_data(auth, db, players_ids, get_prog, session)
  update_players(players_ids, team_id, db, "S")

  # Juniors
  print(show("juniors") + "    -> Cantera:   " + str(team_id))
  juniors_ids = roster_page.enter_junior_roster(team_id, auth, session)
  insert_players_data(auth, db, juniors_ids, get_prog, session)
  update_players(juniors_ids, team_id, db, "J")

def analyze_team(team_id, html_content):
  """ Obtenemos los datos relativos al equipo"""

  soup = BeautifulSoup(html_content, 'html.parser')

  caja50 = soup.find_all("div", {"class": "caja50"})
  th = caja50[0].find("table").find("th")
  data = caja50[0].find("table").find_all("td")

  name = th.text
  # print("Name: " + name)

  id_user = data[1].find_all(
    'a')[0]['href'][data[1].find_all('a')[0]['href'].find('=')+1:]
  # print("IdUser: " + id_user)

  user = data[1].text
  # print("User: " + user)

  arena = data[3].find_all('a')[0].text
  # print("Arena: " + arena)

  division = re.search("([\d])+", data[5].text.split('/')[0])[0]
  group = re.search("([\d])+", data[5].text.split('/')[1])[0]
  # print("League: " + division + "/" + group )

  clasification = data[7].text
  # print("Clasification: " + clasification)

  streak = data[9].text
  # print("Racha: " + streak)

  return team.Team(team_id, name, id_user, user, arena, division, group, \
    clasification, streak)


def insert_players_data(auth, db, players_ids, get_prog = True, session = None):
  """ Realizamos el bucle de inserción de los ids

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
    players_ids -- Array de Ids de los jugadores
  """
  for player_id in players_ids:
    player = player_page.get_player_data(player_id, auth, session)

    player_page.insert_player(player, player_id, db)

    # Si recibimos la orden de guardar la progresión de los jugadores
    if(get_prog):
      future_id = ObjectId((str(int(str(player_id))) + text.get_date_str(datetime.datetime.now(), False)).zfill(24))
      # print(future_id)
      if(db.progressions.find_one({"_id": future_id}) is None):
        prog_id = db.progressions.insert_one(
          player[1].to_db_collection_prog()).inserted_id
        # print(show("progression") + ": " + str(prog_id))

      player_page.updateProgressions(player_id, future_id, db)


def insert_team_data(team, db):
  """ Introduce el equipo en la BD

  Keyword arguments:
      team -- objeto que representa los datos del equipo
      db -- Objeto de conexion a la BD.
  """
  if team is not None:
    # Comprobamos si el equipo ya existe y en consecuencia
    # lo insertamos/actualizamos
    # print(str(player_id)  + ' - '+ str(player[0].id_player))
    # print(db.players.find_one({"id_player": player_id}))
    if (db.teams.find_one({"_id": team._id}) is not None):
      # print(show("player") + "    Actualizar P:  " + str(player[0]))
      db.teams.update_one(
        {"_id": team._id}, 
        {'$set': team.to_db_collection()}
      )
    else:
      # print(show("player") + "    Insertar P:  " + str(player[0]))
      db.teams.insert_one(team.to_db_collection())


def update_players(ids, team_id, db, option):
  """ Actualiza/añade los jugadores del equipo

  Keyword arguments:
    ids -- Ids de los jugadores
    team_id -- Id del equipo
    db -- Objeto de conexion a la BD.
    option -- Plantilla senior o junior
  """
  if option == "S":
    db.teams.update_one(
      {"_id": ObjectId(team_id.zfill(24))}, 
      {"$set": {"seniors": []}}
    )

    for id in ids:
      # print(team_id)
      db.teams.update_one(
        {"_id": ObjectId(team_id.zfill(24))}, 
        {"$push": {"seniors": ObjectId(id.zfill(24))}}
      )
  else:
    db.teams.update_one(
      {"_id": ObjectId(team_id.zfill(24))}, 
      {'$set': {"juniors": []}}
    )

    for id in ids:
      # print(id)
      db.teams.update_one(
        {"_id": ObjectId(team_id.zfill(24))}, 
        {'$push': {"juniors": ObjectId(id.zfill(24))}}
      )