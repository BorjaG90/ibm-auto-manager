# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from bs4 import BeautifulSoup

from ibm_auto_manager.common.util import show
from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.general import profile


def get_profile_data(auth, db):
  """ Obtenemos los datos del perfil del usuario actual

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
  """

  session = login(auth)

  url = 'http://es.ibasketmanager.com/inicio.php'
  r = session.get(url)
  load_status = 0
  while load_status != 200:
    load_status = r.status_code
  
  print(show("profile") + " > Analizando perfil")

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
  v_profile = profile.Profile(
    id_team, username, team_name, money, color_prim, color_sec)

  if (db.profile.find_one({"id": int(id_team)}) is not None):
    db.profile.replace_one(
      {"id": int(id_team)}, v_profile.to_db_collection())
  else:
    db.profile.insert_one(v_profile.to_db_collection())

  print(show("profile") + " > Perfil actualizado")