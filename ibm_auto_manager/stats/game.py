# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from datetime import datetime
from bson import ObjectId

from ibm_auto_manager.common import text


class Game:
  """Representa un partido."""

  def __init__(self, 
      date_game,
      id_game, 
      type_game,
      home_id, 
      away_id, 
      assistance, 
      home_money, 
      away_money):
    self._id = ObjectId(id_game.zfill(24))
    self.date_game = date_game
    self.type_game = type_game
    self.home_id = ObjectId(home_id.zfill(24))
    self.away_id = ObjectId(away_id.zfill(24))
    self.assistance = int(assistance)
    self.home_money = int(home_money)
    self.away_money = int(away_money)

  def __str__(self):
    return "Partido de {}, Id: {} {}-{} Fecha: {}".format(
      self.type_game,
      self.game_id,
      self.home_id,
      self.away_id,
      self.date_game
    )

  def to_db_collection(self):
    """Devuelve los datos del partido en un formato legible de MongoDB."""
    return{
      "_id": self._id,
      "date_game": self.date_game,
      "type_game": self.type_game,
      "home_id": self.home_id,
      "away_id": self.away_id,
      "assistance": self.assistance,
      "home_money": self.home_money,
      "away_money": self.away_money
    }
