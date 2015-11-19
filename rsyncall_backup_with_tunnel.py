#! /usr/bin/python
import sys
import subprocess
import smtplib
import os
import time
from email.mime.text import MIMEText


try:
	conf = eval(open(sys.argv[1],'rb').read())
except:
	print 'config file error'
	exit()
	
output = ''
subject = ''
if not conf['password']:
	conf['password'] = open(os.path.join(os.path.dirname(sys.argv[1]),'%s.password' % conf['email']),'rb').read()

tunnel_command = 'ssh -N -L %s:%s:%s %s@%s -p %s' % (conf['local_port'],conf['tunnel_addr'],conf['tunnel_port'],conf['bridge_user'],conf['bridge_addr'],conf['bridge_port'])
print tunnel_command
tunnel = subprocess.Popen(tunnel_command,shell=True)
time.sleep(10) 
for backup in conf['backups']:
	command = 'rsync -rtOvuh -e "ssh -p %s" %s@%s:%s %s' % (conf['local_port'],conf['tunnel_user'],'localhost',
														 backup['src'],
														 backup['dst'])
	print command
	output += 'Running: ' + command + '\n'
	proc = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = proc.communicate()
	output += '%s\n%s\n' % (stdout,stderr)
	if len(stderr) > 0:
		output += 'Fail' + '\n\n'
		subject += 'Fail:'
	else:
		output += 'Complete' + '\n\n'
		subject += 'Pass:'

tunnel.terminate()

msg = MIMEText(output)

msg['Subject'] = 'Backup: %s' % (subject)
msg['From'] = conf['email_source']

s = smtplib.SMTP(conf['email_server'])
s.starttls()
s.login(conf['email'],conf['password'])
s.sendmail(conf['email_source'],[conf['email_out']],msg.as_string())
s.quit()
