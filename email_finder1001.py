#Copyright (c) 2017 Ahmed Alsharif
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import socket
import smtplib
import dns.resolver
import argparse

#b=0
parser = argparse.ArgumentParser()
parser.add_argument("MODE", type=int, help='Searching mode, curernly only 1 works')
parser.add_argument("DOMAIN", help='The domain of the email has to be like example.com')
parser.add_argument("VORNAME", help="First name, or last. it doesn't really matter")
parser.add_argument("NACHNAME", help="Last name, or first. it doesn't matter really")
parser.add_argument("--verbose", "-v", dest="VERBOSE", action='store_true', help="Dumps info")

args = parser.parse_args()

first_name = args.VORNAME
last_name = args.NACHNAME
domain_name= args.DOMAIN
verbose = args.VERBOSE
	


host = socket.gethostname()
server = smtplib.SMTP()
server.set_debuglevel(0)

def get_webmail(domain):
	records = dns.resolver.query(domain, 'MX')
	webmail_address = records[0].exchange
	webmail_address = str(webmail_address)
	if verbose:
		print("webmail_address: "+webmail_address)
	return webmail_address

webmail_name = get_webmail(domain_name)

def verify_email(email, webmail):

	server.connect(webmail)
	server.helo(host)
	server.mail('meow@kittykitty.com')
	code, message = server.rcpt(email)
	server.quit()

	if code == 250:
		if not verbose:
			print('\n************************************\nFound one: '+email+'\n************************************\n')
		return True
	else:
		if not verbose:
			print(email+" NOPE!")
		return False

def verify_server():
	emaili = "jksdjf90jfls9f@"+domain_name
	if verify_email(emaili, webmail_name):
		if verbose:
			print("verify_server: false")
		return False
	else:
		if verbose:
			print("verify_server: true")
		return True

def spit_def_combos(counter, operator, first_name, last_name):
	dot = '.'
	dash= '-'
	underscore = '_'
	
	if operator == 0:
		operator = dot
	elif operator == 1:
		operator = dash
	elif operator == 2:
		operator = underscore


	if counter == 0:
		return first_name
	elif counter == 1:
		return last_name
	if counter == 2:
		return first_name+last_name
	elif counter == 3:
		return last_name+first_name
	elif counter == 4:
		return first_name[:1]+last_name
	elif counter == 5:
		return last_name[:1]+first_name
	elif counter == 6:
		return first_name+last_name[:1]
	elif counter == 7:
		return last_name+first_name[:1]
	elif counter == 8:
		return first_name+operator+last_name
	elif counter == 9:
		return last_name+operator+first_name
	elif counter == 10:
		return first_name+operator+last_name[:1]
	elif counter == 11:
		return last_name+operator+first_name[:1]
	elif counter == 12:
		return first_name[:1]+operator+last_name
	elif counter == 13:
		return last_name[:1]+operator+first_name

if args.MODE==1 and verify_server():

	i=0
	k=0
	while True:
		emailz = spit_def_combos(i, k, first_name, last_name)+'@'+domain_name
		#print emailz
		if verify_email(emailz, webmail_name):
			#break
			if i<13:
				i+=1
			else:
				i=6
				if k < 2:
					k+=1
				else:
					break
		elif i>=13:
			i=6
			if k < 2:
				k+=1
			else:
				break
		else:
			i+=1
else:
	print("Server prevents checking or MODE not set as 1")
