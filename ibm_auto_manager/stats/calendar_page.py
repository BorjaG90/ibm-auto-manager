# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'


import re

from datetime import datetime
from bs4 import BeautifulSoup
from bson import ObjectId

from ibm_auto_manager.common.util import show
from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.general.dashboard_page import get_season, get_profile_data
from ibm_auto_manager.stats import team_stats, game, player_stats

def get_calendar(settings, auth, db, season=None, team_id=None):
  """ Lee los datos de las páginas de calendario según los parámetros pasados
  
    Keyword arguments:
      settings -- Objeto de configuración de la app
      auth -- Cadena de autenticacion a la web.
      db -- Objeto de conexion a la BD.
      season -- Temporada de la cual analizar el calendario
      team_id -- equipo del que obtener el calendario
  """
  if team_id is None:
    team_id = get_profile_data(auth, db)
  if season is None:
    season = get_season(auth)

  if(settings["seasons"][str(season)]):
    season_dates=settings["seasons"][str(season)]
  [init_day, init_month, init_year] = season_dates["init"].split("/")
  [end_day, end_month, end_year] = season_dates["end"].split("/")
  for year in range(int(init_year), int(end_year)+1):
    for month in range(int(init_month), int(end_month)+1):
      url = "http://es.ibasketmanager.com/proximos_partidos.php?mes=" +\
        str(year) + "-" + str(month).zfill(2) + "&id_equipo=" + team_id
      print(show("calendar") + " > " + url)
      if month == int(init_month):
        analyze_month(url, auth, db, year, month, "I", init_day)
      elif month == int(end_month):
        analyze_month(url, auth, db, year, month, "E", init_day)
      else:
        analyze_month(url, auth, db, year, month)

  
