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


# This controller provides details about network decision making
# access to the FAQ and allows generation of a general message
# on what we are looking to achieve
# The Press Release Note for the latest version is also now included
# and some basic capabilities to download actions have also been added


def index():
    return dict(message="all done in the view")

def privacy():
    return dict(message="all done in the view")

def faq():
    return dict(message="all done in the view")


def pr():
    return dict(message="all done in the view")


def enhance():
    return dict(message="all done in the view")


def stdmsg():
    messagerow = db(db.message.msgtype == 'std').select(
        db.message.message_text).first()
    if messagerow is None:
        message = 'You have not setup any std messages yet'
    else:
        message = messagerow.message_text

    return dict(message=message)


def download():
    downloads = db().select(db.download.ALL, orderby=db.download.title, cache=(cache.ram, 1200), cacheable=True)
    return dict(downloads=downloads)


def getfile():
    return response.download(request, db)
