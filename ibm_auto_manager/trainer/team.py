# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from bson import ObjectId
from datetime import datetime


class Team:
  """ Representa un equipo """
  def __init__(self,
    id_team,
    name,
    id_user,
    user,
    arena,
    division,
    group,
    clasification,
    streak # racha de partidos
  ):
    self._id = ObjectId(id_team.zfill(24))
    self.id_user = ObjectId(id_user.zfill(24))
    self.name = name
    self.user = user
    self.arena = arena
    self.division = int(division)
    self.group = int(group)
    self.clasification = int(clasification)
    self.streak = int(streak)

  def to_db_collection(self):
    """Devuelve los datos del perfil en un formato legible de MongoDB."""
    return {
      "_id": self._id,
      "name": self.name,
      "id_user": self.id_user,
      "user": self.user,
      "arena": self.arena,
      "division": self.division,
      "group": self.group,
      "clasification": self.clasification,
      "streak": self.streak,
      "_date": datetime.now()
    }
