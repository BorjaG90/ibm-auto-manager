# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import datetime
import time

from bs4 import BeautifulSoup
from bson import ObjectId

from ibm_auto_manager.common.util import show
from ibm_auto_manager.common import text
from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.scout import roster_page, player_page


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

  # Analizo el progreso del equipo
  print(show("team_info") + "   > Analizando Equipo: " + str(team_id))

  # Seniors
  print(show("roster") + "    -> Plantilla: " + str(team_id))
  players_ids = roster_page.enter_senior_roster(team_id, auth, session)
  insert_players_data(auth, db, players_ids, get_prog, session)

  # Juniors
  print(show("juniors") + "    -> Cantera:   " + str(team_id))
  juniors_ids = roster_page.enter_junior_roster(team_id, auth, session)
  insert_players_data(auth, db, juniors_ids, get_prog, session)


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
