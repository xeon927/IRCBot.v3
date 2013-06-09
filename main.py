import socket
import re

#Server Settings
HOST = "192.168.1.253"
PORT = 6667

#Bot Settings
nickname = "IRCBotV3"
username = "Steve"
realname = "Steve The (Python) Bot"
channel = "#test"
owner = "xeon927"

#NickServ Settings
nsUse = False
nsPass = "Herpaderpa"

loggedIn = firstPing = nickSent = userSent = canRegex = False
firstRun = True
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
	string = str()
	try:
		servConnect()
		while True:
			data = sock.recv(1).decode("utf-8")
			if data == "\r":
				sock.recv(1)
				if not string[:6] == "PING :":
					print("<<< " + string)
				check(string)
				if not loggedIn:
					runLogin()
				string = str()
				data = str()
			string += data
	except KeyboardInterrupt:
		servSend("QUIT :Killed by console.")
	#except:
		#print("Something went wrong!")
def servConnect():
	sock.connect((HOST, PORT))

def runLogin():
	global firstRun, nickSent, firstPing, userSent, loggedIn, canRegex
	if firstRun:
		firstRun = False
		return
	if not nickSent:
		servSend("NICK %(0)s" % {"0": nickname})
		nickSent = True
		return
	if firstPing:
		if not userSent:
			servSend("USER %(0)s %(1)s %(1)s :%(2)s" % {"0": username, "1": "null", "2": realname})
			userSent = True
			return
		if nsUse:
			sendNickServ()
		joinChan(channel)
		loggedIn = True
		canRegex = True

#Basic Server Stuff
def servSend(message):
	sock.send((message + "\r\n").encode("utf-8"))
	if not message[:6] == "PONG :":
		print(">>> " + message)
def joinChan(chanlist):
	servSend("JOIN %(0)s" % {"0": chanlist})
def partChan(chanlist):
	servSend("PART %(0)s" % {"0": chanlist})
def sendNickServ():
	servSend("PRIVMSG NickServ IDENTIFY %(0)s" % {"0": nsPass})
	
#Message Checking
def check(message):
	checkPing(message)
	checkDisconnect(message)
def checkPing(message):
	global firstPing
	if len(message) > 6:
		if message[:6] == "PING :":
			servSend("PONG :" + message[6:])
			if not firstPing:
				firstPing = True
def checkDisconnect(message):
	global canRegex, loggedIn, firstPing, nickSent, userSent, firstRun
	if len(message) >= len("ERROR :CLOSING LINK:"):
		if message[:len("ERROR :CLOSING LINK:")] == "ERROR :CLOSING LINK:":
			canRegex = loggedIn = firstPing = nickSent = userSent = firstRun = False
			main()

#Regular Expressions and Stuff
def msgRegex(request, message):
	#Use:
	#msgRegex("nickname", message) for nickname
	#msgRegex("username", message) for username
	#msgRegex("hostname", message) for hostname
	#msgRegex("channel", message) for channel
	#msgRegex("message", message) for message
	global canRegex
	if canRegex:
		regexPattern = r"^:(?P<nickname>.+?)!(?P<username>.+?)@(?P<hostname>.+?)\ PRIVMSG\ (?P<channel>.+?)\ :(?P<message>.+?)$"
		if re.match(regexPattern, message):
			m = re.match(regexPattern, message)
			return m.group(request)
		
main()