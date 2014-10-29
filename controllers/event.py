# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): 
#   http://code.google.com/p/global-decision-making-system/
#   http://github.com/NewGlobalStrategy/NetDecisionMaking
#
# Demo Sites (Google App Engine)
#   http://netdecisionmaking.appspot.com
#   http://globaldecisionmaking.appspot.com
#
# License Code: MIT
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


#paper.on('cell:pointerdown', 
#    function(cellView, evt, x, y) { 
#        alert('cell view ' + cellView.model.id + ' was clicked'); 
#    }
#);


"""
This controller has 6 functions:

new_event - for creating events
accept_event - when event submitted
my_events - for creating, updating and deleting events
index - for a list of events
eventquery - a loadable query for events - typicaly split by upcoming, future and past
eventbar - a single column list of events for the sidebar
viewevent - the main detailed page on events which will mainly be accessed from event or the sidebars
and load functions
link - Ajax for linking and unlinking questions from events
move - Ajax for moving event questions around 
"""

import datetime
from netx2py import getpositions
from ndsfunctions import getwraptext
from jointjs2py import colourcode, textcolour


@auth.requires_login()
def new_event():
    #This allows creation of an event

    fields = ['event_name', 'locationid', 'startdatetime', 'enddatetime',
              'description', 'shared']
    form = SQLFORM(db.event, fields=fields, formstyle='table3cols')

    form.vars.locationid = db(db.location.location_name =='Unspecified').select(db.location.id, cache=(cache.ram,3600), cacheable=True).first().id
    if form.validate():
        form.vars.id = db.event.insert(**dict(form.vars))
        #response.flash = 'form accepted'
        session.event_name = form.vars.id
        redirect(URL('accept_event', args=[form.vars.id]))
        #redirect(URL('accept_question',args=[form.vars.qtype])) 
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    return dict(form=form)


def accept_event():
    response.flash = "Event Created"
    eventid = 0
    if len(request.args) > 0:
        eventid = request.args(0)
    else:
        redirect(URL('new_event'))

    return dict(eventid=eventid)


@auth.requires_login()
def my_events():
    query1 = db.event.owner == auth.user.id
    myfilter = dict(event=query1)
    grid = SQLFORM.smartgrid(db.event, formstyle=SQLFORM.formstyles.bootstrap3, constraints=myfilter, searchable=False)
    return locals()


def index():
    if len(request.args):
        scope = request.args[0]
    else:
        scope = 'Unspecified'

    #if scope == 'My':
    #    query = (db.event.auth_userid == auth.user.id)
    #else:
    query = (db.event.id > 0)

    datenow = datetime.datetime.utcnow()
    #start_date = end_date - datetime.timedelta(days=8)
    #difference_in_days = abs((end_date - start_date).days)

    #print difference_in_days
    #this fails on gae as too many inequalities
    if len(request.args) < 2 or request.args[1] == 'Upcoming':
        #query = query & (db.event.startdatetime > datenow) & ((db.event.startdatetime - datenow) < 8.0)
        query = (db.event.startdatetime > datenow)
    elif request.args[1] == 'Future':
        #query = query & (db.event.startdatetime > datenow) & ((db.event.startdatetime - datenow) >= 8.0)
        query = (db.event.startdatetime > datenow)

    if scope == 'My':
        query = (db.event.auth_userid == auth.user.id)

    events = db(query).select(db.event.id, db.event.event_name, db.event.description,
                              db.event.startdatetime, db.event.enddatetime, db.event.locationid, db.event.owner,
                              orderby=[db.event.startdatetime], cache=(cache.ram, 1200), cacheable=True)

    return dict(events=events)


def eventqry():
    if len(request.args):
        scope = request.args[0]
    else:
        scope = 'Unspecified'

    datenow = datetime.datetime.utcnow()

    if len(request.args) < 2 or request.args[1] == 'Upcoming':
        #query = query & (db.event.startdatetime > datenow) & ((db.event.startdatetime - datenow) < 8.0)
        query = (db.event.startdatetime > datenow)
    elif request.args[1] == 'Future':
        #query = query & (db.event.startdatetime > datenow) & ((db.event.startdatetime - datenow) >= 8.0)
        query = (db.event.startdatetime > datenow)

    if scope == 'My':
        query = (db.event.auth_userid == auth.user.id)

    orderby = [db.event.startdatetime]
    events = db(query).select(db.event.id, db.event.event_name, db.event.description,
                              db.event.startdatetime, db.event.enddatetime, db.event.locationid, db.event.owner,
                              orderby=orderby, cache=(cache.ram, 1200), cacheable=True)

    return dict(events=events)


