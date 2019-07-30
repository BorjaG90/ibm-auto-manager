# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import datetime
import time

from bs4 import BeautifulSoup

from ibm_auto_manager.common.util import show
from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.scout import roster_page, player_page


def enter_team(auth, db, own_team_id):
  """ Recorremos las páginas de plantilla y cantera del equipo
    y registra los atributos de los jugadores para
    la posterior comprobación de la progresión

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
    own_team_id -- Id del equipo
  """
  session = login(auth)

  # Analizo el progreso del equipo
  print(show("team_info") + "   > Analizando Equipo propio: " + str(own_team_id))

  # Seniors
  print(show("roster") + "   -> Plantilla: " + str(own_team_id))
  players_ids = roster_page.enter_senior_roster(own_team_id, auth)
  insert_players_data(auth, db, players_ids)

  # Juniors
  print(show("juniors") + "   -> Cantera:   " + str(own_team_id))
  juniors_ids = roster_page.enter_junior_roster(own_team_id, auth)
  insert_players_data(auth, db, juniors_ids)


def insert_players_data(auth, db, players_ids):
  """ Realizamos el bucle de inserción de los ids

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
    players_ids -- Array de Ids de los jugadores
  """
  for player_id in players_ids:
    player = player_page.get_player_data(player_id, auth)

    player_page.insert_player(player, player_id, db)

    prog_id = db.progressions.insert_one(
      player[1].to_db_collection_prog()).inserted_id
    #print(show("progression") + ": " + str(prog_id))

    player_page.updateProgressions(player_id, prog_id, db)
