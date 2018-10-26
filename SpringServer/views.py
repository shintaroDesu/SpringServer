# /usr/bin/env python3

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from SpringServer import data
from SpringServer import extern
import os

JAVA_PATH = "/Users/yuitora./Spring-Tweaker/"
JAVA_FILE_PATH = "out/production/Spring-Tweaker/"
JAVA_RES_COMMUNICATION = JAVA_PATH + "res/communication/"


def runJava(argument):
	os.chdir(JAVA_PATH + JAVA_FILE_PATH)
	os.system("java -cp .:../../../libs/* Spring " + argument)


@csrf_exempt
def loginAccount(request):
	try:
		username = request.POST['username']
		password = request.POST['password']
		runJava(" 1 " + username + " " + password)

		idFile = open(JAVA_RES_COMMUNICATION + "tmpID/" + username, "r")
		identifier = idFile.read()
		data.identifiers[identifier] = username

		return JsonResponse({"id": identifier, "update": "true"})
	except Exception as e:
		print(e)
		return JsonResponse({"update": "false"})


@csrf_exempt
def createAccount(request):
	try:
		username = request.POST['username']
		password = request.POST['password']
		runJava(" 2 " + username + " " + password)

		checkFile = open(JAVA_RES_COMMUNICATION + "checkCreated/" + username, "r")
		check = checkFile.read()
		return JsonResponse({"update": check})
	except Exception as e:
		print(e)
		return JsonResponse({"update": "false"})


@csrf_exempt
def hasPurchased(request):
	try:
		username = request.POST['username']
		runJava(" 3 " + username)

		checkFile = open(JAVA_RES_COMMUNICATION + "hasPurchased/" + username, "r")
		check = checkFile.read()

		return JsonResponse({"update": check})
	except Exception as e:
		print(e)
		return JsonResponse({"update": "false"})


@csrf_exempt
def purchase(request):
	try:
		username = request.POST['username']
		identifier = request.POST['identifier']
		if data.identifiers[identifier] != username:
			return JsonResponse({"update": "false"})

		ip = request.POST['ip']
		hwid = request.POST['hwid']

		location = extern.get_location(ip)

		runJava(" 4 " + username + hwid + location)
		checkFile = open(JAVA_RES_COMMUNICATION + "purchaseCheck/" + username, "r")
		check = checkFile.read()

		return JsonResponse({"update": check})
	except Exception as e:
		print(e)
		return JsonResponse({"update": "false"})


@csrf_exempt
def logout(request):
	try:
		username = request.POST['username']
		identifier = request.POST['identifier']
		if data.identifiers[identifier] != username:
			return JsonResponse({"update": "false"})
		os.system("rm " + JAVA_RES_COMMUNICATION + "tmpID/" + username)
		del data.identifiers[identifier]
		return JsonResponse({"update": "true"})
	except Exception as e:
		print(e)
		return JsonResponse({"update": "false"})
