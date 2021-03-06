# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from datetime import datetime
from bson import ObjectId

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
    self._id = ObjectId(id_player.zfill(24))
    self.team_id = ObjectId(team_id.zfill(24))
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
      self._id,
      self.position,
      self.age,
      self.country
    )

  def to_db_collection(self):
    """Devuelve los datos del jugador en un formato legible de MongoDB."""
    return {
      "_id": self._id,
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
      "_date": datetime.now()
    }

class PlayerAtributes:
  """Representa los atributos de un jugador."""

  def __init__(self,
              id_player,
              power,
              ambition,
              leadership,
              exp,
              speed,
              jump,
              endurance,
              level,
              marking,
              rebound,
              block,
              recover,
              two,
              three,
              free,
              assist,
              dribbling,
              dunk,
              fight,
              mental,
              physic,
              defense,
              offense,
              total,
              loyalty
              ):
    self.player_id = ObjectId(id_player.zfill(24))
    self.power = int(power)
    self.ambition = int(ambition)
    self.leadership = int(leadership)
    self.exp = int(exp)
    self.speed = int(speed)
    self.jump = int(jump)
    self.endurance = int(endurance)
    self.level = int(level)
    self.marking = int(marking)
    self.rebound = int(rebound)
    self.block = int(block)
    self.recover = int(recover)
    self.two = int(two)
    self.three = int(three)
    self.free = int(free)
    self.assist = int(assist)
    self.dribbling = int(dribbling)
    self.dunk = int(dunk)
    self.fight = int(fight)
    self.mental = int(mental)
    self.physic = int(physic)
    self.defense = int(defense)
    self.offense = int(offense)
    self.total = int(total)
    self.loyalty = int(loyalty)

  def __str__(self):
    return "Id: {}, medias -> Tot: {}, Off: {}, Def: {}, \
    Mnt: {}, Fis: {}".format(
      self.player_id,
      self.total / 100,
      self.offense / 100,
      self.defense / 100,
      self.mental / 100,
      self.physic / 100
    )

  def to_db_collection(self):
    """Devuelve los atributos del jugador en un formato legible de MongoDB."""
    return{
      "_id": self.player_id,
      "power": self.power,
      "ambition": self.ambition,
      "leadership": self.leadership,
      "loyalty": self.loyalty,
      "exp": self.exp,
      "speed": self.speed,
      "jump": self.jump,
      "endurance": self.endurance,
      "level": self.level,
      "marking": self.marking,
      "rebound": self.rebound,
      "block": self.block,
      "recover": self.recover,
      "two": self.two,
      "three": self.three,
      "free": self.free,
      "assist": self.assist,
      "dribbling": self.dribbling,
      "dunk": self.dunk,
      "fight": self.fight,
      "mental": self.mental,
      "physic": self.physic,
      "defense": self.defense,
      "offense": self.offense,
      "total": self.total,
      "_date": datetime.now()
    }

  def to_db_collection_prog(self):
    """Devuelve la progresión del jugador en un formato legible de MongoDB."""
    return{
      "_id": ObjectId((str(int(str(self.player_id))) + text.get_date_str(datetime.now(), False)).zfill(24)),
      "player_id": self.player_id,
      "power": self.power,
      "ambition": self.ambition,
      "leadership": self.leadership,
      "loyalty": self.loyalty,
      "exp": self.exp,
      "speed": self.speed,
      "jump": self.jump,
      "endurance": self.endurance,
      "level": self.level,
      "marking": self.marking,
      "rebound": self.rebound,
      "block": self.block,
      "recover": self.recover,
      "two": self.two,
      "three": self.three,
      "free": self.free,
      "assist": self.assist,
      "dribbling": self.dribbling,
      "dunk": self.dunk,
      "fight": self.fight,
      "mental": self.mental,
      "physic": self.physic,
      "defense": self.defense,
      "offense": self.offense,
      "total": self.total,
      "_date": datetime.now()
    }
