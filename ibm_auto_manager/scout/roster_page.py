# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from bs4 import BeautifulSoup

from ibm_auto_manager.connection.login_page import login


def enter_senior_roster(id_team, auth, session = None):
  """ Recorremos las páginas de plantillas
    Devolvemos un array con los ids de los jugadores
      que conforman la plantilla

  Keyword arguments:
    id_team -- Id del equipo al que se va a acceder a su plantilla
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
  """

  if session is None:
    session = login(auth)

  senior_roster_url = "http://es.ibasketmanager.com/plantilla.php?id_equipo="\
    + str(id_team)

  r = session.get(senior_roster_url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code

  seniors = []
  soup = BeautifulSoup(r.content, 'html.parser')
  seniors_str = soup.find_all('table', {"id": "pagetabla"})
  seniors_str = BeautifulSoup(
    str(seniors_str), 'html.parser').find_all("td", {"class": "jugador"})
  if seniors_str is not None:
    for senior_str in seniors_str:
      # print(senior_str.find('a')['href'][senior_str.find(
      #    'a')['href'].find('=')+1:])
      seniors.append(
        senior_str.find("a")["href"][senior_str.find("a")["href"].find("=")+1:]
      )

  return seniors


def enter_junior_roster(id_team, auth, session = None):
  """ Recorremos las páginas de canteras
    Devolvemos un array con los ids de los jugadores que
      conforman la cantera

  Keyword arguments:
    id_team -- Id del equipo al que se va a acceder a su cantera
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
  """

  if session is None:
    session = login(auth)

  jr_url = "http://es.ibasketmanager.com/plantilla.php?" + \
    "juveniles=1&id_equipo=" + str(id_team)

  r = session.get(jr_url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code

  juniors = []
  soup = BeautifulSoup(r.content, "html.parser")
  juniors_str = soup.find_all("table", {"id": "pagetabla"})
  juniors_str = BeautifulSoup(str(juniors_str), "html.parser").find_all(
    "td", {"class": "jugador"})
  if juniors_str is not None:
    print(juniors_str)
    for junior_str in juniors_str:
      # print(junior_str.find('a')['href'][junior_str.find(
      #    'a')['href'].find('=')+1:])
      # Sustituir por split()[1]
      juniors.append(
        junior_str.find("a")["href"][junior_str.find("a")["href"].find("=")+1:]
      )

  return juniors