def analyze_month(url, auth, db, year, month, option=None, day=None):
  """ Analiza el mes pasado por parámetro 
  
    Keyword arguments:
      url -- Página de ese mes
      auth -- Cadena de autenticacion a la web.
      db -- Objeto de conexion a la BD.
      option -- Opción de día desde/hasta el que analizar
      day -- Día inicio/límite
  """

  session = login(auth)

  r = session.get(url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code

  soup = BeautifulSoup(r.content, 'html.parser')

  weeks = soup.find('table', {'id': 'calendario'}).findAll('tr')
  weeks.pop(0)
  weeks.pop(0)
  td_days = []
  actual_day = str(datetime.now().year)+str(datetime.now().month).zfill(2)+\
    str(datetime.now().day).zfill(2)
  print(show("calendar") + " > Mes en análisis: " + \
    str(year)+str(month).zfill(2))
  for week in weeks:
    for td in week.findAll('td'):
      td_days.append(td)

  if option is not None and day is not None:

    if option == "I":
      # Analizar el mes desde el día indicado
      for td_day in td_days:
        if(td_day.find('div',{'class':'numdia'})):

          analyze_day = str(year) + str(month).zfill(2) +\
            td_day.find('div',{'class':'numdia'}).text.zfill(2)
          # print(show("day") + " : " + analyze_day)

          if(int(actual_day) > int(analyze_day)):
            # print(show("day") + " : " + analyze_day)

            if ( int(day) <= int(td_day.find('div',{'class':'numdia'}).text) ):
              print(show("calendar day") + " : " + analyze_day)
              #print(td_day.find('div',{'class':'numdia'}).text)
              if(td_day.findAll('a')):
                game_id = td_day.findAll('a')[0]['href']\
                  [td_day.findAll('a')[0]['href'].find("id=") + 3:]
                game_url = "http://es.ibasketmanager.com/" + \
                  td_day.findAll('a')[0]['href']
                
                # print(game_id)
              
                span_text = td_day.find("div",{"class":"tipopart"}).find('span').text
                game_type = td_day.find("div",{"class":"tipopart"}).text\
                  .replace(span_text,'').strip()
                # print(game_type)
                print(show("calendar") + "  } Game: " + game_type + " : " + game_url )

                # Obtenemos los datos del partido
                str_day = td_day.find('div',{'class':'numdia'}).text.zfill(2) +\
                   "/" + str(month).zfill(2) + "/" + str(year)
            
                get_game(game_url, game_id, game_type, str_day, auth, db, session)

    elif option == "E":
      # Analizar el mes hasta el día indicado
      for td_day in td_days:
        if(td_day.find('div',{'class':'numdia'})):

          analyze_day = str(year) + str(month).zfill(2) +\
            td_day.find('div',{'class':'numdia'}).text.zfill(2)

          # print(show("day") + " : " + analyze_day)

          if(int(actual_day) > int(analyze_day)):

            if ( int(day) >= int(td_day.find('div',{'class':'numdia'}).text) ):
              print(show("calendar day") + " : " + analyze_day)
              #print(td_day.find('div',{'class':'numdia'}).text)
              if(td_day.findAll('a')):
                game_id = td_day.findAll('a')[0]['href']\
                  [td_day.findAll('a')[0]['href'].find("id=") + 3:]
                game_url = "http://es.ibasketmanager.com/" + \
                  td_day.findAll('a')[0]['href']
                
                # print(game_id)
              
                span_text = td_day.find("div",{"class":"tipopart"}).find('span').text
                game_type = td_day.find("div",{"class":"tipopart"}).text\
                  .replace(span_text,'').strip()
                # print(game_type)
                print(show("calendar") + "  } Game: " + game_type + " : " + game_url )

                # Obtenemos los datos del partido
                str_day = td_day.find('div',{'class':'numdia'}).text.zfill(2) +\
                   "/" + str(month).zfill(2) + "/" + str(year)
            
                get_game(game_url, game_id, game_type, str_day, auth, db, session)
    else:
      print(show("calendar") + "ERROR opcion inválida")

  else:
    # Analizar el mes entero
    for td_day in td_days:
      if(td_day.find('div',{'class':'numdia'})):

        analyze_day = str(year) + str(month).zfill(2) +\
          td_day.find('div',{'class':'numdia'}).text.zfill(2)

        # print(show("day") + " : " + analyze_day)

        if(int(actual_day) > int(analyze_day)):
          print(show("calendar day") + " : " + analyze_day)
          #print(td_day.find('div',{'class':'numdia'}).text)
          if(td_day.findAll('a')):
            game_id = td_day.findAll('a')[0]['href']\
              [td_day.findAll('a')[0]['href'].find("id=") + 3:]
            game_url = "http://es.ibasketmanager.com/" + \
              td_day.findAll('a')[0]['href']
            
            # print(game_id)
          
            span_text = td_day.find("div",{"class":"tipopart"}).find('span').text
            game_type = td_day.find("div",{"class":"tipopart"}).text\
              .replace(span_text,'').strip()
            # print(game_type)
            print(show("calendar") + "  } Game: " + game_type + " : " + game_url )

            # Obtenemos los datos del partido
            str_day = td_day.find('div',{'class':'numdia'}).text.zfill(2) +\
                "/" + str(month).zfill(2) + "/" + str(year)
        
            get_game(game_url, game_id, game_type, str_day, auth, db, session)


def get_game(url, game_id, game_type, game_day, auth, db, session=None):
  """ Lee los datos de la página del partido pasado por parámetro
  
  Keyword arguments:
      url -- Página del partido
      game_id -- ID del partido
      auth -- Cadena de autenticacion a la web.
      db -- Objeto de conexion a la BD.
  """
  if session is None:
    session = login(auth)

  r = session.get(url + '&accion=datos')
  load_status = 0
  while load_status != 200:
    load_status = r.status_code

  soup = BeautifulSoup(r.content, 'html.parser')
  
  # Datos del partido
  home_a = soup.find("div", {"class": "nombreequipo1"}).findAll("a")[0]['href']
  home_id = home_a[home_a.find("id=") + 3:]
  away_a = soup.find("div", {"class": "nombreequipo2"}).findAll("a")[0]['href']
  away_id = away_a[away_a.find("id=") + 3:]
  

  table = soup.find("table",{"class": "datos_partido"})
  trs = table.findAll("tr")
  if game_type != "All Star":
    asistencia = trs[1].findAll("td")[0].text.replace('.','').strip()
    ingresos_home = trs[2].findAll("td")[0].text.replace('€', '').replace('.','').strip()
    ingresos_away = trs[2].findAll("td")[2].text.replace('€', '').replace('.','').strip()
    if ingresos_away == '':
      ingresos_away = '0'

    game_obj = game.Game(game_day, game_id, game_type, home_id, away_id, 
      asistencia, ingresos_home, ingresos_away)

    # Inserción del partido en la BD
    insert_game(game_obj, ObjectId(game_id.zfill(24)), db)

    # Es posible que haya partidos de copa sin rival, 
    # entonces solo registramos el partido sin estadisticas
    valido = True
    
    if trs[4].findAll("td")[0].text == '0':
      print(show("calendar_game") + "  !> ERROR: partido no válido")
      valido = False
    if int(home_id) != 0 and int(away_id) != 0 and valido:
      # Stats de Equipos
      # Equipo Anfitrión
      home_stats = team_stats.TeamStats(
        game_id + home_id, game_id, home_id,
        trs[3].findAll("td")[0].text, # Puntos
        re.search("([\d])+", trs[4].findAll("td")[0].text.split('/')[0])[0], # T2C
        re.search("([\d])+", trs[4].findAll("td")[0].text.split('/')[1])[0], # T2I
        re.search("([\d])+", trs[5].findAll("td")[0].text.split('/')[0])[0], # T3C
        re.search("([\d])+", trs[5].findAll("td")[0].text.split('/')[1])[0], # T3I
        re.search("([\d])+", trs[6].findAll("td")[0].text.split('/')[0])[0], # TLC
        re.search("([\d])+", trs[6].findAll("td")[0].text.split('/')[1])[0], # TLI
        trs[7].findAll("td")[0].text, # RebD
        trs[8].findAll("td")[0].text, # RebO
        trs[10].findAll("td")[0].text, # Asi
        trs[11].findAll("td")[0].text, # Rob
        trs[12].findAll("td")[0].text, # Per
        trs[13].findAll("td")[0].text, # TapF
        trs[14].findAll("td")[0].text, # TapC
        trs[15].findAll("td")[0].text, # FalR
        trs[16].findAll("td")[0].text, # FalC
        trs[17].findAll("td")[0].text, # Val
      )
      # print(home_stats)
      # Insertamos las estadisticas en la bd
      insert_team_stats(
        ObjectId((game_id + home_id).zfill(24)),
        ObjectId(home_id.zfill(24)),
        ObjectId(game_id.zfill(24)),
        home_stats, db
      )

      # Equipo Visitante
      away_stats = team_stats.TeamStats(
        game_id + away_id, game_id, away_id,
        trs[3].findAll("td")[2].text, # Puntos
        re.search("([\d])+", trs[4].findAll("td")[2].text.split('/')[0])[0], # T2C
        re.search("([\d])+", trs[4].findAll("td")[2].text.split('/')[1])[0], # T2I
        re.search("([\d])+", trs[5].findAll("td")[2].text.split('/')[0])[0], # T3C
        re.search("([\d])+", trs[5].findAll("td")[2].text.split('/')[1])[0], # T3I
        re.search("([\d])+", trs[6].findAll("td")[2].text.split('/')[0])[0], # TLC
        re.search("([\d])+", trs[6].findAll("td")[2].text.split('/')[1])[0], # TLI
        trs[7].findAll("td")[2].text, # RebD
        trs[8].findAll("td")[2].text, # RebO
        trs[10].findAll("td")[2].text, # Asi
        trs[11].findAll("td")[2].text, # Rob
        trs[12].findAll("td")[2].text, # Per
        trs[13].findAll("td")[2].text, # TapF
        trs[14].findAll("td")[2].text, # TapC
        trs[15].findAll("td")[2].text, # FalR
        trs[16].findAll("td")[2].text, # FalC
        trs[17].findAll("td")[2].text, # Val
      )
      # print(away_stats)
      # Insertamos las estadisticas en la bd
      insert_team_stats(
        ObjectId((game_id + away_id).zfill(24)),
        ObjectId(away_id.zfill(24)),
        ObjectId(game_id.zfill(24)),
        away_stats, db
      )

      # Stats de Jugadores
      get_player_stats(url, game_id, home_id, away_id, auth, db, session)
  

def get_player_stats(url, game_id, home_id, away_id, auth, db, session=None):
  """ Lee las estadísticas de la página del partido pasado por parámetro
  
  Keyword arguments:
      url -- Página del partido
      game_id -- ID del partido
      auth -- Cadena de autenticacion a la web.
      db -- Objeto de conexion a la BD.
  """
  if session is None:
    session = login(auth)

  r = session.get(url + "&accion=alineaciones")
  load_status = 0
  while load_status != 200:
    load_status = r.status_code

  soup = BeautifulSoup(r.content, 'html.parser')
  tables = soup.findAll("table", {"id": "pagetabla"})

  # Equipo anfitrión
  trs_home = tables[0].find('tbody').findAll('tr', {'class':['tipo1','tipo2']})
  trs_home.pop()
  for tr in trs_home:
    # print(tr)
    tds = tr.findAll('td')
    player_a = tds[3].findAll('a')[0]['href']
    player_id = player_a[player_a.find("id_jugador=") + 11:]
    
    player_data_stats = player_stats.PlayerStats(
      game_id + player_id, game_id, home_id, player_id,
      tds[4].text,
      tds[5].text.split('/')[0], # T2C
      tds[5].text.split('/')[1], # T2I
      tds[7].text.split('/')[0], # T3C
      tds[7].text.split('/')[1], # T3I
      tds[9].text.split('/')[0], # T3C
      tds[9].text.split('/')[1], # T3I
      tds[11].text, # RebD
      tds[12].text, # RebO
      tds[14].text, # Ste
      tds[15].text, # TurnOvers
      tds[16].text, # Ass
      tds[17].text, # BlockF
      tds[18].text, # BlockC
      tds[19].text, # FoulR
      tds[20].text, # FoulC
      tds[21].text.split(':')[0], # Min
      tds[21].text.split(':')[1], # Seg
      tds[22].text, # Val
    )
    # print(player_data_stats)
    # Insertamos las estadisticas en la bd
    insert_player_stats(
      ObjectId((game_id + player_id).zfill(24)),
      ObjectId(player_id.zfill(24)),
      ObjectId(game_id.zfill(24)),
      player_data_stats, db
    )
    
  # Equipo visitante
  trs_away = tables[1].findAll('tr', {'class':['tipo1','tipo2']})
  trs_away.pop()
  for tr in trs_away:
    # print(tr)
    tds = tr.findAll('td')
    player_a = tds[3].findAll('a')[0]['href']
    player_id = player_a[player_a.find("id_jugador=") + 11:]
    
    player_data_stats = player_stats.PlayerStats(
      game_id + player_id, game_id, away_id, player_id,
      tds[4].text,
      tds[5].text.split('/')[0], # T2C
      tds[5].text.split('/')[1], # T2I
      tds[7].text.split('/')[0], # T3C
      tds[7].text.split('/')[1], # T3I
      tds[9].text.split('/')[0], # T3C
      tds[9].text.split('/')[1], # T3I
      tds[11].text, # RebD
      tds[12].text, # RebO
      tds[14].text, # Ste
      tds[15].text, # TurnOvers
      tds[16].text, # Ass
      tds[17].text, # BlockF
      tds[18].text, # BlockC
      tds[19].text, # FoulR
      tds[20].text, # FoulC
      tds[21].text.split(':')[0], # Min
      tds[21].text.split(':')[1], # Seg
      tds[22].text, # Val
    )
    # print(player_data_stats)
    # Insertamos las estadisticas en la bd
    insert_player_stats(
      ObjectId((game_id + player_id).zfill(24)),
      ObjectId(player_id.zfill(24)),
      ObjectId(game_id.zfill(24)),
      player_data_stats, db
    )

def insert_game(game, game_id, db):
  if (db.games.find_one({"_id": game_id}) is not None):
    db.games.update_one(
      {"_id": game_id}, 
      {'$set': game.to_db_collection()}
    )
  else:
    db.games.insert_one(game.to_db_collection())

def insert_team_stats(stats_id, team_id, game_id, team_data_stats, db):
  """ Realiza la inserción y las actualizaciones de las estadisticas 
    de un equipo en un partido en la base de datos"""
  if (db.team_stats.find_one({"_id": stats_id}) is not None):
    db.team_stats.update_one(
      {"_id": stats_id}, 
      {'$set': team_data_stats.to_db_collection()}
    )
  else:
    db.team_stats.insert_one(team_data_stats.to_db_collection())

  if(db.teams.find_one({"stats": stats_id}) is None):
    # print("Inserta stat")
    db.teams.update_one(
      {"_id": team_id}, 
      {'$push': {"stats": stats_id}}
    )
  if(db.games.find_one({"team_stats": stats_id}) is None):
    # print("Inserta stat")
    db.games.update_one(
      {"_id": game_id}, 
      {'$push': {"team_stats": stats_id}}
    )


def insert_player_stats(stats_id, player_id, game_id, player_data_stats, db):
  """ Realiza la inserción y las actualizaciones de las estadisticas 
    de un jugador en un partido en la base de datos"""
  if (db.player_stats.find_one({"_id": stats_id}) is not None):
    db.player_stats.update_one(
      {"_id": stats_id}, 
      {'$set': player_data_stats.to_db_collection()}
    )
  else:
    db.player_stats.insert_one(player_data_stats.to_db_collection())

  if(db.players.find_one({"stats": stats_id}) is None):
    # print("Inserta stat")
    db.players.update_one(
      {"_id": player_id}, 
      {'$push': {"stats": stats_id}}
    )
  if(db.games.find_one({"player_stats": stats_id}) is None):
    # print("Inserta stat")
    db.games.update_one(
      {"_id": game_id}, 
      {'$push': {"player_stats": stats_id}}
    )
  