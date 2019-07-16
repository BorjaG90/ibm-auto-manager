# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import sys

from ibm_auto_manager import app

if __name__ == '__main__':
	app.run(sys.argv[1]) if len(sys.argv)>1 else app.run()