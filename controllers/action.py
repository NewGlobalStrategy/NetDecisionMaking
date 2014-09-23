# - Coding UTF8 -
#
# Networked Decision Making
# Site: http://code.google.com/p/global-decision-making-system/
#
# License Code: GPL, General Public License v. 2.0
# License Content: Creative Commons Attribution 3.0
#
# Also visit: www.web2py.com
# or Groups: http://groups.google.com/group/web2py
# 	For details on the web framework used for this development
#
# Developed by Russ King (newglobalstrategy@gmail.com
# Russ also blogs occasionally to pass the time at: 
# http://proudofyourplanent.blogspot.com
# His general thinking on why this project is very important is available at
# http://www.scribd.com/doc/98216626/New-Global-Strategy
# With thanks to Guido, Massimo and many other that make this sort of thing
# much easier than it used to be


# Now only 1 function here which allows sending of messages to yourself to then
# forward on to those you see fit
# sendmsg - actually sends via ajax


def sendmsg():
    #Called via ajax to send messages to users for forwarding on as they see fit
    if auth.user is None:
        responsetext = 'You must be logged in to create messages'
    else:
        messagetxt = db(db.message.msgtype == 'std').select(
            db.message.message_text).first().message_text

        email = [auth.user.email]

        link = URL('default', 'index', scheme=True, host=True)
        #link = URL('viewquest','index', args=questid, scheme=True, host=True)
        footnote = 'More details on the overall approach and the identified actions can be found at: ' + link
        #messagetxt = '<html>' + messagetxt + ' ' + footnote + '</html>'   
        messagetxt = messagetxt + ' ' + footnote
        mail.send(to=email,
                  subject='Networked Decision Making Action Request',
                  message=messagetxt)

        responsetext = 'Your message has been sent to you to foward on.'

    return responsetext
