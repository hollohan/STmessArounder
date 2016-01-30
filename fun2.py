from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from time import sleep
from threading import Thread
from random import randint

# st system class
class stsystem:
	ip = ''
	sock = 0
	endrot = False
	msgs = [
			'PC:loadletter',
			'PCM2.0',
			'system|meltdown',
			'failure_802',
			'VS2_NOT_FOUND'
		]
	
	def __init__(self, ipadd):
		self.ip = ipadd
		try:
			self.sock = socket(AF_INET, SOCK_STREAM)
			self.sock.connect((self.ip, 17000))
			print('socket opened for %s [%s]' % (self.ip, self.sock.recv(16)))
		except:
			print('failed to open socket for ' + self.ip)
			self.ip = self.ip + ' FAILED'

	def destroy(self):
		self.sock.close()
		print('socket closed for ' + self.ip)
		
	
	def snd(self, msg):
		self.sock.send(bytes(msg + '\n', 'utf-8'))
		print ('msg sent to %s [%s]' % (self.ip, self.sock.recv(1024)))
		
	def display(self, msg):
		self.snd('display set countdown ' + msg + ' 1000')
		print ('display set on %s [%s]' % (self.ip, self.sock.recv(1024)))
		
	def led(self, color):
		choice = ['amber', 'white']
		if color in choice:
			self.snd('led intensity 100 ' + color)
		else:
			print ('invalid color[%s]', (color))
			return
		#print ('color set on %s' % (self.ip))
		
	def clear(self):
		self.snd('sys power')
		sleep(1)
		self.snd('sys power')
		
	def msgrot(self):
		while True:
			if self.endrot:
				self.clear()
				break
			self.display(self.msgs[randint(0,len(self.msgs)-1)])
			sleep(5)
			
	def ledblink(self, count):
		white = True
		for i in range(count):
			if white:
				self.led('white')
				white = False
			else:
				self.led('amber')
				white = True
			sleep(2)	
		
		
# globals
# '192.168.0.5' st20 luis
staddys = []
systems = []
started = False

# opts functions
def mkobjs():
	global started
	if started:
		print ('you cannot do this because you\'ve already started once')
		return
	started = True
	for addy in staddys:
		systems.append(stsystem(addy))
def help():
	print('\n\n')
	with open('banner.txt', 'r') as f:
		for line in f: print(line.rstrip())
	print('\n\t\t\t', end = '')
	for opt in opts:
		print(opt + ' ', end='')
	print('\n\n')
def showsystems():
	print()
	print ('id\tip')
	print ('--\t--')
	for i in range(len(systems)):
		print('%i:\t%s' % (i, systems[i].ip))
	print ()
def closeprog():
	for system in systems:
		system.destroy()
	exit()
def sndmsg():
	id = int(input('\tid: '))
	msg = input('\tmsg: ')
	systems[id].snd(msg)
def setdisplay():
	id = int(input('\tid: '))
	msg = input('\tmsg: ')
	systems[id].display(msg)
def setled():
	id = int(input('\tid: '))
	color = input('\tcolor: ')
	systems[id].led(color)
def cleardisp():
	id = int(input('\tid: '))
	systems[id].clear()
def addsys():
	if started:
		print ('you cannot add a system because this has already been started')
	userin = input('\tip: ')
	staddys.append(userin)
def rot():
	id = int(input('\tid: '))
	systems[id].endrot = False
	mythread = Thread(target=systems[id].msgrot)
	mythread.start()
def endrot():
	id = int(input('\tid: '))
	systems[id].endrot = True
def blink():
	id = int(input('\tid: '))
	cnt = int(input('\tcount: '))
	systems[id].ledblink(cnt)
		
		
	
	
# main
opts = {
			'start'		:mkobjs,
			'exit'		:closeprog,
			'send'		:sndmsg,
			'display'	:setdisplay,
			'led'		:setled,
			'clear'		:cleardisp,
			'?'			:help,
			'show'		:showsystems,
			'add'		:addsys,
			'rot'		:rot,
			'endrot'	:endrot,
			'blink'		:blink
}
help()
while True:
	userin = input('> ')
	if userin in opts:
		opts[userin]()