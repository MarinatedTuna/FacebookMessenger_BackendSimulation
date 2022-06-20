import socket
import sys
from thread import *
import getpass
import os

'''
Function Definition
'''
def receiveThread(s):
	while True:
		try:
			reply = s.recv(4096) # receive msg from server
			msg = reply
			for i in msg:
				if i == '<':
					msg = msg.replace(i, ',')
				elif i == '>':
					msg = msg.replace(i, ' ')
			print msg
				
			# You can add operations below once you receive msg
			# from the server

		except:
			print "Connection closed"
			break
	

def tupleToString(t):
	s = ""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
try:
	# create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();
print 'Socket Created'

'''
Resolve Hostname
'''
host = '10.0.0.4'
port = 9487
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()
print 'Ip address of ' + host + ' is ' + remote_ip

'''
Connect to remote server
'''
s.connect((remote_ip , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip

'''
TODO: Part-1.1, 1.2: 
Enter Username and Passwd
'''

username = raw_input("Please enter your username\n")
s.sendall(username)
password = getpass.getpass(prompt="Please enter your password\n", stream = None)
s.sendall(password)

#for debugging
#print("Username: " + username)
#print("Password: " + password)

#userpass = username + password
#userpass = stringToTuple(userpass)

# Whenever a user connects to the server, they should be asked for their username and password.
# Username should be entered as clear text but passwords should not (should be either obscured or hidden). 
# get username from input. HINT: raw_input(); get passwd from input. HINT: getpass()

# Send username && passwd to server
# sendall twice, receive twice later
#s.sendall(username)
#s.sendall(password)

#add option to view message

'''
TODO: Part-1.3: User should log in successfully if username and password are entered correctly. A set of username/password pairs are hardcoded on the server side. 
'''
welcome = s.recv(1024)
#print welcome

reply = s.recv(5)
#print reply
if reply == "valid": # TODO: use the correct string to replace xxx here!
	print 'Username and password valid'
        print welcome
	# Start the receiving thread
	start_new_thread(receiveThread ,(s,))

	'''
	Part-2:TODO: Please printout the number of unread message once a new client login
	'''
	
	count = s.recvfrom(1024)
	count = tupleToString(count)

	if str(count[0:1]) == '9' and str(count[1:2]) == '9':
		print('You have ' + str(count[:2]) + '+ unread messages\n')
	elif str(count[1:2]) != '<':
		print('You have ' + str(count[:2]) + ' unread messages\n')	
	else:
		print('You have ' + str(count[:1]) + ' unread messages\n') 

	message = ""

	start_new_thread(receiveThread, (s,))

	while True :

		#receiveThread(s) #for broadcast message


		# TODO: Part-1.4: User should be provided with a menu. Complete the missing options in the menu!
		message = raw_input("Choose an option (type the number): \n 1. Logout \n 2. Post a message \n 3. Change password \n 4. Group configuration \n 5. Offline message \n ")
		
		try :
			# TODO: Send the selected option to the server
			# HINT: use sendto()/sendall()
			if message == str(1):
				print 'Logout'
				s.sendall(message)
				# TODO: add logout operation
				#sys.exit()
				break
			elif message == str(2):
				print 'Post a message'
				s.sendall(message)
			# Add other operations, e.g. change password
				while True:
					message = raw_input("Choose an option (type the number): \n 1. Private messages \n 2. Broadcast messages \n 3. Group messages \n")
					s.sendall(message)
					try :
						'''
						Part-2:TODO: Send option to server
						'''
						if message == str(1):
							pmsg = raw_input("Enter your private message\n")
							try :
								'''
								Part-2:TODO: Send private message
								'''
								s.sendall(pmsg)
							except socket.error:
								print 'Private Message Send failed'
								sys.exit()
							rcv_id = raw_input("Enter the recevier ID (full username):\n")
							try :
								'''
								Part-2:TODO: Send private message
								'''
								s.sendall(rcv_id)
								break
							except socket.error:
								print 'rcv_id Send failed'
								sys.exit()
						elif message == str(2):
							bmsg = raw_input("Enter your broadcast message\n")
							try :
								'''
								Part-2:TODO: Send broadcast message
								'''
								s.sendall(bmsg)
								print 'Hear'
								#receiveThread(s)
								recv_bmsg = s.recvfrom(1024)
								print recv_bmsg
								break
							except socket.error:
								print 'Broadcast Message Send failed'
								sys.exit()
							
							#print 'Hear2'
							#recv_bmsg = s.recvfrom(1024)
							#print recv_bmsg
						elif message == str(3):
							gmsg = raw_input("Enter your group message\n")
							try :
								'''
								Part-2:TODO: Send group message
								'''
								s.sendall(gmsg)
							except socket.error:
								print 'Group Message Send failed'
								sys.exit()
							g_id = raw_input("Enter the Group ID (full group name):\n")
							try :
								'''
								Part-2:TODO: Send group message
								'''
								s.sendall(g_id)
								#break
							except socket.error:
								print 'g_id Send failed'
								sys.exit()
					except socket.error:
						print 'Message Send failed'
						sys.exit() 
			elif message == str(3):
				#start_new_thread(receiveThread, (s,))
				print 'Changing password\n'
				s.sendall(message)
				old_pass = getpass.getpass("Please enter old password:\n", stream = None)
				while(old_pass != password):
					print "Incorrect password\n"
					old_pass = getpass.getpass("Please enter old password:\n", stream = None)
				new_pass = getpass.getpass("Please enter new password:\n", stream = None)
				#print("Old password: " + old_pass)
				#print("New password: " + new_pass)
				s.sendall(new_pass)
				#password = s.recv(1024)
				password = new_pass
				#print password
			elif message == str(4):
				s.sendall(message)
				option = raw_input("Do you want to: \n 1. Join Group \n 2. List Groups \n 3. Quit Group: \n")
				#s.sendall(message)
				#for message_id, group_id, use it to get specific index
				s.sendall(option)
				if option == str(1):
					group = raw_input("Enter the Group you want to join: ")
					try :
						'''
						Part-2:TODO: Join a particular group
						'''
						s.sendall(group)
					except socket.error:
						print 'group info sent failed'
						sys.exit()
				elif option == str(2):
					print 'Press ctrl-c to close connection\n\n'
					print 'All groups listed below: \n'
					receiveThread(s)
					#print 'Press ctrl-c to close connection\n'
				elif option == str(3):
					group = raw_input("Enter the Group you want to quit: ")
					try :
						'''
						Part-2:TODO: Quit a particular group
						'''
						s.sendall(group)
					except socket.error:
						print 'group info sent failed'
						sys.exit()
				else:
					print 'Option not valid'		
			elif message == str(5):
				while not os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno()):
					pass
				s.sendall(message)
				option = raw_input("Do you want to: \n 1. View all offline messages \n 2. View only from a particular Group\n")
				s.sendall(option)
				if option == str(1):					
					try :
						'''
						Part-2:TODO: View all offline (private) messages
						'''
						print 'Press ctrl-c to close connection\n\n'
						print 'Showing all unread private messages\n'
						receiveThread(s)
						
					except socket.error:
						print 'msg Send failed'
						sys.exit()
				elif option == str(2):
					group = raw_input("Enter the group you want to view the messages from: ")
					try :
						'''
						Part-2:TODO: View only from a particular group
						'''
						print 'Press ctrl-c to close connection\n\n'
						print 'Showing all group messages\n'
						receiveThread(s)
					except socket.error:
						print 'group Send failed'
						sys.exit()
				else:
					print 'Option not valid'
			elif message == str(6):
                                s.sendall(message)
				print 'Getting message from server\n'
				receiveThread(s)
				print 'Done\n'
			else:
				error = s.recv(1024)
				print error
		except socket.error:
			print 'Send failed'
			sys.exit()

		print '\n'
else:
	print 'Invalid username or passwword'

s.close()S
