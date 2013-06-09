import socket
#import strings

#Server Settings
HOST = "192.168.1.253"
PORT = 6667

#Bot Settings
nickname = "IRCBotV3"
username = "Steve"
realname = "Steve The (Python) Bot"
channel = "#MLP,#ACorp"

#NickServ Settings
nsUse = False
nsPass = "Herpaderpa"

loggedIn = firstPing = nickSent = userSent = canRegex= False
firstRun = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def main():
	string = str()
	try:
		while True:
			data = sock.recv(1).decode("utf-8")
			if data == "\r":
				sock.recv(1)
				print("<<< " + string)
				check(string)
				if not loggedIn:
					runLogin()
				string = str()
				data = str()
			string += data
	except KeyboardInterrupt:
		servSend("QUIT :Killed by console.")
		print("Killing")
	#except:
		#print("Well, fuck.")

def runLogin():
	global firstRun, nickSent, firstPing, userSent, loggedIn
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

def servSend(message):
	sock.send((message + "\r\n").encode("utf-8"))
	print(">>> " + message)

def joinChan(chanlist):
	servSend("JOIN %(0)s" % {"0": chanlist})

def sendNickServ():
	servSend("PRIVMSG NickServ IDENTIFY %(0)s" % {"0": nsPass})
	
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
	canRegex = loggedIn = firstPing = nickSent = userSent = firstRun = False
	if len(message) >= len("ERROR :CLOSING LINK:"):
		if message[:len("ERROR :CLOSING LINK:")] == "ERROR :CLOSING LINK:":
			
main()