def eventbar():
    datenow = datetime.datetime.utcnow()
    #line below fails on gae for some reason and limitby may be fine instead to not get too many
    #query = (db.event.startdatetime > datenow) & ((db.event.startdatetime - datenow) < 8.0)
    query = (db.event.startdatetime > datenow)
    orderby = [db.event.startdatetime]
    events = db(query).select(db.event.id, db.event.event_name, db.event.description,
                              db.event.startdatetime, db.event.enddatetime, db.event.locationid, db.event.owner,
                              orderby=orderby, cache=(cache.ram, 1200), cacheable=True)

    return dict(events=events)


def viewevent():
    #This is a non-network view of events - think this will be removed
    #just use vieweventmap instead
    eventid = 0
    if len(request.args):
        eventid = int(request.args[0])
    else:
        redirect(URL('index'))

    eventrow = db(db.event.id == eventid).select(db.event.id, db.event.event_name, db.event.description,
                                                 db.event.startdatetime,
                                                 db.event.enddatetime, db.event.locationid,
                                                 db.event.owner, db.event.shared, cache=(cache.ram, 1200),
                                                 cacheable=True).first()

    session.eventid = eventid
    return dict(eventrow=eventrow, eventid=eventid)


@auth.requires_login()
def eventaddquests():
    #Think this is a non-network view of events
    page = 0
    eventid = 0
    if len(request.args):
        eventid = int(request.args[0])
        if len(request.args) > 1:
            page = int(request.args[1])
    else:
        redirect(URL('index'))

    eventrow = db(db.event.id == eventid).select(db.event.id, db.event.event_name, db.event.description,
                                                 db.event.startdatetime,
                                                 db.event.enddatetime, db.event.locationid,
                                                 db.event.owner, db.event.shared).first()

    session.event_name = eventrow.event_name

    unspecevent = db(db.event.event_name == 'Unspecified').select(db.event.id).first().id

    #Plan then would be to list some sort of items not in the event - think this will be a full view on a page
    #for now as will be easier to manage the view and the enquiry types probably also want a remove questions from 
    #event option - both will be an ajax call I think for now with return to a div

    query = (db.question.eventid == eventid) & (db.question.qtype == 'quest')
    sortby = ~db.question.createdate
    items_per_page = 20

    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)

    quests = db(query).select(
        db.question.id, db.question.status, db.question.questiontext, db.question.duedate,
        db.question.responsible, db.question.priority, db.question.achieved, db.question.level,
        db.question.correctanstext, db.question.numagree, db.question.numdisagree,
        db.question.activescope, db.question.category, db.question.continent,
        db.question.country, db.question.subdivision, db.question.scopetext, db.question.priority,

        orderby=sortby, limitby=limitby)

    query = (db.question.eventid == eventid) & (db.question.qtype == 'action')

    actions = db(query).select(
        db.question.id, db.question.status, db.question.questiontext, db.question.duedate,
        db.question.responsible, db.question.priority, db.question.achieved, db.question.level,
        db.question.correctanstext, db.question.numagree, db.question.numdisagree,
        db.question.activescope, db.question.category, db.question.continent,
        db.question.country, db.question.subdivision, db.question.scopetext,
        orderby=sortby, limitby=limitby)

    query = (db.question.eventid == unspecevent) & (db.question.qtype == 'quest')
    othquests = db(query).select(

        db.question.id, db.question.status, db.question.questiontext, db.question.duedate,
        db.question.responsible, db.question.priority, db.question.achieved, db.question.level,
        db.question.correctanstext, db.question.numagree, db.question.numdisagree,
        db.question.activescope, db.question.category, db.question.continent,
        db.question.country, db.question.subdivision, db.question.scopetext, db.question.priority,
        orderby=sortby, limitby=limitby)

    query = (db.question.eventid == unspecevent) & (db.question.qtype == 'action')

    othactions = db(query).select(
        db.question.id, db.question.status, db.question.questiontext, db.question.duedate,
        db.question.responsible, db.question.priority, db.question.achieved, db.question.level,
        db.question.correctanstext, db.question.numagree, db.question.numdisagree,
        db.question.activescope, db.question.category, db.question.continent,
        db.question.country, db.question.subdivision, db.question.scopetext,
        orderby=sortby, limitby=limitby)

    return dict(eventrow=eventrow, eventid=eventid, quests=quests, actions=actions, othquests=othquests,
                othactions=othactions,
                page=page, items_per_page=items_per_page)


