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
# For details on the web framework used for this development
#
# Developed by Russ King (newglobalstrategy@gmail.com
# Russ also blogs occasionally to pass the time at: 
# http://proudofyourplanent.blogspot.com
# His general thinking on why this project is very important is available at
# http://www.scribd.com/doc/98216626/New-Global-Strategy
# With thanks to Guido, Massimo and many other that make this sort of thing
# much easier than it used to be
# This controller has 3 functions:
# my_questions for reviewing progress on questions you have asked
# my_answers for reviewing your answers
# resovled for reviewing resolved questio

"""This controller has 3 functiosns:
new_location - for creating locations
my_locations - for creating, updating and deleting details of your locations
locations for seeing a list of locations that are setup
viewlocation - for reviewing details of a single location and links to the events that
are planned to take place there
"""


@auth.requires_login()
def new_location():
    #This allows creation of a location

    fields = ['location_name', 'description', 'addrurl', 'address1', 'address2', 'address3', 'address4', 'addrcode',
              'continent', 'country', 'subdivision', 'shared']

    form = SQLFORM(db.location, fields=fields, formstyle='table3cols')

    if form.validate():
        #form.vars.auth_userid=auth.user.id

        form.vars.id = db.location.insert(**dict(form.vars))
        #response.flash = 'form accepted'
        session.lastevent = form.vars.id
        #redirect(URL('accept_question',args=[form.vars.qtype])) 
        redirect(URL('accept_location', args=[form.vars.id]))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    return dict(form=form)


def accept_location():
    response.flash = "Location Created"
    eventid = 0
    if len(request.args) > 0:
        eventid = request.args(0)
    else:
        redirect(URL('new_location'))

    return dict(eventid=eventid)


@auth.requires_login()
def my_locations():
    #thinking is users shouldn't have that many of these so this should be easy - will need to be a button
    # to view events at this location and that this shold list all locations
    query1 = db.location.auth_userid == auth.user.id
    myfilter = dict(location=query1)
    grid = SQLFORM.smartgrid(db.location, constraints=myfilter, searchable=False)
    return locals()


def locationqry():
    #are using this for locations
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)

    locations = db(db.location.auth_userid == auth.user.id).select(db.location.id,
                                                                   db.location.location_name, db.location.description,
                                                                   db.location.address1, db.location.address2,
                                                                   db.location.address3, db.location.address4,
                                                                   db.location.addrcode,
                                                                   db.location.continent, db.location.country,
                                                                   db.location.subdivision,
                                                                   db.location.shared, db.location.addrurl,
                                                                   db.location.auth_userid,
                                                                   orderby=[~db.location.createdate], limitby=limitby)

    return dict(locations=locations, page=page, items_per_page=items_per_page)

def index():
    #are using this for locations
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)

    locations = db(db.location.id>0).select(orderby=[~db.location.createdate], limitby=limitby)

    return dict(locations=locations, page=page, items_per_page=items_per_page)

def viewlocation():
    #This should list location details with an event load for upcoming and future events at this location
    query1 = db.location.auth_userid == auth.user.id
    return
