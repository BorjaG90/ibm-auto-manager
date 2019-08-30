# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import requests

from ibm_auto_manager.common.util import show

def login(payload):
	""" Devuelve una sesión logueada en la web de IBM
		con la cual hacer peticiones.
	Se usara tambien para renovar la llamada cada vez que sea
	susceptible de caducarse la sesión """

	session = requests.session()

	login_url = 'http://es.ibasketmanager.com/loginweb.php'

	r = session.post(login_url, data=payload)

	load_status = 0
	while load_status != 200:
		load_status = r.status_code
	print(show("login") + "[[Relogging]]")
	return session
