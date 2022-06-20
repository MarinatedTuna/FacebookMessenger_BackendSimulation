import socket
import sys
from thread import *
import time

'''
Function Definition
'''
def tupleToString(t):
	s=""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
HOST = ''	# Symbolic name meaning all available interfaces
PORT = 9487	# Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

'''
Bind socket to local host and port
'''
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket bind complete'

'''
Start listening on socket
'''
s.listen(10)
print 'Socket now listening'

'''
Define variables:
username && passwd
smessage queue for each user
'''

username = ["Alpha", "Bravo", "Charlie"]
password = ["moab", "bfb", "zomg"]

clients = []
# TODO: Part-1 : create a var to store username && password. NOTE: A set of username/password pairs are hardcoded here. 
# e.g. userpass = [......]

userpass = [["Alpha", "moab"], ["Bravo", "bfb"], ["Charlie", "zomg"]]
usergroup = [] #make pair
messages = [] #private messages
group_messages = [] #group messages
broadcast_message = ""
message_only = []
count = 0
groups = ("genius", "voltage", "pixelberry")

#pair for username and message in messages

'''
Function for handling connections. This will be used to create threads
'''
def clientThread(conn):
	global clients
	global count
	# Tips: Sending message to connected client
	conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	rcv_msg = conn.recv(1024) #username
	rcv_pass = conn.recv(1024) #password
	rcv_userpass = [rcv_msg, rcv_pass]
	rcv_msg = stringToTuple(rcv_msg)
	rcv_pass = stringToTuple(rcv_pass)

	# print rcv_userpass
	# print userpass[0]

	if rcv_userpass in userpass:
		user = userpass.index(rcv_userpass)
                #print 'here'		

		'''
		Part-2:TODO:
		After user logs in, check the unread message for this user.
		Return the number of unread messages to this user.
		'''
		
		count = 0

		#print rcv_msg, message_only
		for a, b in messages:
			for c in rcv_msg:
				#print 'debug time\n'
				#print a
				#print c
				if a == c:
					item = '[\'' + a + '\']' + ' '  + '[\'' + b + '\']'
					#print item
					count = count + 1

		#print broadcast_message
		#conn.sendall(broadcast_message)
		#broadcast_message = ""
		
		#count = count + 1

		#print rcv_msg, message_only
		#print messages

		print ('You have ' + str(count) + ' unread messages\n')
		#conn.sendall(str(count))

		try :
			conn.sendall('valid')
		except socket.error:
			print 'Send failed'
			sys.exit()
		
		conn.sendall(str(count))
	
		# Tips: Infinite loop so that function do not terminate and thread do not end.
		while True:
			try :
				option = conn.recv(1024)
			except:
				break
			if option == str(1):
				print 'user logout'
				# TODO: Part-1: Add the logout processing here	
				conn.close()
				clients.remove(conn)	
				#break
			elif option == str(2):
				print 'Post a message'
				message = conn.recv(1024)
				if message == str(1):
					#print 'Here1'
					'''
					Part-2:TODO: Send private message
					'''
					pmsg = conn.recv(1024)
					#print pmsg
					receiver_id = conn.recv(1024)
					#print receiver_id
					new_pm = [receiver_id, pmsg]
				        messages.append(new_pm)	
					#print messages
					message_only.append(pmsg)
					#print message_only
				if message == str(2):
					#print 'Here2'
					'''
					Part-2:TODO: Send broadcast message
					'''
					bmsg = conn.recv(1024)
					#conn.sendall(bmsg)
					#print bmsg
					broadcast_message = bmsg
					#print clients
				if message == str(3):
					#print 'Here3'
					gmsg = conn.recv(1024)
					#print gmsg
					g_id = conn.recv(1024)
					#print g_id
					new_gm = [g_id, gmsg]
					group_messages.append(new_gm)
					#print usergroup
					#print group_messages
					'''
					Part-2:TODO: Send group message
					'''
			elif option == str(3):
				print 'user change password'
				new_pass = conn.recv(1024)
				#print old_pass
				rcv_msg = tupleToString(rcv_msg)
				change_pass = [rcv_msg, new_pass]
				#print change_pass
				if rcv_userpass in userpass:
					userpass.append(change_pass)
					userpass.remove(rcv_userpass)
					#print change_pass
					conn.sendall(new_pass)
			elif option == str(4):
				print 'Group options'
				choice = conn.recv(1024)
				if choice == str(1):
					#print 'Here_1'
					group_join = conn.recv(1024)
					#print group_join
					if group_join in groups:
						add_to_group = [group_join, rcv_msg]
						#print add_to_group
						usergroup.append(add_to_group)
						#print usergroup
						print 'Successfully joined the group!'
					else:
						print 'Group does not exist!\n'
				elif choice == str(2):
					#print 'Here_2'
					print 'Sending group info to client...'
					send_groups = tupleToString(groups)
					conn.send(send_groups)
					#print send_groups
				elif choice == str(3):
					#print 'Here_3'
					group_to_leave = conn.recv(1024)
					#print group_to_leave
					group_leave_process = [group_to_leave, rcv_msg]
					#print group_leave_process
					if group_leave_process in usergroup:
						usergroup.remove(group_leave_process)
						print 'Successfully left the group'
					else:
						print 'Either the group does not exist or the user is already not in the group'
				'''
				Part-2:TODO: Join/Quit group
				'''
			elif option == str(5):
				'''
				Part-2:TODO: Read offline message
				'''
				choice = conn.recv(1024)
				if choice == str(1):
					print 'Sending private message\n'
					#count = 0
					#send_offline_message = tupleToString(message_only)
					#print send_offline_message
					#conn.sendall(send_offline_message)
					#remove_unread = [rcv_msg, message_only]
					#print remove_unread
					#print messages
					#messages.remove(remove_unread)
					#rcv_msg only 1 parameter
					#print 'rcv_msg below\n'
					#print rcv_msg
					#['']
					#print 'Before sending messages'
					#print messages
					#print 'Tuple to string messages'
					#messages_tuple = tupleToString(messages)
					#print messages_tuple
					#conn.sendall(messages_tuple)

					to_send = []
					
					#sending message
					
					for a, b in messages:
						for c in rcv_msg:
							if a == c:
								to_send.append(b)

					#print 'to_send:'
					#print to_send		
					to_send_string = tupleToString(to_send)
					#print to_send_string
					conn.sendall(to_send_string)

					#removing sent message

					for a, b in messages:
						#print 1
						for c in rcv_msg:
							#print 2
							if a == c:
								#print 3
								d = [a, b]
								messages.remove(d)
							#messages.remove(d)

					for a, b in messages:
						for c in rcv_msg:
							if a == c:
								d = [a, b]
								messages.remove(d)

					#print 'cnt: ' 
					#print cnt
				elif choice == str(2):
					print 'Sending group message\n'
					#send_offline_message = tupleToString(message_only)
					#print send_offline_message
					#conn.sendall(send_offline_message)
					print usergroup
					print group_messages
					send_group_msg = []
					for a, b in group_messages: #maybe add 3rd pair
						for c, d in usergroup:
							if a == d:
								send_group_msg.append(b)
					send_group_msg_string = tupleToString(send_group_msg)
					print send_group_msg_string
					conn.sendall(send_group_msg_string)
			elif option == str(6):
				print 'Okay we are in option 6\n'
				#sample = "Sending this"
				try:
					conn.sendall('Sending this')
				except socket.error:
					print 'Could not send'
					sys.exit()
			else:
				try :
					conn.sendall('Option not valid')
				except socket.error:
					print 'option not valid Send failed'
					conn.close()
					clients.remove(conn)			

	else:
		try :
			conn.sendall('nalid')
		except socket.error:
			print 'nalid Send failed'
	print 'Logged out'
	conn.close()
	if conn in clients:
		clients.remove(conn)

def receiveClients(s):
	global clients
	while 1:
		# Tips: Wait to accept a new connection (client) - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		clients.append(conn)
		# Tips: start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientThread ,(conn,))

start_new_thread(receiveClients ,(s,))

'''
main thread of the server
print out the stats
'''
while 1:
	message = raw_input()
	if message == 'messagecount':
		print 'Since the server was opened ' + str(count) + ' messages have been sent'
	elif message == 'usercount':
		print 'There are ' + str(len(clients)) + ' current users connected'
	elif message == 'storedcount':
		print 'There are ' + str(sum(len(m) for m in messages)) + ' unread messages by users'
	elif message == 'newuser':
		user = raw_input('User:\n')
		password = raw_input('Password:')
		userpass.append([user, password])
		messages.append([])
		subscriptions.append([])
		print 'User created'
	elif message == 'listgroup':
		print 'Listing all available groups...\n'
		print groups
		'''
		Part-2:TODO: Implement the functionality to list all the available groups
		'''
s.close()

