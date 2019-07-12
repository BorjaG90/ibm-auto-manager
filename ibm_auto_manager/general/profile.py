# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'


class Profile:
  def __init__(self, id, money):
    self.id = int(id)
    self.money = int(money)

  def to_db_collection(self):
    """Devuelve los datos del perfil en un formato legible de MongoDB."""
    return {
      "id": self.id,
      "money": self.money
    }