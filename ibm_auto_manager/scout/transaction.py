# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from datetime import datetime
from bson import ObjectId

from ibm_auto_manager.common import text


class Transaction:
  """Representa una transacción de un jugador de un equipo a otro
    en una fecha especifica.

  Keyword arguments:
  id_player -- id of the player.
  id_date_buy -- date of transaction in numeric format.
  age -- age of the player at the moment of the transaction.
  avg -- average points at the moment of the transaction.
  pos -- position of the player.
  price -- cost of the player.
  salary -- salary of the player.
  type_buy -- [Subasta/Compra directa/Traspaso pactado/Clausulazo]
  date_buy -- date of transaction in date format.
  """

  def __init__(self,
              id_player,
              id_date_buy,
              age,
              avg,
              pos,
              price,
              type_buy,
              salary=None,
              date_buy=None
              ):
    self.player_id = ObjectId(id_player.zfill(24))
    self._id = ObjectId(id_date_buy.zfill(24))
    self.age = int(age)
    self.average = int(avg)
    self.position = pos
    self.price = int(price.replace('.', ''))
    self.salary = int(salary.replace('.', ''))
    self.type_buy = type_buy
    self.date_buy = date_buy

  def __str__(self):
    return 'Id: {} {} de {} años, con {} de media\n\tVendido en {} por {}€\
    , cobrando {}€ en la fecha {},{}'.format(
      self.player_id,
      self.position,
      self.age,
      self.average,
      self.type_buy,
      self.price,
      self.salary,
      self.date_buy,
      self._id
    )

  def to_db_collection(self):
    """Devuelve los datos del jugador en un formato legible de MongoDB."""
    return {
      "_id": self._id,
      "player_id": self.player_id,
      "age": self.age,
      "average": self.average,
      "position": text.pos_treatment(self.position),
      "price": self.price,
      "salary": self.salary,
      "type_buy": self.type_buy,
      "date_buy": self.date_buy,
      "_date": datetime.now()
    }
