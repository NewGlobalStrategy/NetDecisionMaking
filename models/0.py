# - Coding UTF8 -
#
# Networked Decision Making
# Site: http://code.google.com/p/global-decision-making-system/
#
# License Code: GPL, General Public License v. 2.0
# License Content: Creative Commons Attribution 3.0
#
# Also visit: www.web2py.com
#             or Groups: http://groups.google.com/group/web2py 
# 	For details on the web framework used for this development
#
# Developed by Russ King (newglobalstrategy@gmail.com
# Russ also blogs occasionally at proudofyourplanent.blogspot.com
# His general thinking on why this project is very important is available at
# http://www.scribd.com/doc/98216626/New-Global-Strategy
#
# This file contains settings for auth policy which are need before setup
# of rest of configuration so staying here for now
#
#########################################################################

from gluon.storage import Storage
settings = Storage()

#Settings for user logon - lets just uncomment as needed for now - not clear if there is much scope to
#allow changes and python social auth will hopefully be added I don't think dual login worked with google but
#lets setup again and see

#Plan for this for now is that netdecisionmaking will use web2py and Janrain while
#globaldecisionmaking will use google - for some reason Janrain doesn't seem
#to come up with google as a login and google login does not support dual methods
#reason for which has not been investigated

#settings.logon_methods = 'web2py'
#settings.logon_methods = 'google'
#settings.logon_methods = 'janrain'
settings.logon_methods = 'web2pyandjanrain'

settings.verification = False
settings.approval = False
