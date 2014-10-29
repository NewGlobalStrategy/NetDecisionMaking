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
# Russ also blogs occasionally to pass the time at proudofyourplanent.blogspot.com
# His general thinking on why this project is very important is availalbe at
# http://www.scribd.com/doc/98216626/New-Global-Strategy

from gluon import *
from textwrap import fill


def userdisplay(userid):
    """This should take a user id and return the corresponding
       value to display depending on the users privacy setting"""
    usertext = userid
    return usertext


def scopetext(scopeid, continent, country, subdivision):
    request = current.request
    if not request.env.web2py_runtime_gae:
        db = DAL('sqlite://storage.sqlite')
    else:
        db = DAL('google:datastore')

    scope = db(db.scope.id == scopeid).select(db.scope.description).first().description
    if scope == 'Global':
        activetext = 'Global'
    elif scope == 'Continental':
        activetext = db(db.continent.id == continent).select(
            db.continent.continent_name).first().continent_name
    elif scope == 'National':
        activetext = db(db.country.id == country).select(
            db.country.country_name).first().country_name
    else:
        activetext = db(db.subdivision.id == subdivision).select(
            db.subdivision.subdiv_name).first().subdiv_name

    return activetext


#prev maxlen was 700
def truncquest(questiontext, maxlen=600, wrap=0):
    #aim to do wordwrapping and possibly stripping and checking as
    #part of this function for jointjs now
    if len(questiontext) < maxlen:
        txt = MARKMIN(questiontext)
    else:
        txt = MARKMIN(questiontext[0:maxlen] + '...')
    return txt


def getwraptext(textstring, answer, textwidth, maxlength=230):
    if len(textstring) < maxlength:
        txt = textstring
    else:
        txt = textstring[0:maxlength] + '...'
    if answer:
        txt = txt + '\n' + 'A:' + answer
    qtexttemp = fill(txt, textwidth)
    lqtext = qtexttemp.split('\n')
    qtext = ''
    for y in lqtext:
        qtext += y
        qtext += r'\n'

    #qtext = textstring[:20] + r'\n' + textstring[21:40]
    qtext = qtext[:-2]
    return (qtext)




