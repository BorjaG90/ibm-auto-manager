# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from datetime import datetime
from bson import ObjectId

from ibm_auto_manager.common import text


class Auction:
	"""Representa una línea de mercado, una subasta de un jugador."""

	def __init__(self,
							id_player,
							pos,
							avg,
							age,
							date_auction,
							offer
							):
		self._id = ObjectId((id_player + text.get_date_str(date_auction)).zfill(24))
		self.player = ObjectId(id_player.zfill(24))
		self.position = pos
		self.average = int(avg)
		self.age = int(age)
		self.date_auction = date_auction
		self.offer = int(offer.replace('.', ''))

	def __str__(self):
		return "Id: {}, {} de {} años y {} de media,\
		hasta el {} por {}€".format(
			self._id,
			self.position,
			self.age,
			self.average,
			self.date_auction,
			self.offer
		)

	def to_db_collection(self):
		"""Devuelve el dato de la subasta en un formato legible de MongoDB."""
		return {
			"_id": self._id,
			"position": text.pos_treatment(self.position),
			"age": self.age,
			"average": self.average,
			"date_auction": self.date_auction,
			"offer": self.offer,
			"_date": datetime.now(),
			"player": self.player
		}
