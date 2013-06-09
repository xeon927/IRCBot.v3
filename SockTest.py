import socket

HOST = "192.168.1.253"
PORT = 6667

nickname = "IRCBotV3"
username = "Steve"
realname = "Steve The (Python) Bot"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

channel = "#MLP,#ACorp"

loggedIn = firstPing = nickSent = userSent = nsUse = False
firstRun = True
string = str()

def servSend(message):
	sock.send((message + "\r\n").encode("utf-8"))

def joinChan(chanlist):
	servSend("JOIN %(0)s" % {"0": chanlist})

def runLogin():
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

try:
	while True:
		data = sock.recv(1).decode("utf-8")
		if data == "\r":
			sock.recv(1)
			print(string)

			#Check shit here
			string = str()
		string += data
except KeyboardInterrupt:
	servSend("QUIT :Killed by console.")
	print("Killing")
except:
	print("Well, fuck.")
