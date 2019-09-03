# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from datetime import datetime
from bson import ObjectId

from ibm_auto_manager.common import text


class TeamStats:
  """Representa las estadisticas hechas por un equipo en un partido."""

  def __init__(self,
      id_stats,
      game_id,
      team_id,
      points, t2c, t2i, t3c, t3i, tlc, tli, rebd, rebo, ass, 
      ste, turn, blkf, blkc, foulr, foulc, val):
    self._id = ObjectId(id_stats.zfill(24))
    self.game_id = ObjectId(game_id.zfill(24))
    self.team_id = ObjectId(team_id.zfill(24))
    self.points = int(points)
    self.t2c = int(t2c)
    self.t2i = int(t2i)
    self.t3c = int(t3c)
    self.t3i = int(t3i)
    self.tlc = int(tlc)
    self.tli = int(tli)
    self.rebd = int(rebd)
    self.rebo = int(rebo)
    self.ass = int(ass)
    self.ste = int(ste)
    self.turn = int(turn)
    self.blkf = int(blkf)
    self.blkc = int(blkc)
    self.foulr = int(foulr)
    self.foulc = int(foulc)
    self.val = int(val)

  def __str__(self):
    return "ID: {}, Game: {}, Team:{} -> {} pts, {} 3s, {} valoracion".format(
      self._id,
      self.game_id,
      self.team_id,
      self.points,
      self.t3c,
      self.val
    )

  def to_db_collection(self):
    """Devuelve las estadisticas del equipo en el partido
     en un formato legible de MongoDB."""
    return {
      "_id": self._id,
      "game_id": self.game_id,
      "team_id": self.team_id,
      "points": self.points,
      "t2i": self.t2i,
      "t2c": self.t2c,
      "t3i": self.t3i,
      "t3c": self.t3c,
      "tli": self.tli,
      "tlc": self.tlc,
      "rebd": self.rebd,
      "rebo": self.rebo,
      "ass": self.ass,
      "ste": self.ste,
      "turn": self.turn,
      "blkf": self.blkf,
      "blkc": self.blkc,
      "foulr": self.foulr,
      "foulc": self.foulc,
      "val": self.val
    }
    