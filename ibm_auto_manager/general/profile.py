# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from datetime import datetime
from bson import ObjectId


class Profile:
  def __init__(self, 
              id_user, 
              username,
              id_team, 
              team_name, 
              money, 
              color_prim, 
              color_sec,
              club_seats, # socios
              fans, # aficionados
              ranking_team,
              streak, # racha de partidos

              ):
    self._id = ObjectId(id_user.zfill(24))
    self.username = str(username)
    self.team_id = ObjectId(id_team.zfill(24))
    self.team_name = str(team_name)
    self.money = int(money)
    self.color_prim = str(color_prim)
    self.color_sec = str(color_sec)
    self.club_seats = int(club_seats)
    self.fans = int(fans)
    self.ranking_team = int(ranking_team)
    self.streak = int(streak)

  def to_db_collection(self):
    """Devuelve los datos del perfil en un formato legible de MongoDB."""
    return {
      "_id": self._id,
      "username": self.username,
      "team_id": self.team_id,
      "team_name": self.team_name,
      "money": self.money,
      "color_prim": self.color_prim,
      "color_sec": self.color_sec,
      "club_seats": self.club_seats,
      "fans": self.fans,
      "ranking_team": self.ranking_team,
      "streak": self.streak,
      "_date": datetime.now()
    }