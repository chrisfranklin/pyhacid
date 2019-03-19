#!/usr/bin/python
#-*-coding: utf-8-*-
# ncidha is a python ncid-client to pass caller id data to home assistant
import json
import logging
import os
import re
import socket
import time

from string import Template 

import requests


logging.basicConfig(level=logging.DEBUG)

ncid_host = os.getenv("NCID_HOST", "127.0.0.1")
ncid_port = int(os.getenv("NCID_PORT", 3333))
ncid_connected = False

ha_url = os.getenv("HA_URL")
ha_token = os.getenv("HA_TOKEN")

alexa_announce = bool(os.getenv("ALEXA_ANNOUNCE", True))
alexa_push = bool(os.getenv("ALEXA_PUSH", True))
alexa_targets = os.getenv("ALEXA_TARGETS", None)

notify_services = os.getenv("NOTIFY_SERVICES", None)

message_template = Template(os.getenv("MESSAGE_TEMPLATE", "$cid is calling."))
alexa_title_template = Template(os.getenv("ALEXA_TITLE", "Call on Home Phone"))

ha_headers = {
	'Authorization': "Bearer {}".format(ha_token),
}


def incomingCall(call):
	logging.debug(call)
	nmbr = re.search(r"(NMBR\*)([\w]*-[\w]*)(\*)", call).group(2)
	name = re.search(r"(NAME\*)([0-9a-zA-Z_ ]*)(\*)", call).group(2)
	logging.debug("Name: {}, Number: {}".format(name, nmbr))
	if name == "NO NAME":
		cid = nmbr
	else:
		cid = name
	return cid

def notify_alexa(message, notification_type, targets, title=None):
	url = ha_url + "services/notify/alexa_media"
	data = {
		"message": message,
		"data": {"type": notification_type},
		"target": targets
	}
	if notification_type == "push" or "announce":
		if title:
			data["title"] = title
		else:
			data["title"] = message
	payload = json.dumps(data)
	response = requests.post(url, data=payload, headers=ha_headers, verify=False)
	logging.debug(response.text)
	return response

def notify_service(message, target):
	url = "{}services/notify/{}".format(ha_url, target)
	data = {
		"message": message,
	}
	payload = json.dumps(data)
	response = requests.post(url, data=payload, headers=ha_headers, verify=False)
	logging.debug(response.text)
	return response

def main():
	logging.info("Connecting to ncidd server at {}:{}".format(ncid_host, ncid_port))
	ncid_connected = True
	while True:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect((ncid_host, ncid_port))
			data = s.recv(1024)
			if data[:4] == "CID:":
				cid = incomingCall(data[:-1])
				logging.info("Call from {}".format(cid))
				message = message_template.substitute(cid=cid)
				targets = alexa_targets.split(',')
				if alexa_targets:
					alexa_title = alexa_title_template.substitute(cid=cid)
					if alexa_announce:
						logging.debug("Announcing to target Alexa devices: {}".format(targets))
						notify_alexa(message, "announce", targets)
					if alexa_push:
						logging.debug("Pushing to 1st target Alexa device only: {}".format(targets[0]))
						notify_alexa(message, "push", [targets[0]], title=alexa_title)
				if notify_services:
					for service in notify_services.split(','):
						notify_service(message, service)
			time.sleep(0.1)
		except socket.error as e:
			logging.error(e)
			ncid_connected = False
			s = socket.socket()
			logging.info( "Connection lost... reconnecting." )
			while not ncid_connected:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				try:
					s.connect((ncid_host, ncid_port))
					ncid_connected = True
					logging.info("Reconnected.")
				except socket.error:
					time.sleep(2)
		except:
			raise
		finally:
			s.close()

if __name__ == "__main__":
	main()
