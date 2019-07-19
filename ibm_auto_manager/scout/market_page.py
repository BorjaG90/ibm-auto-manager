# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from bs4 import BeautifulSoup

from ibm_auto_manager.common import text
from ibm_auto_manager.common.util import cls, show
from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.scout import player_page, auction

def enter_market(auth, db):
  """ Recorremos las páginas de mercado

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
  """

  db.auctions.delete_many({})
  print(show("market") + " > Mercado previo eliminado")

  params = {
    "juvenil": 0,
    "tiempos": 0,
    "posiciones": -1,
    "calidad": 14,
    "edad": -1,
    "cdirecta":  0
  }

  print(show("market") + " > Analizando Mercado Seniors")
  for p_time in range(2, 5):
    params["tiempos"] = p_time
    for p_avg in range(11, 17):
      params["calidad"] = p_avg
      analyze_market_page(auth, params, db)

  print(show("market") + " > Analizando Mercado Juniors")
  params["juvenil"] = 1
  params["edad"] = 0  # 14 años
  for p_time in range(2, 5):
    params["tiempos"] = p_time
    for p_avg in range(4, 6):
      params["calidad"] = p_avg
      analyze_market_page(auth, params, db)


def analyze_market_page(auth, params, db):
  """ Accede a la página del mercado obtenida de los parametros

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    params -- Parametros para construir la url del mercado.
    db -- Objeto de conexion a la BD.
  """

  session = login(auth)

  market_url = "http://es.ibasketmanager.com/mercado.php"
  market_url = market_url + "?juvenil=" + str(params["juvenil"])
  market_url = market_url + "&tiempos=" + str(params["tiempos"])
  market_url = market_url + "&posiciones=" + str(params["posiciones"])
  market_url = market_url + "&calidad=" + str(params["calidad"])
  market_url = market_url + "&edad" + str(params["edad"])
  market_url = market_url + "&cdirecta=" + str(params["cdirecta"])
  print(show("market") + ">{ " + market_url + " }")

  r = session.get(market_url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code
  auctions = get_auctions(r.content)

  for v_auction in auctions:
    # print("\t{}".format(auction))
    # Realizamos un analisis profundo de cada jugador
    player = player_page.get_player_data(v_auction.player_id, auth)
    # Esto es una tupla
    similars = player_page.get_similar_data(v_auction.player_id, auth)
    # print(similars)
    # Insertamos la subasta
    db.auctions.insert_one(v_auction.to_db_collection())

    player_page.insert_player(player, v_auction.player_id, db)
    player_page.insert_similars(similars, db)


def get_auctions(html_content):
    """ Analizamos los datos de la página del mercado y devolvemos las subastas

    Keyword arguments:
      html_content -- Texto completo de la página del mercado
        en formato String.
    """

    soup = BeautifulSoup(html_content, "html.parser")
    auctions = []
    final = soup.find("div", {"class": "texto final"})
    if(final is None):  # If there is auctions with that filter
      players_str = soup.find_all(
        "table", {"id": "pagetabla"})[0].find_all("tr")
      players_str.pop(0)
      # print(players_str)

      for player_str in players_str:
        player_soup = BeautifulSoup(str(player_str), "html.parser")
        data_player = player_soup.find_all("td")
        url = str(data_player[1].find("a")["href"]).split("id_jugador=")[1]
        pos = str(data_player[2].text)[3:5:1]
        avg = str(data_player[3].text)
        age = str(data_player[4].text)
        date_auction = text.date_market_translation(
          str(data_player[6].text[10:50:1]))
        offer = str(data_player[8].text).replace(
          '€', '').replace('.', '').strip()
        auctions.append(
          auction.Auction(url, pos, avg, age, date_auction, offer))

    else:
      print('\t' + final.contents[0])
    return auctions