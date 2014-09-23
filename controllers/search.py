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
# Russ also blogs occasionally at proudofyourplanent.blogspot.com
# His general thinking on why this project is very important is availalbe at
# http://www.scribd.com/doc/98216626/New-Global-Strategy
#
# search is now using the haystack plugin and generating a full text index on question text only
# which we might add a capabilty to filter by action or question
# it will allow generation of a list of up to x items to display the questions and status which I
# think may just be another method of populating the existing review function
# so looks like the in operator would work for this - but most likely search is different and we keep
# as separate function to begin with until requirements fully understood
# but by some means search will get a list of 20 items (which may be hard coded) GQL is limited to 
# 30 and then go and retrieve the related ids so will always be two queries one on the full text search
# which probably needs a bit of further understanding on my part
# and then a second one to get the questions which would have pagination I think
#
# pagination to be added here and link to viewquestion from the view - should be easy


def index():
    return dict()


def search():

    fields = ['searchstring']

    form = SQLFORM(db.viewscope, fields=fields)

    if form.validate():
        redirect(URL('search', 'haystack', args=[request.vars.searchstring]))

    return dict(form=form)


def quick():
    response.view = 'search/index.html'
    term = request.vars.keyword
    #so think this needs to be different on GAE - suck all to python and then search
    #that would do for now and question text to related ids is all we need to search
    # so maybe haystack plugin with fix for contains is still the way to go

    topic_search = db(db.question.questiontext.contains(term)).select()
    count = db(db.question.questiontext.contains(term)).count()

    #topic_search=db(db.question.id>0).select(db.question.questiontext).find(
    #    lambda row:row.questiontext.find(term))
    #count=len(topic_search)
    return dict(results=topic_search, count=count)


def haystack():
    response.view = 'search/search.html'
    #term = request.args[0]
    term = request.vars.keyword

    #fields= ['searchstring','sortorder','showscope','scope', 'continent','country',
    #         'subdivision','showcat','category']

    fields = ['searchstring']

    form = SQLFORM(db.viewscope, fields=fields)

    if form.validate():
        redirect(URL('search', 'haystack', args=[request.vars.searchstring]))

    query = indsearch.search(questiontext=term)

    #this now works thinking is that additional filters could kick in here
    #rather than add them to full text search to give combination - concern is that may need to recall search if 
    #first one gets everything fltered out and no longer a two query process 
    #would also like the filter selection as a plugin with associated script file to do 
    #the showing and hiding - as all based on viewscope this may be possible or perhaps thats a block
    #in the view not a plugin

    results = db(query).select(db.question.id, db.question.status, db.question.questiontext,
                               db.question.correctanstext, db.question.category, db.question.activescope,
                               db.question.qtype, db.question.resolvedate, db.question.createdate, db.question.priority,
                               orderby=db.question.status)
    count = 3
    if results:
        session.networklist = [x.id for x in results]
    else:
        session.networklist = []

    #topic_search=db(db.question.id>0).select(db.question.questiontext).find(
    #    lambda row:row.questiontext.find(term))
    #count=len(topic_search)
    return dict(form=form, results=results, count=count)
