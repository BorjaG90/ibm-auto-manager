# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from bs4 import BeautifulSoup

from ibm_auto_manager.connection.login_page import login
from ibm_auto_manager.common.util import cls, show


def auto_bid(auth, play_aut_id = None):
  """ Auto-apuesta en una subasta por un jugador

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    play_aut_id -- id del jugador por el que pujar
  """
  #Login
  session = login(auth)

  print("\n\n")
  cls()

  if not play_aut_id:
    play_aut_id = input("Introduce el id del jugador: ")

  bid_url = 'http://es.ibasketmanager.com/ofertapuja.php?' \
    + 'acc=nuevo&id_jugador=' + str(play_aut_id)
  #http://es.ibasketmanager.com/ofertapuja.php?acc=nuevo&id_jugador=6345048
  print(show("auto-bid") + ' >{ ' + bid_url + ' }')

  r = session.get(bid_url)
  load_status=0
  while load_status!=200:
    load_status = r.status_code
  #make_bid(r.content,play_aut_id,auth)

  ###########################################################
  soup = BeautifulSoup(r.content, 'html.parser')
  final = soup.find("span",{"id":"claus"})
  # print(final)
  if(final!=None): #I can bid
    puja = final.find(text=True, recursive=False)
    puja_max = soup.find("span",{"id":"clausmax"}).find(text=True, recursive=False)
    fich = soup.find_all("div",{"class":"selector2"})[2].attrs['valor']
    ano = soup.find("span",{"id":"ano"}).find(text=True, recursive=False)
    print("\t\tPuja: " + str(puja))
    print("\t\tPujaMax: " + str(puja_max))
    print("\t\tFicha: " + str(fich))
    print("\t\tAños: " + str(ano))

    max_team = input(" Introduzca Puja máxima para el Equipo: ")
    min_player = input(" Introduzca Ficha minima para el Jugador: ")
    max_player = input(" Introduzca Ficha máxima para el Jugador: ")
    years = input(" Introduzca Años de Contrato: ")

    par = {
      "acc":"ofrecer",
      "tipo":"1",
      "id_jugador":str(play_aut_id),
      "clausula":str(puja),
      "clausulamax":str(max_team),
      "ficha":str(max_player),
      "anos":str(years)
    }
    session = login(auth)

    bid_up = 5000
    if(int(max_player)-int(min_player) < 5000):
      print(show("auto-bid") + "  >>Apuestas a 100")
      bid_up = 100
    elif(int(max_player)-int(min_player) < 25000):
      print(show("auto-bid") + "  >>Apuestas a 1000")
      bid_up = 1000
    for i in range(int(min_player),int(max_player)+1,bid_up):

      print(show("auto-bid") + " Bid: [" + str(i) + "€]")

      x_url = "http://es.ibasketmanager.com/ofertapuja.php?acc=" + par['acc']
      x_url = x_url + "&tipo=" + par['tipo'] + "&id_jugador=" + par['id_jugador']
      x_url = x_url + "&clausula=" + par['clausula'] + "&clausulamax=" + par['clausulamax']
      x_url = x_url + "&ficha=" + str(i) + "&anos=" + par['anos']
      # print(x_url)
      r = session.post(x_url)
      load_status=0
      while load_status!=200:
        load_status = r.status_code
      soup=BeautifulSoup(r.content, 'html.parser')
      # print('#########')
      # print(str(soup))
      # print('#########')
      final = soup.find("td",{"class":"formerror"})
      #
      if(final==None):
        print(show("auto-bid") + " }La apuesta es buena")
        #print(final.find(text=True, recursive=False))
        i=int(max_player)+2
        break
      elif(final=="El jugador pide más años de contrato."):
        break
      else:
        print(final.find(text=True, recursive=False))
    print(show("auto-bid") + " Fin de bucle")
  else:
    print(show("auto-bid") + " [No puedes pujar por este jugador]")

def auto_offer(auth, play_aut_id=None):
  """ Auto-oferta de renovacion por un jugador

  Keyword arguments:
    auth -- Cadena de autenticacion a la web.
    play_aut_id -- id del jugador por el que pujar
  """
  #Login
  session = login(auth)

  print("\n\n")
  cls()
  
  if not play_aut_id:
    play_aut_id = input("Introduce el id del jugador: ")

  bid_url = 'http://es.ibasketmanager.com/ofertarenovar.php?' \
    + 'acc=nuevo&tipo=4&id_jugador=' + str(play_aut_id)
  #http://es.ibasketmanager.com/ofertarenovar.php?acc=nuevo&tipo=4&id_jugador=7895726
  print(show("auto-offer") + ' >{ ' + bid_url + ' }')
  r = session.get(bid_url)
  load_status=0
  while load_status!=200:
    load_status = r.status_code
  #make_bid(r.content,play_aut_id,auth)

  ###########################################################
  soup = BeautifulSoup(r.content, 'html.parser')
  #print(soup)
  final = soup.find_all("div",{"class":"selector2"})[0].attrs['valor']
  print(final)
  if(final!=None): #I can bid
    fich = soup.find_all("div",{"class":"selector2"})[0].attrs['valor']
    ano = soup.find("span",{"id":"ano"}).find(text=True, recursive=False)
    print("\t\tFicha: " + str(fich))
    print("\t\tAños: " + str(ano))

    min_player = input("Introduzca Ficha minima para el Jugador: ")
    max_player = input("Introduzca Ficha máxima para el Jugador: ")
    years = input("Introduzca Años de Contrato: ")

    par = {
      "acc":"ofrecer",
      "tipo":"4",
      "id_jugador":str(play_aut_id),
      "clausula":str(0),
      "clausulamax":str(0),
      "ficha":str(max_player),
      "anos":str(years)
    }
    session = login(auth)

    bid_up = 5000
    if(int(max_player)-int(min_player) < 5000):
      print(show("auto-offer") + " >>Ofertas a 100")
      bid_up = 100
    elif(int(max_player)-int(min_player) < 25000):
      print(show("auto-offer") + " >>Ofertas a 1000")
      bid_up = 1000
    for i in range(int(min_player),int(max_player)+1,bid_up):

      print(show("auto-offer") + " Offer: [" + str(i) + "€]")

      x_url = "http://es.ibasketmanager.com/ofertarenovar.php?acc=" + par['acc']
      x_url = x_url + "&tipo=" + par['tipo'] + "&id_jugador=" + par['id_jugador']
      x_url = x_url + "&clausula=" + par['clausula'] + "&clausulamax=" + par['clausulamax']
      x_url = x_url + "&ficha=" + str(i) + "&anos=" + par['anos']
      #print(x_url)
      r = session.post(x_url)
      load_status=0
      while load_status!=200:
        load_status = r.status_code
      soup=BeautifulSoup(r.content, 'html.parser')
      # print('#########')
      # print(str(soup))
      # print('#########')
      
      final = soup.find("td",{"class":"formerror"})
      print(final.find(text=True, recursive=False))
      if(final==None):
        print(show("auto-offer") + " La apuesta es buena")
        #print(final.find(text=True, recursive=False))
        i=int(max_player+2)
        break
      elif(final=="El jugador pide más años de contrato."):
        break
    print(show("auto-offer") + " Fin de bucle")
  else:
    print(show("auto-offer") + " [No puedes renovar este jugador]")