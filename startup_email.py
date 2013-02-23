#! /usr/bin/python

import smtplib
import time
import socket
import sys
import os
from email.mime.text import MIMEText

try:
	conf = eval(open(sys.argv[1],'rb').read())
except:
	print 'config file error'
	exit()
	
if not conf['password']:
	conf['password'] = open(os.path.join(os.path.dirname(sys.argv[1]),'%s.password' % conf['email']),'rb').read()

name = socket.gethostname()
time = time.strftime('%Y-%m-%d %H:%M',time.localtime())
output = '%s has started at %s.' % (name,time)
msg = MIMEText(output)

msg['Subject'] = '%s Remote: Started' % (name)
msg['From'] = conf['email_source']

s = smtplib.SMTP(conf['email_server'])
s.starttls()
s.login(conf['email'],conf['password'])
s.sendmail(conf['email_source'],[conf['email_out']],msg.as_string())
s.quit()

#Add to rc.d
# sudo ln -fs /home/pi/scripts/startup_email.py /etc/init.d/startup_email
# sudo update-rc.d startup_email defaults
