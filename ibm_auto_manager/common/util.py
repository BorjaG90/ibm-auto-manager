# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import os
import time

def cls():
  """ Limpia la terminal según el sistema operativo """
  os.system('cls' if os.name=='nt' else 'clear')


def show(title):
  """ Devuelve la fecha con el objeto entre corchetes """
  return str("[" + title + "](" + time.strftime("%H:%M:%S") + ") ")
