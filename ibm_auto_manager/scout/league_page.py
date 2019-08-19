# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from bs4 import BeautifulSoup

from ibm_auto_manager.common.util import show
from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.general.dashboard_page import get_season
from ibm_auto_manager.trainer.team_page import enter_team


def enter_competition(auth, db, option):
  """ Recorremos las páginas de divisiones y ligas

    Keyword arguments:
        auth -- Cadena de autenticacion a la web.
        db -- Objeto de conexion a la BD.
        option -- opción de divisiones a analizar
    """
  season = get_season(auth)
  p_division = 1
  p_group = 1

  # División 1
  print(show("division") + " > Analizando división " + str(p_division))
  league_url = 'http://es.ibasketmanager.com/liga.php?temporada=' + \
    str(season) + '&division=' + str(p_division) + '&grupo=' + str(p_group)

  teams_ids = analyze_standings(league_url, auth)

  for team_id in teams_ids:
    enter_team(auth, db, team_id, False)

  # División 2
  p_division = 2
  print(show("division") + " > Analizando división " + str(p_division))
  for p_group in range(1, 5):
    print(show("division") + "   > Analizando división " + str(p_division) + \
      " Grupo: " + str(p_group))
    league_url = 'http://es.ibasketmanager.com/liga.php?temporada=' + \
      str(season) + '&division=' + str(p_division) + '&grupo=' + str(p_group)

    teams_ids = analyze_standings(league_url, auth)

    for team_id in teams_ids:
      enter_team(auth, db, team_id, False)

  if (option == "m" or option == "f"):
    # División 3
    p_division = 3
    print(show("division") + " > Analizando división " + str(p_division))
    for p_group in range(1, 17):
      print(show("division") + "   > Analizando división " + str(p_division) + \
        " Grupo: " + str(p_group))
      league_url = 'http://es.ibasketmanager.com/liga.php?temporada=' + \
        str(season) + '&division=' + str(p_division) + '&grupo=' + str(p_group)

      teams_ids = analyze_standings(league_url, auth)

      for team_id in teams_ids:
        enter_team(auth, db, team_id, False)

    # División 4
    p_division = 4
    print(show("division") + " > Analizando división " + str(p_division))
    for p_group in range(1, 65):
      print(show("division") + "   > Analizando división " + str(p_division) + \
        " Grupo: " + str(p_group))
      league_url = 'http://es.ibasketmanager.com/liga.php?temporada=' + \
        str(season) + '&division=' + str(p_division) + '&grupo=' + str(p_group)

      teams_ids = analyze_standings(league_url, auth)

      for team_id in teams_ids:
        enter_team(auth, db, team_id, False)

  if (option == "f"):
    # División 5
    p_division = 5
    print(show("division") + " > Analizando división " + str(p_division))
    for p_group in range(1, 51): # Es posible que no haya más equipos
      print(show("division") + "   > Analizando división " + str(p_division) + \
        " Grupo: " + str(p_group))
      league_url = 'http://es.ibasketmanager.com/liga.php?temporada=' + \
        str(season) + '&division=' + str(p_division) + '&grupo=' + str(p_group)

      teams_ids = analyze_standings(league_url, auth)

      for team_id in teams_ids:
        enter_team(auth, db, team_id, False)

def analyze_standings(league_url, auth):
    """ Analizamos los equipos de la liga pasada por parametro.
        Devolvemos los ids de los equipos inscritos a esa liga

    Keyword arguments:
        league_url -- URL de la liga
        auth -- Cadena de autenticacion a la web.
    """
    session = login(auth)

    # print(league_url)
    r = session.get(league_url)
    load_status = 0
    while load_status != 200:
        load_status = r.status_code

    soup = BeautifulSoup(r.content, 'html.parser')
    teams_str_a = soup.find_all('table')[0].find_all('a')
    teams_str_b = soup.find_all('table')[1].find_all('a')

    # Obtenemos los ids de los equipos que conforman esa liga
    teams_ids = []
    for team_str in teams_str_a + teams_str_b:
        # print(team_str['href'][team_str['href'].find('=')+1:])
        teams_ids.append(team_str['href'][team_str['href'].find('=')+1:])

    return teams_ids