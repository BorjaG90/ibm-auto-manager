# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import datetime


class Profile:
  def __init__(self, 
              id, 
              username, 
              team_name, 
              money, 
              color_prim, 
              color_sec,
              club_seats, # socios
              fans, # aficionados
              ranking,
              streak, # racha de partidos

              ):
    self.id = int(id)
    self.username = str(username)
    self.team_name = str(team_name)
    self.money = int(money)
    self.color_prim = str(color_prim)
    self.color_sec = str(color_sec)
    self.club_seats = int(club_seats)
    self.fans = int(fans)
    self.ranking = int(ranking)
    self.streak = int(streak)

  def to_db_collection(self):
    """Devuelve los datos del perfil en un formato legible de MongoDB."""
    return {
      "id": self.id,
      "username": self.username,
      "team_name": self.team_name,
      "money": self.money,
      "color_prim": self.color_prim,
      "color_sec": self.color_sec,
      "club_seats": self.club_seats,
      "fans": self.fans,
      "ranking": self.ranking,
      "streak": self.streak,
      "_date": datetime.datetime.now()
    }