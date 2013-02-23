#! /usr/bin/python
import sys
import subprocess
import smtplib
import os
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

for backup in conf['backups']:
	command = 'rsync -avz -e "ssh -p %i" %s@%s:%s %s' % (conf['port'],
	                                                     conf['user'],
														 conf['host'],
														 backup['src'],
														 backup['dst'])
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

msg = MIMEText(output)

msg['Subject'] = 'Backup: %s' % (subject)
msg['From'] = conf['email_source']

s = smtplib.SMTP(conf['email_server'])
s.starttls()
s.login(conf['email'],conf['password'])
s.sendmail(conf['email_source'],[conf['email_out']],msg.as_string())
s.quit()
