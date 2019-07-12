# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from ibm_auto_manager.common.util import cls, show

def enter_market(auth, db):
  """ Recorremos las páginas de mercado

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    db -- Objeto de conexion a la BD.
  """

  db.market.delete_many({})
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