def vieweventmap():
    #This now has a load option and works fine when events are setup - however the redirect is a problem if no events
    #as then loads with another layout html and thing fails badly possibly better to change to just return message if
    #no selection for now

    grwidth = 800
    grheight = 600
    FIXWIDTH = 800
    FIXHEIGHT = 600

    resultstring = ''
    gotevent=True

    if len(request.args) and int(request.args[0]) > 0:
        eventid = int(request.args[0])
    else:
        datenow = datetime.datetime.utcnow()
        #query = (db.event.startdatetime > datenow) & (db.event.event_name != 'Unspecified') fails on gae 2 inequalities

        query = (db.event.startdatetime > datenow)
        events = db(query).select(db.event.id, orderby=[db.event.startdatetime]).first()
        if events:
            eventid = events.id
        else:
            response.view = 'noevent.load'
            return dict(resultstring='No Event')

    if len(request.args) > 2:
        grwidth = int(request.args[1])
        grheight = int(request.args[2])

    eventrow = db(db.event.id == eventid).select().first()

    eventmap = db(db.eventmap.eventid == eventid).select()

    query = db.question.eventid == eventid

    # quests=db(db.question.id.belongs([4,8,10])).select(db.question.id, db.question.questiontext,
    # db.question.correctanstext, db.question.status, db.question.level)
    quests = db(query).select(db.question.id, db.question.questiontext, db.question.correctanstext, db.question.status,
                              db.question.level, db.question.qtype, db.question.category, db.question.priority,
                              cache=(cache.ram, 120), cacheable=True)

    questlist = [x.id for x in quests]
    if not questlist:
            response.view = 'noevent.load'
            return dict(resultstring='No Event')

    parentlist = questlist
    childlist = questlist
    #removed for gae for now
    #intquery = (db.questlink.targetid.belongs(questlist)) & (db.questlink.status == 'Active') & (
    #db.questlink.sourceid.belongs(questlist))

    #this fails on gae as two inequalities
    #intlinks = db(intquery).select(db.questlink.id, db.questlink.sourceid, db.questlink.targetid,
    #                               db.questlink.createcount, db.questlink.deletecount)

    intquery = (db.questlink.status == 'Active') & (db.questlink.sourceid.belongs(questlist))

    intlinks = db(intquery).select(db.questlink.id, db.questlink.sourceid, db.questlink.targetid,
                                   db.questlink.createcount, db.questlink.deletecount,cache=(cache.ram, 120), cacheable=True)

    links = [x.sourceid for x in intlinks]

    if links:
        linklist = [(x.sourceid, x.targetid) for x in intlinks]
    else:
        linklist = []

    # idea is to put the event as a node at the top of the graph so may offset everything else by say
    # 200 and leave that space - however first question if it exists should be at a fixed position - but lets add that
    # later given query doesn't seem to work may be better to add the event as a node - however that causes some issues
    # as well let's remove the ports as well for now on this I think in the view and see how that goes
    # ok so now got the question but need to get the list of links as well to draw the graph -
    # same approach with a rows object
    # this whole first question piece doesn't appear to work lets revert to std for now and not really setting first
    # question either for now - spring weights might be more important in due course

    if not eventmap and quests:
            nodepositions = getpositions(questlist, linklist)
            #think we insert them into the eventmap here and then run the query and may need to re-run if get wrong
            #number because of gae
            for key in nodepositions:
                recid = db.eventmap.insert(eventid=eventid, questid=key, xpos=(nodepositions[key][0] * FIXWIDTH), ypos=(nodepositions[key][1] * FIXHEIGHT))
            #Make sure everything picked up
            eventmap = db(db.eventmap.eventid == eventid).select()

    #so could then emerge here always with an eventmap established (probably as a dictionary rather than node positions
    if eventmap is None:
        redirect(URL('index'))

    #thinking about doing a similar thing for parent child view - but not sure that's practical
    #insert from viewquest to go through - so this may be made into a separate routine

    questmap = {}
    qlink = {}
    keys = '['

    for x in quests:
        if x['qtype'] == 'action':
            width = 200
            height = 140
            wraplength = 30
        else:
            width = 160
            height = 200
            wraplength = 25
        qtext = getwraptext(x.questiontext, x.correctanstext, wraplength)
        rectcolour = colourcode(x.qtype, x.status, x.priority)
        colourtext = textcolour(x.qtype, x.status, x.priority)
        strobj = 'Nod' + str(x.id)
        #questmap[strobj] = [nodepositions[x.id][0] * grwidth, 200 + nodepositions[x.id][1] * grheight, qtext,
        #                    rectcolour, 12, 'lr', width, height]
        questmap[strobj] = [0, 0, qtext, rectcolour, 12, 'tb', width, height, colourtext]
        keys += strobj
        keys += ','

    if eventmap is not None:
        for row in eventmap:
            strobj = 'Nod' + str(row.questid)
            questmap[strobj][0] = row.xpos
            questmap[strobj][1] = row.ypos

    #if we have siblings and partners and layout is directionless then may need to look at joining to the best port
    #or locating the ports at the best places on the shape - most questions will only have one or two connections
    #so two ports may well be enough we just need to figure out where the ports should be and then link to the 
    #appropriate one think that means iterating through quests and links for each question but can set the 
    #think we should move back to the idea of an in and out port and then position them possibly by rotation
    #on the document - work in progress
    #thinking this graph will ultimately NOT use ports as this will be view only and would like html to work
    #think link can perhaps be same as std ones once graph created

    for x in intlinks:
        strlink = 'Lnk' + str(x.id)
        strsource = 'Nod' + str(x.sourceid)
        strtarget = 'Nod' + str(x.targetid)
        if questmap[strtarget][1] > questmap[strsource][1]:
            sourceport = 'b'
            targetport = 't'
        else:
            sourceport = 't'
            targetport = 'b'
        if x.createcount - x.deletecount > 1:
            dasharray = False
            linethickness = min(3 + x.createcount, 7)
        else:
            dasharray = True
            linethickness = 3

        qlink[strlink] = [strsource, strtarget, sourceport, targetport, dasharray, linethickness]
        keys += strlink
        keys += ','

    keys = keys[:-1] + ']'

    #This may now be a questmap - will need to come back to fixing the position and adding in the link to the event
    session.networklist = [x.id for x in quests]

    session.eventid = eventid
    return dict(eventrow=eventrow, quests=quests, links=links, resultstring=resultstring, eventmap=eventmap,
                questmap=questmap, keys=keys, qlink=qlink, eventid=eventid)


