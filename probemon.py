#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import argparse
import netaddr
import sys
import logging
import MySQLdb
import string
from scapy.all import *
from pprint import pprint
from logging.handlers import RotatingFileHandler

NAME = 'probemon'
DESCRIPTION = "a command line tool for logging 802.11 probe request frames"

DEBUG = False

def build_packet_callback(time_fmt, logger, delimiter, mac_info, ssid, rssi, mysql):
	# read file "config" for login, passwd,...
	flux = open( "config" ).readlines()
	lines = [ l.strip().split("=") for l in flux if not l.startswith("#")]
	dico_cfg = {}
	for l in lines:
		#la clef c'est le terme de gauche, la valeur celui de droite
		dico_cfg[ l[0] ] = l[1]

	def packet_callback(packet):
		if not packet.haslayer(Dot11):
			return

		# we are looking for management frames with a probe subtype
		# if neither match we are done here
		if packet.type != 0 or packet.subtype != 0x04:
			return

		# list of output fields
		fields = []

		# determine preferred time format
		log_time = str(int(time.time()))
		if time_fmt == 'iso':
			log_time = datetime.datetime.now().isoformat()

		fields.append(log_time)

		# append the mac address itself
		fields.append(packet.addr2)

		# parse mac address and look up the organization from the vendor octets
		if mac_info:
			try:
				parsed_mac = netaddr.EUI(packet.addr2)
				fields.append(parsed_mac.oui.registration().org)
				orga = parsed_mac.oui.registration().org
			except netaddr.core.NotRegisteredError, e:
				fields.append('UNKNOWN')
				orga = "UNKNOWN"

		# include the SSID in the probe frame
		if ssid:
			fields.append(packet.info)

		if rssi:
			rssi_val = -(256-ord(packet.notdecoded[-4:-3]))
			fields.append(str(rssi_val))


		# ajout BDD
		# connection BDD
		if mysql:
			try:
				db = MySQLdb.connect(host=dico_cfg["host"],user=dico_cfg["login"],passwd=dico_cfg["passwd"], db=dico_cfg["db"])
			except Exception:
				print "Erreur connection Mysql"
 			else:
				cur = db.cursor()
				requete='insert into '+dico_cfg['table']+' (date, source, firm, rssi ,ssid) values (%s,%s,%s,%s,%s)'
				table = dico_cfg["table"]
				try:
					cur.execute (requete, (log_time, packet.addr2, orga, str(rssi_val), packet.info))
				except Exception:
					db.close()
				else:
					db.commit()
					db.close()
		else:
			logger.info(delimiter.join(fields))
	return packet_callback

def main():
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	parser.add_argument('-i', '--interface', help="capture interface")
	parser.add_argument('-t', '--time', default='iso', help="output time format (unix, iso)")
	parser.add_argument('-o', '--output', default='probemon.log', help="logging output location")
	parser.add_argument('-b', '--max-bytes', default=5000000, help="maximum log size in bytes before rotating")
	parser.add_argument('-c', '--max-backups', default=99999, help="maximum number of log files to keep")
	parser.add_argument('-d', '--delimiter', default='\t', help="output field delimiter")
	parser.add_argument('-f', '--mac-info', action='store_true', help="include MAC address manufacturer")
	parser.add_argument('-s', '--ssid', action='store_true', help="include probe SSID in output")
	parser.add_argument('-r', '--rssi', action='store_true', help="include rssi in output")
	parser.add_argument('-D', '--debug', action='store_true', help="enable debug output")
	parser.add_argument('-l', '--log', action='store_true', help="enable scrolling live view of the logfile")
	parser.add_argument('-m', '--mysql',action='store_true', help="save into mysql")
	args = parser.parse_args()

	if not args.interface:
		print "error: capture interface not given, try --help"
		sys.exit(-1)
	
	DEBUG = args.debug

	# setup our rotating logger
	logger = logging.getLogger(NAME)
	logger.setLevel(logging.INFO)
	handler = RotatingFileHandler(args.output, maxBytes=args.max_bytes, backupCount=args.max_backups)
	logger.addHandler(handler)
	if args.log:
		logger.addHandler(logging.StreamHandler(sys.stdout))
	built_packet_cb = build_packet_callback(args.time, logger, 
		args.delimiter, args.mac_info, args.ssid, args.rssi, args.mysql)
	

	# tracking
	sniff(iface=args.interface, prn=built_packet_cb, store=0)
	
	# fermeture BDD
	conn.close()

if __name__ == '__main__':
	main()
