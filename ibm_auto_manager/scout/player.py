# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import datetime

from ibm_auto_manager.common import text


class Player:
  """Representa un jugador."""

  def __init__(self,
                id_player,
                team_id,
                name,
                position,
                age,
                heigth,
                weight,
                canon,
                salary,
                clause,
                years,
                juvenil,
                country
                ):
    self.id_player = int(id_player)
    self.team_id = int(team_id)
    self.name = name
    self.position = position
    self.age = int(age)
    self.heigth = int(heigth)
    self.weight = int(weight)
    self.canon = int(canon)
    self.salary = int(salary)
    self.clause = int(clause)
    self.years = int(years)
    self.juvenil = juvenil
    self.country = country

  def __str__(self):
    return "{} con Id: {}, {} de {} años de {}".format(
      self.name,
      self.id_player,
      self.position,
      self.age,
      self.country
    )

  def to_db_collection(self):
    """Devuelve los datos del jugador en un formato legible de MongoDB."""
    return {
      "id_player": self.id_player,
      "team_id": self.team_id,
      "name": self.name,
      "position": text.pos_treatment(self.position),
      "age": self.age,
      "heigth": self.heigth,
      "weight": self.weight,
      "canon": self.canon,
      "salary": self.salary,
      "clause": self.clause,
      "years": self.years,
      "juvenil": self.juvenil,
      "country": self.country,
      "_date": datetime.datetime.now()
    }
