#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/20 16:02
# @Author  : Mad_frog
# @File    : email.py

def sentmail(receiver,context):
    import smtplib
    from email.mime.text import MIMEText

    sender = 'projectblog'
    subject = '密码找回邮件'
    smtpserver = 'smtp.126.com'
    username = 'projectblog'
    password = 'qishihenjiandan'

    msg = MIMEText('<html><h1>%s</h1></html>'%context, 'html', 'utf-8')

    msg['Subject'] = subject

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username,password)
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.close()

if __name__ == '__main__':
    sentmail('155317720@qq.com','hello')