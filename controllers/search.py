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
# pagination to be added here at some point but currently search limit of 20 and refine search will do

def newsearch():
    #term = request.args[0]
    #term = request.vars.keyword

    #fields= ['searchstring','sortorder','showscope','scope', 'continent','country',
    #         'subdivision','showcat','category']

    fields = ['searchstring']

    form = SQLFORM(db.viewscope, fields=fields)
    results = None

    if form.validate():
        query = indsearch.search(questiontext=form.vars.searchstring)

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