def link():
    # This allows linking questions to an event via ajax

    eventid = request.args[0]
    chquestid = request.args[1]
    action = request.args[2]
    eventmapexists = 'T'  # Change to request.args[3] presently
    fixedx = 600
    fixedy = 500

    if auth.user is None:
        responsetext = 'You must be logged in to record agreement or disagreement'
    else:
        #questrows = db(db.question.id == chquestid).select()
        #quest = questrows.first()
        quest = db(db.question.id == chquestid).select(db.question.id, db.question.eventid,
                                                       db.question.auth_userid).first()
        unspecevent = db(db.event.event_name == 'Unspecified').select(db.event.id, cache=(cache.ram, 3600),).first()

        #Think about where this is secured - should probably be here
        event = db(db.event.id == eventid).select(db.event.id, db.event.event_name, db.event.owner,
                                                  db.event.shared).first()

        if event.shared or (event.owner == auth.user.id) or (quest.auth_userid == auth.user.id):
            if action == 'unlink':
                db(db.question.id == chquestid).update(eventid=unspecevent.id)
                responsetext = 'Question unlinked'
            else:
                db(db.question.id == chquestid).update(eventid=eventid)
                responsetext = 'Question linked to event'
                #Then if there was an eventmap it should require to be linked to 
                #to the eventmap but if not it shouldn't - this may need to be an arg
                if eventmapexists == 'T':
                    db.eventmap.insert(eventid=eventid, questid=chquestid, xpos=fixedx, ypos=fixedy)
        else:
            responsetext = 'Not allowed - This event and you are not the owner'
                    
    return responsetext


def move():
    # This will allow moving the position of questions on an eventmap - but not on a general map at present
    # as no obvious way to save them - however think we will comment out the code if not authorised

    eventid = request.args[0]
    chquestid = request.args[1]
    newxpos = request.args[2]
    newypos = request.args[3]
    questid = int(chquestid[3:])

    if auth.user is None:
        responsetext = 'You must be logged in to save movements'
    else:
        #questrows = db(db.question.id == chquestid).select()
        #quest = questrows.first()
        #eventpos = db(db.eventmap.questid == chquestid).select().first()

        event = db(db.event.id == eventid).select().first()
        if event.shared or (event.owner == auth.user.id):
            db(db.eventmap.questid == questid).update(xpos=newxpos, ypos=newypos)
            responsetext = 'Element moved'
        else:
            responsetext = 'Moves not saved - you must be owner of ' + event.event_name + 'to save changes'

    return responsetext
