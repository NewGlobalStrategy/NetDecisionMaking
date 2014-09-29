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
# Russ also blogs occasionally at proudofyourplanent.blogspot.com
# His general thinking on why this project is very important is availalbe at
# http://www.scribd.com/doc/98216626/New-Global-Strategy
#
# This is the main model definition file changes should be agonised over

import datetime
from plugin_hradio_widget import hradio_widget
from plugin_haystack import Haystack, SimpleBackend, GAEBackend

not_empty = IS_NOT_EMPTY()

db.define_table('question',
                Field('qtype', 'string', writable=False,
                      requires=IS_IN_SET(['quest', 'action']), default='quest'),
                Field('questiontext', 'text', label='Question', requires=not_empty),
                Field('level', 'integer', default=1, writable=False),
                Field('status', 'string', default='In Progress', writable=False,
                      requires=IS_IN_SET(['In Progress', 'Resolved', 'Agreed', 'Disagreed', 'Rejected'])),
                Field('auth_userid', 'reference auth_user', writable=False, label='Submitter', default=auth.user_id),
                Field('category', 'string', default='Unspecified', label='Category', comment='Optional'),
                Field('activescope', 'string', default='1 Global', label='Active Scope'),
                Field('continent', 'string', default='Unspecified', label='Continent'),
                Field('country', 'string', default='Unspecified', label='Country'),
                Field('subdivision', 'string', default='Unspecified', label='Sub-division eg State'),
                Field('scopetext', compute=lambda row: (row.activescope == '1 Global' and row.activescope) or
                                (row.activescope == '2 Continenal' and row.continent) or (row.activescope ==
                                '3 National' and row.country) or row.subdivision),
                Field('numanswers', 'integer', label='Number of Answers', default=2,
                      requires=IS_IN_SET([2, 3, 4, 5, 6, 7, 8, 9, 10])),
                Field('answers', 'list:string'),
                Field('answercounts', 'list:integer', default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                # always 11 items passes in element 0
                Field('totanswers', 'integer', default=0, writable=False),
                Field('correctans', 'integer', default=0, requires=IS_IN_SET([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                      writable=False, label='Correct Ans'),
                Field('correctanstext', 'string', label='Ans Text'),
                Field('urgency', 'decimal(6,2)', default=5, writable=False, label='Urgency'),
                Field('importance', 'decimal(6,2)', default=5, writable=False, label='Importance'),
                Field('totratings', 'integer', default=0, writable=False),
                Field('priority', 'decimal(6,2)', compute=lambda r: r['urgency'] * r['importance'], writable=False,
                      label='Priority'),
                Field('numchallenges', 'integer', default=0, readable=False),
                Field('numchallenged', 'integer', default=0, readable=False),
                Field('currentrouting', 'string', default='std', requires=IS_IN_SET(['std', 'vote']), writable=False),
                Field('unpanswers', 'integer', default=0, writable=False, readable=False),
                Field('createdate', 'datetime', writable=False, label='Date Submitted', default=request.utcnow),
                Field('resolvedate', 'datetime', writable=False, label='Date Resolved'),
                Field('answerreasons', 'text', writable=False, label='Reason1'),
                Field('answerreason2', 'text', writable=False, label='Reason2'),
                Field('answerreason3', 'text', writable=False, label='Reason3'),
                Field('numagree', 'integer', default=0, writable=False),
                Field('numdisagree', 'integer', default=0, writable=False),
                Field('responsible', 'string', label='Person or Group Responsible'),
                Field('respemail', 'string', label='Responsible e-mail address'),
                Field('respurl', 'string', label='Responsible website'),
                Field('contactmethod', 'string', requires=IS_IN_SET(['email', 'website']), default='email'),
                Field('duedate', 'datetime', label='Due Date', default=(request.utcnow + datetime.timedelta(days=365))),
                Field('achieved', 'integer', default=0),
                Field('eventid', 'reference event', label='Event',default=db(db.event.event_name =='Unspecified').select(
                    db.event.id).first().id),
                Field('challenge', 'boolean', default=False),
                Field('numcomments', 'integer', default=0, writable=False,
                      label='# of comments'), )  # numcomments not yet used

if request.env.web2py_runtime_gae:
    indsearch = Haystack(db.question, backend=GAEBackend)  # table to be indexed
    indsearch.indexes('questiontext','category') # lets go with this for now - some issues here but
                                                            #  questiontext never changes and category rarely and can do
                                                            #  defined update if it does answertext didnt work as not
                                                            # part of fieldset when record created
else:
    indsearch = Haystack(db.question)
    indsearch.indexes('questiontext','category')


db.question.category.requires = IS_IN_SET(settings.categories)
db.question.continent.requires = IS_IN_SET(settings.continents)
db.question.activescope.requires = IS_IN_SET(settings.scopes)


db.question.duedate.requires = IS_DATETIME_IN_RANGE(format=T('%Y-%m-%d %H:%M:%S'),
                                                    minimum=datetime.datetime(2013, 1, 1, 10, 30),
                                                    maximum=datetime.datetime(2030, 12, 31, 11, 45),
                                                    error_message='must be YYYY-MM-DD HH:MM::SS!')

db.question.respemail.requires = IS_EMPTY_OR(IS_EMAIL())

#This table holds records for normal question answers and also for answering
#challenges and actions - in fact no obvious reason to differentiate
#the question will hold a flag to determine if under challenge but only so 
#that the challengers get credit when resolved again if the answer is 
#different

db.define_table('userquestion',
                Field('questionid', db.question, writable=False),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False),
                Field('status', 'string', default='In Progress', writable=False, readable=False),
                Field('level', 'integer', readable=False, writable=False),
                Field('answer', 'integer', default=0, requires=IS_IN_SET([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                      label='My Answer'),
                Field('reject', 'boolean'),
                Field('urgency', 'integer', default=5, requires=IS_IN_SET([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                Field('importance', 'integer', default=5, requires=IS_IN_SET([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                Field('score', 'integer', writable='False'),
                Field('answerreason', 'text', label='Reasoning'),
                Field('ansdate', 'datetime', default=request.now, writable=False, readable=False),
                Field('category', 'string', default='Unspecified'),
                Field('activescope', 'string', default='1 Global'),
                Field('continent', 'string', default='Unspecified', label='Continent'),
                Field('country', 'string', default='Unspecified', label='Country'),
                Field('subdivision', 'string', default='Unspecified', label='Sub-division'),
                Field('changecat', 'boolean', default=False, label='Change Category'),
                Field('changescope', 'boolean', default=False, label='Change Scope'),
                #Field('reviewstatus', 'string', default='Not Reviewed', label='Review Status'),
                Field('resolvedate', 'datetime', writable=False, label='Date Resolved'))

#suggest using this to stop unnecessary indices on gae but doesn't work elsewhere so need to fix somehow
#,custom_qualifier={'indexed':False} think - retry this later
#db.table.field.extra = {} looks to be the way to do this in an if gae block

db.userquestion.category.requires = IS_IN_SET(settings.categories)
db.userquestion.continent.requires = IS_IN_SET(settings.continents)
db.userquestion.activescope.requires = IS_IN_SET(settings.scopes)

db.define_table('questchallenge',
                Field('questionid', 'reference question', writable=False, readable=False),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False),
                Field('status', 'string', default='In Progress', writable=False, readable=False),
                Field('challengereason', 'text'),
                Field('challengedate', 'datetime', default=request.now, writable=False, readable=False))


#this holds details of who has agreed and disagreed on the answer to a question
#no points are awarded for this at present but it may be configured to prevent
#challenges if the agreement to disagreement ratio is above some point this will also 
#now support logging agreement to actions and so urgency and importance have been 
#added to this table - however they are also picked up in userquestion - thinking is
#questions will not show this but actions will ie will pick-up in one place only
#Some users may want to record agreement without ranking immediately - but will
#accept their default values for now as no way of knowing if intended or not

db.define_table('questagreement',
                Field('questionid', 'reference question', writable=False),
                Field('auth_userid', 'reference auth_user', writable=False),
                Field('agree', 'integer', writable=False, readable=False),
                Field('agreedate', 'datetime', default=request.now, writable=False, readable=False),
                Field('urgency', 'integer', default=0, requires=IS_IN_SET([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                Field('importance', 'integer', default=0, requires=IS_IN_SET([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                Field('level', 'integer', default=1, readable=False, writable=False))

db.define_table('questurgency',
                Field('questionid', 'reference question', writable=False),
                Field('auth_userid', 'reference auth_user', writable=False),
                Field('urgency', 'integer', default=5, requires=IS_IN_SET([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                Field('importance', 'integer', default=5, requires=IS_IN_SET([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                Field('level', 'integer', default=1, readable=False, writable=False))


#questlinks replaces priorquests and subsquests in the questtion table at present as
#list reference fields weren't going to be enough to provide funcionality to 
#allow creation and deletion of links I now think the record gets deleted
#when delete count exceeds createcount and deletecount is also greater than one
#so that may mean that status can be a computed field but would need to be queried on
#so not a virtual field

db.define_table('questlink',
                Field('sourceid', 'reference question'),
                Field('targetid', 'reference question'),
                Field('createdby', 'reference auth_user', default=auth.user_id),
                Field('createcount', 'integer', default=1),
                Field('deletecount', 'integer', default=0),
                Field('status', 'string', default='Active'),
                Field('lastdeleter', 'reference auth_user'),
                Field('lastaction', 'string', default='create'),
                Field('createdate', 'datetime', default=request.utcnow, writable=False, readable=False))

#this holds comments for resolved questions
#it may be extended to allow comments against unresolved but not yet
#it will allow comments against actions that are proposed
#which is now a new status on actions where preceding question is not resolved
#and on follow-up questions

db.define_table('questcomment',
                Field('questionid', 'reference question', writable=False, readable=False,
                      default=session.questid),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False,
                      default=auth.user_id),
                Field('comment', 'text', requires=IS_NOT_EMPTY()),
                Field('status', 'string', default='OK', writable=False, readable=False,
                      requires=IS_IN_SET(['OK', 'NOK'])),
                Field('numreject', 'integer', default=0, writable=False, readable=False),
                Field('usersreject', 'list:integer', writable=False, readable=False),
                Field('commentdate', 'datetime', default=request.utcnow, writable=False, readable=False))



#This table is never populated but holds settings and options for configuring
#many of the displays of actions and questions

db.define_table('viewscope',
                Field('sortorder', 'string', default='1 Priority', label='Sort Order'),
                Field('qsortorder', 'string', default='1 Priority', label='Sort Order'),
                Field('asortorder', 'string', default='1 Answer Date', label='Sort Order'),
                Field('showscope', 'boolean', label='Show scope Filter', comment='Uncheck to show all'),
                Field('scope', 'string', default='1 Global'),
                Field('continent', 'string', default='Unspecified', label='Continent'),
                Field('country', 'string', default='Unspecified', label='Country'),
                Field('subdivision', 'string', default='Unspecified', label='Sub-division'),
                Field('showcat', 'boolean', label='Show Category Filter', comment='Uncheck to show all'),
                Field('category', 'string', default='Unspecified', label='Category', comment='Optional'),
                Field('searchstring', 'string', label='Search string'))


#lets see how the input works first
db.viewscope.category.requires = IS_IN_SET(settings.categories)
db.viewscope.scope.requires = IS_IN_SET(settings.scopes)
db.viewscope.continent.requires = IS_IN_SET(settings.continents)
db.viewscope.sortorder.requires = IS_IN_SET(['1 Priority', '2 Due Date', '3 Resolved Date', '4 Submit Date',
                                             '5 Responsible'])
db.viewscope.qsortorder.requires = IS_IN_SET(['1 Priority', '2 Resolved Date', '3 Submit Date'])
db.viewscope.asortorder.requires = IS_IN_SET(['1 Answer Date', '2 Resolved Date', '3 Category'])
db.viewscope.scope.widget = hradio_widget
db.viewscope.sortorder.widget = hradio_widget
db.viewscope.searchstring.requires = IS_NOT_EMPTY()
db.viewscope.qsortorder.widget = hradio_widget
db.viewscope.asortorder.widget = hradio_widget

#This contains two standard messages one for general objective and a second
#for specific action which someone is responsible for
db.define_table('message', Field('msgtype', 'string'),
                Field('description', 'text'),
                Field('message_text', 'text'))

db.define_table('eventmap',
    Field('eventid', 'reference event'),
    Field('questid', 'reference question'),
    Field('xpos', 'double', default=0.0, label='xcoord'),
    Field('ypos', 'double', default=0.0, label='ycoord'))

