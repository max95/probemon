#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import string

# read file "config" for login, passwd,...
flux = open( "config" ).readlines()
lines = [ l.strip().split("=") for l in flux if not l.startswith("#")]
dico_cfg = {}
for l in lines:
	#la clef c'est le terme de gauche, la valeur celui de droite
	dico_cfg[ l[0] ] = l[1]
db = dico_cfg["db"]
table = dico_cfg["table"]
host = dico_cfg["host"]
login = dico_cfg["login"]
passwd = dico_cfg["passwd"]

try:
	db = MySQLdb.connect(host=dico_cfg["host"],user=dico_cfg["login"],passwd=dico_cfg["passwd"])
	print "Connexion réussie"
except Exception:
	print "Erreur connection Mysql"
else:
	cur = db.cursor()
	requete = 'DROP DATABASE IF EXISTS '+ dico_cfg["db"]
	try:
		cur.execute (requete)
		print "BASE supprimée"
	except Exception:
		db.close()
	else:
		requete = 'CREATE DATABASE '+ dico_cfg["db"]
		try :
			cur.execute (requete)
		except Exception:
			db.close()
			print "impossible de créer la base"
		else:
			try:
				db = MySQLdb.connect(host=dico_cfg["host"],user=dico_cfg["login"],passwd=dico_cfg["passwd"], db=dico_cfg["db"])
			except Exception:
				print "impossible de sec onnecter à la nouvelle base"
			else:
				try:
					requete = 'DROP TABLE IF EXISTS '+ dico_cfg["table"]
					cur.execute
				except Exception:
					print "erreur lors de la suppression de la table"
				else:
					print "Table supprimée"
					requete = 'CREATE TABLE '+dico_cfg["db"]+'.'+dico_cfg["table"]+' (`date` int(10) NOT NULL,`source` varchar(17) NOT NULL,`firm` varchar(50),`rssi` int,`ssid` varchar(32),PRIMARY KEY (`date`,`source`)) ENGINE=InnoDB DEFAULT CHARSET=latin1'
					cur.execute (requete)
					print "La table est créée"
