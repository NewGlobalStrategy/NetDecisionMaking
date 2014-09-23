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

#form = SQLFORM(..., formstyle = SQLFORM.formstyles.bootstrap3)
#grid = SQLFORM.grid(..., formstyle = SQLFORM.formstyles.bootstrap3) rubbish
#grid = SQLFORM.smartgrid(..., formstyle = SQLFORM.formstyles.bootstrap3)
#class="btn btn-primary btn-lg btn-block" - next find the button setup
#class="btn btn-primary"
#A(download.title, _href=URL("getfile", args=download.file))
#response.formstyle = 'bootstrap3_inline' # or 'bootstrap3_stacked'


def index():
    """
    This is the startup function.
    
    It retrieves the 5 highest priority actions, 5 most recently resolved quests
    and highest priority quests in progress.
        
    For actions - any status except rejected are wanted but to avoid an or or a
    not for GAE we will use ans3 for this purpose with numans always two for an 
    action this is ok.  All queries are cached for 2 mins which should be OK
    """

    response.flash = "Welcome to Net Decision Making"
    #Move subject table to website parameters - think how this fits in though
    #think this should be done elsewhere
    #subj = db(db.subject.id>0).select(db.subject.longdesc).first()
    if WEBSITE_PARAMETERS:
        pass
    else:
        redirect(URL('admin', 'init'))

    response.title = "Net Decision Making"

    return dict(title=response.title)


def questload():
    #this came from resolved and thinking is it may replace it in due course but have
    #take then hradio button form out for now at least
    #need to get the event id into the query in due course but get it basically working
    #first

    if request.vars.page:
        page = int(request.vars.page)
    else:
        page = 0

    if request.vars.items_per_page:
        items_per_page = int(request.vars.items_per_page)
    else:
        items_per_page = 3

    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    q = 'std'

    if request.vars.sortby:
        if request.vars.sortby == 'ResDate':
            sortby = ~db.question.resolvedate
        else:
            sortby = ~db.question.priority
    else:
        sortby = ~db.question.createdate

    if request.vars.query:
        if request.vars.query == 'inprog':
            q = 'inprog'
            query = (db.question.qtype == 'quest') & (db.question.status == 'In Progress')
            quests = db(query).select(db.question.id, db.question.questiontext, db.question.level, db.question.priority,
                                      orderby=[sortby], limitby=limitby, cache=(cache.ram, 1200), cacheable=True)
        elif request.vars.query == 'event':
            q = 'event'
            query = (db.question.eventid == session.eventid)
            quests = db(query).select(db.question.id, db.question.questiontext, db.question.level, db.question.priority,
                                      orderby=[sortby], limitby=limitby, cache=(cache.ram, 1200), cacheable=True)
    else:
        query = (db.question.qtype == 'quest') & (db.question.status == 'Resolved')
        quests = db(query).select(db.question.id, db.question.questiontext, db.question.status, db.question.level,
                                  db.question.priority, db.question.correctanstext, db.question.numagree,
                                  db.question.numdisagree, orderby=[sortby], limitby=limitby,cache=(cache.ram, 1200), cacheable=True)

    return dict(quests=quests, page=page, items_per_page=items_per_page, q=q)


def actionload():
    #this came from questload and it may make sense to combine - however fields
    #and query would be different lets confirm works this way and then think about it

    if request.vars.page:
        page = int(request.vars.page)

    else:
        page = 0

    items_per_page = 3
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    q = 'std'
    if request.vars.query == 'home':
        q = 'home'

    query = (db.question.qtype == 'action') & (db.question.status == 'Agreed')
    sortby = ~db.question.createdate

    actions = db(query).select(db.question.id, db.question.status, db.question.questiontext, db.question.duedate,
                               db.question.responsible, db.question.priority, db.question.achieved,
                               db.question.activescope, db.question.category, db.question.continent,
                               db.question.country, db.question.subdivision, db.question.scopetext,
                               orderby=sortby, limitby=limitby, cache=(cache.ram, 1200), cacheable=True)

    return dict(actions=actions, page=page, items_per_page=items_per_page, q=q)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """

    #if request.args[0][:8] == "register":
    response.title = "Net Decision Making"

    session.exclude_cats = None
    session.comblist = None
    session.questlist = None
    session.actlist = None
    session.continent = None
    session.country = None
    session.subdivision = None
    session.eventid = None

    return dict(form=auth())


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
