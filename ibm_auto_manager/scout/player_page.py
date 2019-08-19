# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import re
import time

from bs4 import BeautifulSoup
from bson import ObjectId

from ibm_auto_manager.common import text
from ibm_auto_manager.common.util import show
from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.scout import player, transaction


def get_player_data(id_player, auth):
  """ Obtenemos los datos del jugador pasado por parametros

  Keyword arguments:
    id_player -- Id del jugador con el que cargamos su página
    auth -- Cadena de autenticacion a la web.
  """

  session = login(auth)
  # http://es.ibasketmanager.com/jugador.php?id_jugador=7192302
  # http://es.ibasketmanager.com/jugador.php?id_jugador=7856412
  # id_player = 7856412
  player_url = "http://es.ibasketmanager.com/" + \
    "jugador.php?id_jugador=" + str(id_player)
  # print(show("player") + " >{ " + player_url + " }")
  r = session.get(player_url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code

  v_player = analyze_player_page(id_player, r.content)

  return v_player


def analyze_player_page(id_player, html_content):
  """ Analizamos la página del jugador
    y devolvemos una tupla con sus datos y atributos

  Keyword arguments:
    id_player -- Id del jugador con el que cargamos su página
    html_content -- Texto completo de la página del mercado
      en formato String.

  """
  soup = BeautifulSoup(html_content, 'html.parser')
  
  # Datos
  name = soup.find("div", {"class": "barrajugador"})
  if name is not None:  # El jugador está en medio de un partido
    name = name.text.strip()
    name = str(re.search(r'[A-ZÁÉÍÓÚ][\w\W]+', name).group(0))

    if name.find('(Juvenil)') > 0:
      juvenil = True
      name = name.replace('(Juvenil)', '')
    else:
      juvenil = False
    name = name.strip()
    caja50 = soup.find_all("div", {"class": "caja50"})
    data0 = caja50[0].find_all("td")
    data1 = caja50[1].find_all("td")

    position = data0[1].text
    age = str(re.search(r'[\d]+', data0[3].text).group(0)).strip()
    # age = data0[3].text.replace('años','').replace('año','').replace(
    #  'aÃ±os','').replace('aÃ±o','').strip()
    heigth = str(re.search(r'[\d]+', data0[5].text.replace(
      '.', '').replace(',', '')).group(0)).strip()
    weight = str(re.search(r'[\d]+', data0[7].text.replace(
      '.', '').replace(',', '')).group(0)).strip()
    canon = str(re.search(r'[\d]+', data0[9].text.replace(
      '.', '').replace(',', '')).group(0)).strip()

    team_id = data1[1].find_all(
      'a')[0]['href'][data1[1].find_all('a')[0]['href'].find('=')+1:]
    salary = data1[3].text.replace('€', '').replace('.', '').strip()
    clause = data1[5].text.replace('€', '').replace('.', '').strip()
    years = str(re.search(r'[\d]+', data1[7].text).group(0)).strip()
    country = data1[9].text.strip()

    # Atributos
    bars = soup.find_all("div", {"class": "jugbarranum"})

    # print("---Atributos---")
    power = bars[0].text
    ambition = bars[1].text
    leadership = bars[2].text
    exp = bars[3].text
    speed = bars[4].text
    jump = bars[5].text
    endurance = bars[6].text
    level = bars[7].text[0:bars[7].text.find('(')].replace(',', '').strip()
    marking = bars[11].text
    rebound = bars[12].text
    block = bars[13].text
    recover = bars[14].text
    two = bars[15].text
    three = bars[16].text
    free = bars[17].text
    assist = bars[18].text
    dribbling = bars[19].text
    dunk = bars[20].text
    fight = bars[21].text

    # for t in bars:
    #   print(str(t.text))

    # print("--Medias--")
    caja5b = soup.find("div", {"class": "caja5b"})
    mrx = caja5b.find("div", {"class": "mrx"}).find_all(
      "td", {"class": "rojo"})
    mental = mrx[0].text.replace('.', '').strip()
    physic = mrx[1].text.replace('.', '').strip()
    defense = mrx[2].text.replace('.', '').strip()
    offense = mrx[3].text.replace('.', '').strip()
    total = mrx[4].text.replace('.', '').strip()

    # for t in mrx:
    #   print(t.text)

    return [player.Player(id_player, team_id, name, position, age, heigth,
                          weight, canon, salary, clause, years, juvenil,
                          country),
            player.PlayerAtributes(id_player, power, ambition, leadership,
                                  exp, speed, jump, endurance, level,
                                  marking, rebound, block, recover, two,
                                  three, free, assist, dribbling, dunk,
                                  fight, mental, physic, defense, offense,
                                  total)]
  else:
      return None


def insert_player(player, player_id, db):
  """ Introduce el jugador en la BD

  Keyword arguments:
      player -- tupla que representa los datos y los atributos del jugador
      player_id -- id del jugador
      db -- Objeto de conexion a la BD.
  """
  if player is not None:
    # Comprobamos si el jugador ya existe y en consecuencia
    # lo insertamos/actualizamos
    # print(str(player_id)  + ' - '+ str(player[0].id_player))
    # print(db.players.find_one({"id_player": player_id}))
    if (db.players.find_one({"_id": ObjectId(player_id.zfill(24))}) is not None):
      # print(show("player") + "    Actualizar P:  " + str(player[0]))
      db.players.update_one(
        {"_id": ObjectId(player_id.zfill(24))}, 
        {'$set': player[0].to_db_collection()}
      )
    else:
      # print(show("player") + "    Insertar P:  " + str(player[0]))
      db.players.insert_one(player[0].to_db_collection())

    if (db.players.find_one({"_id": ObjectId(player_id.zfill(24))}) is not None):
      # print(show("player") + "    Actualizar PA: " + str(player[1]))
      db.players.update_one(
        {"_id": ObjectId(player_id.zfill(24))}, 
        {'$set': player[1].to_db_collection()}
      )
    else:
      # print(show("player") + "    Insertar PA: " + str(player[1]))
      db.players.insert_one(player[1].to_db_collection())


def get_similar_data(id_player, auth, register_date = None):
  """ Obtenemos los datos de transacciones del jugador pasado por parametro

  Keyword arguments:
    id_player -- Id del jugador con el que cargamos su página
    auth -- Cadena de autenticacion a la web.
  """

  session = login(auth)

  # http://es.ibasketmanager.com/jugador.php?id_jugador=7192302
  # http://es.ibasketmanager.com/jugador.php?id_jugador=7856412
  # id_player = 7856412
  player_url = "http://es.ibasketmanager.com/jugador_compras_similares.php?" + \
     "id_jugador=" + str(id_player)
  # print(show("player") + " >{ " + player_url + " }")
  r = session.get(player_url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code

  transactions = analyze_similar_page(id_player, r.content)

  return transactions


def analyze_similar_page(id_player, html_content):
  """ Analizamos la página de transacciones similares del jugador
    y devolvemos una tupla con sus datos y atributos

  Keyword arguments:
    id_player -- Id del jugador con el que cargamos su página
    html_content -- Texto completo de la página del mercado
      en formato String.
  """
  soup = BeautifulSoup(html_content, 'html.parser')
  # Datos
  transactions = []
  final = soup.find("div", {'class': 'texto final'})
  # print(final)
  mensaje = soup.find("div", {"id": "menserror"})  # Playing a game
  # print(mensaje)
  if(final is None and mensaje is None):
    # If there is auctions with that filter
    players_str = soup.find_all(
      'table', {"id": "pagetabla"})[0].find_all('tr')
    players_str.pop(0)  # Deleted THs elements

    for player_str in players_str:
      player_soup = BeautifulSoup(str(player_str), 'html.parser')
      data_player = player_soup.find_all("td")
      name = str(data_player[0].find('a').text)
      id_date_buy = data_player[1].find("div").text
      date_buy = text.date_translation(
          data_player[1].text.replace(id_date_buy, '').strip())
      age = data_player[2].text
      avg = data_player[3].text
      pos = data_player[4].text
      salary = data_player[5].text.replace(
        '.', '').replace('€', '').strip()
      price = data_player[6].text.replace(
        '.', '').replace('€', '').strip()
      type_buy = data_player[7].text

      # print('\nId: '+ str(id_player) + ' Jugador: ' + name+ ' \
      # ' + pos +  ' de ' + age + ' años, con ' + avg + ' de media')
      # print('Vendido en ' + type_buy + ' por ' + price + '€, cobrando \
      # ' + salary + '€ en la fecha '+ date_buy +'\n')

      transactions.append(
        transaction.Transaction(
          id_player,
          id_date_buy,
          age,
          avg,
          pos,
          price,
          type_buy,
          salary,
          date_buy
        )
      )
  return transactions


def insert_similars(similars, db):
  """ Introduce las compras similares en la BD

  Keyword arguments:
    similars -- Array que representa las transacciones similares al jugador
    db -- Objeto de conexion a la BD.
  """
  for similar in similars:
    id_player = str(int(str(similar.player_id)))
    id_similar = str(int(str(similar.date_buy_id)))
    if(db.transactions.find(
      {"id_player": ObjectId(id_player.zfill(24))},
      {"date_buy_id": ObjectId(id_similar.zfill(24))}
    ).count() == 0):
      db.transactions.insert_one(similar.to_db_collection())
    else:
      pass
      # print("\t-Ya existe-")
      # db.transactions.replace_one(
      #  {"$and": [{"id_player": ObjectId(id_player.zfill(24))},
      #            {"date_buy_id": ObjectId(id_similar.zfill(24))}]},
      #  similar.to_db_collection())


def updateProgressions(player_id, progression_id, db):
  """ Actualiza/añade una progresion al jugador

  Keyword arguments:
    player_id -- Id del jugador con el que cargamos su página
    progression_id -- Id de la progresion
    db -- Objeto de conexion a la BD.
  """

  db.players.update_one(
    {"_id": ObjectId(player_id.zfill(24))}, 
    {'$push': {"progressions": ObjectId(progression_id)}}
  )


def updateAuctions(player_id, auction_id, db):
  """ Actualiza/añade una subasta al jugador

  Keyword arguments:
    player_id -- Id del jugador con el que cargamos su página
    auction_id -- Id de Subasta
    db -- Objeto de conexion a la BD.
  """
  db.players.update_one(
    {"_id": ObjectId(player_id.zfill(24))}, 
    {'$push': {"auctions": auction_id}}
  )