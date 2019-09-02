# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'


import re

from datetime import datetime
from bs4 import BeautifulSoup

from ibm_auto_manager.common.util import show
from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.general.dashboard_page import get_season, get_profile_data

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

          if(int(actual_day) >= int(analyze_day)):
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

                game = [game_id, game_type, game_url]
                # Obtenemos los datos del partido
                get_game(game_url, game_id, auth, db, session)



    elif option == "E":
      # Analizar el mes hasta el día indicado
      for td_day in td_days:
        if(td_day.find('div',{'class':'numdia'})):

          analyze_day = str(year) + str(month).zfill(2) +\
            td_day.find('div',{'class':'numdia'}).text.zfill(2)

          print(show("day") + " : " + analyze_day)

          if(int(actual_day) >= int(analyze_day)):

            if ( int(day) >= int(td_day.find('div',{'class':'numdia'}).text) ):
              print(td_day.find('div',{'class':'numdia'}).text)
    else:
      print(show("calendar") + "ERROR opcion inválida")
  else:
    # Analizar el mes entero
    pass


def get_game(url, game_id, auth, db, session=None):
  """ Lee los datos de la página del partido pasado por parámetro
  
  Keyword arguments:
      url -- Página del partido
      game_id -- ID del partido
      auth -- Cadena de autenticacion a la web.
      db -- Objeto de conexion a la BD.
  """
  if session is None:
    session = login(auth)

  r = session.get(url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code

  soup = BeautifulSoup(r.content, 'html.parser')
  
  # Datos del partido
  home_a = soup.find("div", {"class": "nombreequipo1"}).findAll("a")[0]['href']
  home_id = home_a[home_a.find("id=") + 3:]
  away_a = soup.find("div", {"class": "nombreequipo2"}).findAll("a")[0]['href']
  away_id = away_a[away_a.find("id=") + 3:]
  print("H: " + home_id + " A: " + away_id)
  table = soup.find("table",{"class": "datos_partido"})
  trs = table.findAll("tr")
  asistencia = trs[1].findAll("td")[0].text
  ingresos_home = trs[2].findAll("td")[0].text
  ingresos_away = trs[2].findAll("td")[2].text
  home_data = [
    trs[3].findAll("td")[0].text, # Puntos
    re.search("([\d])+", trs[4].findAll("td")[0].text.split('/')[0])[0], # T2I
    re.search("([\d])+", trs[4].findAll("td")[0].text.split('/')[1])[0], # T2C
    re.search("([\d])+", trs[5].findAll("td")[0].text.split('/')[0])[0], # T3I
    re.search("([\d])+", trs[5].findAll("td")[0].text.split('/')[1])[0], # T3C
    re.search("([\d])+", trs[6].findAll("td")[0].text.split('/')[0])[0], # TLI
    re.search("([\d])+", trs[6].findAll("td")[0].text.split('/')[1])[0], # TLC
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
  ]
  print(home_data)

  away_data = [
    trs[3].findAll("td")[2].text, # Puntos
    re.search("([\d])+", trs[4].findAll("td")[2].text.split('/')[0])[0], # T2I
    re.search("([\d])+", trs[4].findAll("td")[2].text.split('/')[1])[0], # T2C
    re.search("([\d])+", trs[5].findAll("td")[2].text.split('/')[0])[0], # T3I
    re.search("([\d])+", trs[5].findAll("td")[2].text.split('/')[1])[0], # T3C
    re.search("([\d])+", trs[6].findAll("td")[2].text.split('/')[0])[0], # TLI
    re.search("([\d])+", trs[6].findAll("td")[2].text.split('/')[1])[0], # TLC
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
  ]
  print(away_data)

  # print("A: " + asistencia + ", h: " + ingresos_home + ", aw: " + ingresos_away)






  