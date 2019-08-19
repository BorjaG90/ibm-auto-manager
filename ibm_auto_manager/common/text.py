# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import datetime
import re

from bs4 import BeautifulSoup

reg_date_full = r'(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|\
(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|\
(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))\
(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)\
(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|\
(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:\
(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|\
(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})'
reg_month = r'(Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Oct|Nov|Dic)'
reg_day = r'(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo)'
reg_hour = r'(([01]\d|2[0-3]):([0-5]\d)|24:00)'


def pos_treatment(position):
  """ Tratamiento de las posiciones de los jugadores """
  return position.replace("SF", "A").replace("PF", "AP").replace(
    "C", "P").replace("PG", "B").replace("SG", "E").replace(
    "Base", "B").replace("Escolta", "E").replace(
    "Alero", "A").replace("Ala-pivot", "AP").replace("Pivot", "P")


def date_translation(html_content):
  """Transform short date format to standard date format.
    Keyword arguments:
      html_content -- String who represents a date in diverse formats.
  """
  # Remove the hour
  html_content = html_content.replace(re.search(
    r'\s\d{1,2}:\d{1,2}', html_content).group(0), '')

  if re.search("Hoy", html_content) is not None:
    # print("Hoy")
    return '{}/{}/{}'.format(str(datetime.datetime.now().day).zfill(2), \
      str(datetime.datetime.now().month).zfill(2), datetime.datetime.now().year)

  elif re.search("Ayer", html_content) is not None:
    # print("Ayer")
    return '{}/{}/{}'.format(str(datetime.datetime.now().day -1).zfill(2), \
      str(datetime.datetime.now().month).zfill(2), datetime.datetime.now().year)

  elif re.search(reg_month, html_content) is not None:
    day = re.search(r'\d{1,2}', html_content).group(0).replace(' ', '')
    month_str = re.search(reg_month, html_content).group(0)
    if(month_str == 'Ene'):
      month = 1
    elif(month_str == 'Feb'):
      month = 2
    elif(month_str == 'Mar'):
      month = 3
    elif(month_str == 'Abr'):
      month = 4
    elif(month_str == 'May'):
      month = 5
    elif(month_str == 'Jun'):
      month = 6
    elif(month_str == 'Jul'):
      month = 7
    elif(month_str == 'Ago'):
      month = 8
    elif(month_str == 'Sep'):
      month = 9
    elif(month_str == 'Oct'):
      month = 10
    elif(month_str == 'Nov'):
      month = 11
    elif(month_str == 'Dic'):
      month = 12
    if(month < datetime.datetime.now().month):
      year = datetime.datetime.now().year - 1
    else:
      year = datetime.datetime.now().year
    return '{}/{}/{}'.format(str(day).zfill(2), str(month).zfill(2), year)

  elif re.search(reg_day, html_content) is not None:
    day = re.search(r'\d{1,2}', html_content).group(0).replace(' ', '')
    if(int(day) < datetime.datetime.now().day):
      if(datetime.datetime.now().month == 1):
        month = 12
      else:
        month = datetime.datetime.now().month - 1
    else:
      month = datetime.datetime.now().month
    if(month < datetime.datetime.now().month):
      year = datetime.datetime.now().year - 1
    else:
      year = datetime.datetime.now().year
    return '{}/{}/{}'.format(str(day).zfill(2), str(month).zfill(2), year)
    
  else:
    pass
    # print(html_content)

  return html_content


def date_market_translation(html_content):
  """Transform short date format to standard date format.

    Keyword arguments:
      html_content -- String who represents a date in diverse formats.
  """
  soup = BeautifulSoup(html_content, 'html.parser')
  html_content = str(soup).replace('&nbsp;', ' ').replace(
    '&aacute;', 'á').replace('&eacute;', 'é').replace(
      '&iacute;', 'í').replace('&oacute;', 'ó').replace('&uacute;', 'ú')
  hr = re.search(reg_hour, html_content).group(0)
  # print(html_content)
  hour = int(hr.split(':')[0])
  minutes = int(hr.split(':')[1])
  # print('{}:{}'.format(hour,minutes))
  today = datetime.datetime.today()
  if(re.search(reg_day, html_content) is not None):
    h = str(html_content).split('\xa0')
    while(int(today.strftime("%d")) != int(h[1])):
      today = today + datetime.timedelta(days=1)
  elif(re.search('MaÃ±ana', html_content) is not None or re.search(
      'Mañana', html_content) is not None):
    today = today + datetime.timedelta(days=1)
  elif(re.search('Hoy', html_content) is not None):
    pass
  else:
    print('\t[Market-COMPROBAR]:' + html_content)
  today = today.replace(
    hour=hour,
    minute=minutes
  )

  return today
    

def get_date_str(p_date, seconds = True):
  """ Devuelve la cadena de una fecha """
  if(seconds):
    res = str(str(p_date.year) +  str(p_date.month) + str(p_date.day) + str(p_date.hour) + str(p_date.minute))
  else:
    res = str(str(p_date.year) +  str(p_date.month) + str(p_date.day))

  return res
