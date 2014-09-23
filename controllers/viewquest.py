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

"""
 This controller handles viewing the full details on questions if allowed
 and also displaying the reason you are not allowed to view the question
 the functionality to submit a challenge is also included in this controller
 and that is called via ajax from the view of the question detail
 The three functions are:
 index:  displays the question details
 notshowing: explains why the question can't be displayed - actions should always be displayed
 challenge: allows submission of a challenge and return of whether this is allowed
 via ajax
 For actions not generally interested in user's views but would like these to be capable
 of prioritisation at any stage - need to see the date and will be some options to generate
 emails based on actions and also to challenge resolved actions to return them to proposed
 A separate comments function has now been created
"""

from ndsfunctions import getwraptext
from jointjs2py import colourcode


def index():
    #This will be a general view on question details and it will require the 
    #question id as an argument Logic will be to only display the question if it
    #has been submitted, resolved or answered/passed by the user
    #This maintains the general privacy approach to questions that may be 
    #subject to answer eventually if resolved then there will be a view option
    #However approach for actions is different - they can be viewed at any time
    #but the buttons at the bottom should be very simlar

    #initialize variables as not used if action 
    viewtext = ''
    lstanswers = []
    lstnumanswers = []
    numpass = 0
    #not used if not answered    
    uqanswered = False
    uqurg = 5
    uqimp = 5
    uqans = 0
    questid = 0

    if len(request.args):
        questid = int(request.args[0])
    else:
        redirect(URL('gdms', 'viewquest', 'notshowing/' + 'NoQuestion'))

    #session.questid = questid # check why doing this

    questrow = db(db.question.id == questid).select(db.question.id, db.question.status,
                                                    db.question.qtype, db.question.questiontext, db.question.answers,
                                                    db.question.urgency,
                                                    db.question.importance, db.question.numanswers, db.question.level,
                                                    db.question.totanswers, db.question.category,
                                                    db.question.correctans,
                                                    db.question.correctanstext, db.question.answerreasons,
                                                    db.question.answerreason2,
                                                    db.question.answerreason3, db.question.answercounts,
                                                    db.question.auth_userid).first()

    if questrow is None:
        redirect(URL('gdms', 'viewquest', 'notshowing/' + 'NoQuestion'))
    else:
        quest = questrow.as_dict()

    if quest['qtype'] == 'quest':
        #View question logic 
        if auth.user is None:
            if quest['status'] != 'Resolved':
                redirect(URL('gdms', 'viewquest', 'notshowing/' + 'NotResolved/' + str(questid)))
        else:
            uq = db((db.userquestion.auth_userid == auth.user.id) & (db.userquestion.questionid
                                                                     == questid)).select(db.userquestion.id,
                                                                                         db.userquestion.urgency,
                                                                                         db.userquestion.importance,
                                                                                         db.userquestion.answer).first()
            if uq is None:
                uqanswered = False
                if quest['status'] != 'Resolved' and quest['auth_userid'] != auth.user:
                    redirect(URL('gdms', 'viewquest', 'notshowing/NotAnswered/' + str(questid)))
            else:
                uqanswered = True

        #now three scenarios now either the user has answered the question
        #or they haven't but it is resolved the population of the question variables
        #v2 if not answered we will now open a link to answer the question
        #to return to the view should be broadly the same in both scenarios
        #or they have submitted question and are being allowed to see progress

        #Get question details into a list of correct size
        #possibly just append

        mastlstanswers = quest['answers']
        mastlstnumanswers = quest['answercounts']

        k = quest['numanswers']
        lstanswers = mastlstanswers[:k]
        lstnumanswers = mastlstnumanswers[1:k + 1]
        numpass = mastlstnumanswers[0]

        #in terms of the user there are basically 3 things to pick-up on
        #the user answer
        #users rating of urgency and importance
        #did the user get this right (if resolved or under challenge)

        if uqanswered:
            uqurg = uq.urgency
            uqimp = uq.importance
            uqans = uq.answer

        #Now work out what we can say about this question
        #if resolved we can say if right or wrong and allow the question to be challenged
        if quest['status'] == 'Resolved':
            #Did the user answer the question
            if uqanswered:
                if uqans == 0:
                    viewtext = 'You passed on this question but it has now been resolved'
                elif quest['correctans'] == uqans:
                    viewtext = 'Well done - you helped resolve this question'
                else:
                    viewtext = 'Your answer to this question disagrees with the resolved'
                    'correct answer - you may want to request a challenge'
            else:
                viewtext = "You didn't get to answer this question"
        elif quest['status'] == 'Rejected':
            viewtext = "This question has been rejected"
        else:
            #if not resolved can only say in progress and how many more answers are required
            #at present should only be here if
            #answered as we are not showing users unresolved and unanswered questions
            viewtext = 'This question is in progress at level ' + str(quest['level'])

            #That will do for now - display of challenges and probably numanswers remaining
            #and level can be added later

    else:  # action
        #Get details of the action urgency and importance of actions is stored in a different table because they can
        #be prioritised without answering

        if auth.user is not None:
            uq = db((db.questurgency.auth_userid == auth.user.id) & (
                db.questurgency.questionid == questid)).select(db.questurgency.urgency,
                                                               db.questurgency.importance).first()

            if uq is not None:
                uqanswered = True
                uqurg = uq.urgency
                uqimp = uq.importance

    #need to get priorquests and subsquests as lists which may be empty for each quest now
    priorquestrows = db(db.questlink.targetid == questid).select(db.questlink.sourceid)
    subsquestrows = db(db.questlink.sourceid == questid).select(db.questlink.targetid)
    priorquests = [row.sourceid for row in priorquestrows]
    subsquests = [row.targetid for row in subsquestrows]

    return dict(quest=quest, viewtext=viewtext, lstanswers=lstanswers,
                lstnumanswers=lstnumanswers, uqanswered=uqanswered,
                uqurg=uqurg, uqimp=uqimp, numpass=numpass, priorquests=priorquests, subsquests=subsquests)


def qmap():
    #This generates a view of a question and it's parents  and children we are not now showing
    #siblings and partners - they can be shown on the main network view.  The web2py question ids need
    #to be passed into the objects - however these must be unique and we may want to present
    #the same question twice on the map so think we need to make the ids combine the role
    #and the id.  Current roles would be as follows:
    #
    #   1   Cen- the main central question on the map
    #   2   Par- a parent question
    #   3   Chi- a child question
    #
    #thinking we will have two different shapes of rectangle for questions and actions
    #questions will be longer and slightly narrower actions shorter and a little wider
    #wrapping of text will need to reflect this for now

    if len(request.args):
        questid = int(request.args[0])
    else:
        redirect(URL('gdms', 'viewquest', 'notshowing/' + 'NoQuestion'))

    questrow = db(db.question.id == questid).select(db.question.id, db.question.status,
                                                    db.question.qtype, db.question.questiontext, db.question.urgency,
                                                    db.question.importance, db.question.level, db.question.priority,
                                                    db.question.totanswers, db.question.category,
                                                    db.question.correctanstext, db.question.answercounts).first()

    if questrow == None:
        redirect(URL('gdms', 'viewquest', 'notshowing/' + 'NoQuestion'))
    else:
        quest = questrow.as_dict()

    #so have quest['subsquests'] and quest['priorquests'] which I think we want to make
    #into a list of objects and associated values qmap may as well be a dictionary I think
    #with name, position, colour, text and font size, no width and height for now think textwrap can provide the
    #text so in qmap name will be the key and then list of x,y,colour, text, font size
    #so in this scenario would have a main question and then prior and subs and outputs
    #are keys, qmap and qlink
    #for now lets hard code some positions in terms of lists
    #width=140, height=250

    xpos = [330, 170, 490, 10, 650]
    ypos = [10, 300, 550]

    obj = 'Cen' + str(questrow['id'])
    questmap = {}
    qlink = {}

    #for testing this allowed dummy linking
    #priortemp = [1,3,5]
    #substemp = [4,10,12]

    if quest['qtype'] == 'action':
        width = 200
        height = 100
        wraplength = 30
    else:
        width = 160
        height = 200
        wraplength = 25

    keys = '[' + obj
    #add the prior quests - so this should become a procedure shortly
    #with params and I think prefix plus quest ids is best as will need
    #to work back to updates to ids once we use events  - think we can just
    #make a new function here in first instance and then move in fact maybe just
    #iterate over the list here is fine with separate function for the text
    #but may then need second pass for next generation - but later
    #however they can be defined as query and then do 4 iterations
    #if siblings:

    #change to just be a single question
    parentquery = db.questlink.targetid == questid
    childquery = db.questlink.sourceid == questid
    #so this needs to b
    parentlinks = db(parentquery).select(db.questlink.id, db.questlink.sourceid, db.questlink.targetid)
    mylist = [x.sourceid for x in parentlinks]
    query = db.question.id.belongs(mylist)
    #query = db.question.id.belongs(priortemp)
    parentquests = db(query).select(db.question.id, db.question.questiontext, db.question.correctanstext,
                                    db.question.status,
                                    db.question.level, db.question.qtype, db.question.category, db.question.priority)

    for i, x in enumerate(parentquests):
        if x['qtype'] == 'action':
            width = 200
            height = 100
            wraplength = 30
        else:
            width = 160
            height = 200
            wraplength = 25
        qtext = getwraptext(x.questiontext, x.correctanstext, wraplength)
        rectcolour = colourcode(x.qtype, x.status, x.priority)

        strobj = 'Par' + str(x.id)
        strlink = 'Plk' + str(x.id)
        questmap[strobj] = [xpos[i], ypos[0], qtext, rectcolour, 12, 'b', width, height]
        #change to call function in the line above
        qlink[strlink] = [strobj, obj]
        keys += ','
        keys += strobj
        keys += ','
        keys += strlink

    if parentquests:
        ypos.pop(0)

    qtext = getwraptext(quest['questiontext'], quest['correctanstext'], wraplength)
    rectcolour = colourcode(quest['qtype'], quest['status'], quest['priority'])
    #add the main question
    questmap[obj] = [xpos[0], ypos[0], qtext, rectcolour, 12, 'tb', width, height]

    ypos.pop(0)

    childlinks = db(childquery).select(db.questlink.id, db.questlink.sourceid, db.questlink.targetid)
    mylist = [x.targetid for x in childlinks]
    query = db.question.id.belongs(mylist)
    #query = db.question.id.belongs(substemp)
    childquests = db(query).select(db.question.id, db.question.questiontext, db.question.correctanstext,
                                   db.question.status,
                                   db.question.level, db.question.qtype, db.question.category, db.question.priority)

    for i, x in enumerate(childquests):
        if x['qtype'] == 'action':
            width = 200
            height = 160
            wraplength = 30
        else:
            width = 160
            height = 200
            wraplength = 25
        qtext = getwraptext(x.questiontext, x.correctanstext, wraplength)
        rectcolour = colourcode(x.qtype, x.status, x.priority)
        strobj = 'Chi' + str(x.id)
        strlink = 'Clk' + str(x.id)
        questmap[strobj] = [xpos[i], ypos[0], qtext, rectcolour, 12, 't', width, height]
        qlink[strlink] = [obj, strobj]
        keys += ','
        keys += strobj
        keys += ','
        keys += strlink

    keys += ']'

    return dict(quest=quest, questmap=questmap, keys=keys, qlink=qlink)


def comments():
    #This will be a general view on question comments it will require the 
    #question id as an argument Logic will be to only display the comements if it
    #has been resolved
    #This maintains the general privacy approach to questions that may be 
    #subject to answer eventually if resolved then there will be a view option
    #this needs the as_dict() treatment as well but lets debug viewquest first
    # and then do next

    page = 0
    if len(request.args):
        questid = int(request.args[0])

        if len(request.args) > 1:
            page = request.args[1]
    else:
        redirect(URL('default', 'index'))

    session.questid = questid
    quest = db.question[questid].as_dict()

    if quest is None:
        redirect(URL('viewquest', 'notshowing/' + 'NoQuestion'))

    # create the form before the comments then it includes in subsequent refresh 
    if auth.user:
        form = crud.create(db.questcomment)
    else:
        form = 'You must be logged in to post comments'

    #Now select the question comments will have an add comments form if 
    #the user is logged in - else comment that must login to add comments
    #below logic needs fixed as now question is request.args[0] but can 
    #test the rest while I figure out how to fix

    if len(request.args) > 1:
        page = int(request.args[1])

    else:
        page = 0
    items_per_page = 3
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)

    basenum = items_per_page * page
    comments = db((db.questcomment.questionid == questid)).select(
        db.questcomment.id,
        db.questcomment.numreject, db.questcomment.comment,
        db.questcomment.commentdate, db.questcomment.status,
        orderby=[db.questcomment.commentdate], limitby=limitby)

    return dict(quest=quest, comments=comments, page=page,
                items_per_page=items_per_page, form=form, basenum=basenum)


def useranswers():
    #This displays all users answers to the question and challenges if any
    #for now will probably display all challenges at the bottom of the page
    #as assumption is there won't be too many of these
    # looks like this also needs as_dict treatment

    page = 0
    if len(request.args):
        questid = int(request.args[0])
        if len(request.args) > 1:
            page = request.args[1]
    else:
        redirect(URL('default', 'index'))

    session.questid = questid
    quest = db(db.question.id == questid).select(db.question.id, db.question.status,
                                                 db.question.qtype, db.question.questiontext, db.question.answers,
                                                 db.question.urgency,
                                                 db.question.importance, db.question.numanswers, db.question.level,
                                                 db.question.totanswers, db.question.category, db.question.correctans,
                                                 db.question.correctanstext, db.question.answerreasons,
                                                 db.question.answerreason2,
                                                 db.question.answerreason3, db.question.answercounts)[0]
    quest = db.question[questid].as_dict()

    if quest is None:
        redirect(URL('viewquest', 'notshowing/' + 'NoQuestion'))
    #Get question details into a list of correct size
    # this needs to become a function - duplicated code with viewquest

    mastlstanswers = quest['answers']
    mastlstnumanswers = quest['answercounts']

    k = quest['numanswers']
    lstanswers = mastlstanswers[:k]
    lstnumanswers = mastlstnumanswers[1:k + 1]
    numpass = mastlstnumanswers[0]

    #Now select the userquestion records in order by level

    if len(request.args) > 1:
        page = int(request.args[1])

    else:
        page = 0
    items_per_page = 21
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)

    uqs = db(db.userquestion.questionid == questid).select(db.userquestion.id,
                                                           db.userquestion.level, db.userquestion.auth_userid,
                                                           db.userquestion.answer,
                                                           db.userquestion.answerreason, db.userquestion.urgency,
                                                           db.userquestion.importance, db.userquestion.score,
                                                           orderby=[~db.userquestion.level], limitby=limitby)

    challs = db(db.questchallenge.questionid == questid).select(
        db.questchallenge.auth_userid, db.questchallenge.status,
        db.questchallenge.challengereason, db.questchallenge.challengedate,
        orderby=[~db.questchallenge.challengedate])

    return dict(quest=quest, uqs=uqs, page=page,
                items_per_page=items_per_page, lstanswers=lstanswers,
                lstnumanswers=lstnumanswers, challs=challs)


def notshowing():
    shortreason = request.args[0]
    questid = request.args[1]

    if shortreason == 'NotResolved':
        reason = "This question is not yet resolved and you haven't answered it"
    elif shortreason == 'NotAnswered':
        reason = 'You have not answered this question'
    elif shortreason == 'NoQuestion':
        reason = 'This question does not exist'
    else:
        reason = 'Not Known'
    return dict(reason=reason, questid=questid)


def create_action():
    quest = request.args[0]
    return dict(quest=quest)


def create_message():
    quest = request.args[0]
    return dict(quest=quest)


def challenge():
    #This allows users to challenge resolved questions - whether or not they have answered them - users are not
    #allowed to challenge questions that are not currently in a state of resolved and this should be done by the 
    #viewquestion function rather than the challenge ie option isn't available if question isn't resolved - actions 
    #are similar and would only be challenged once they are in a state of Agreed

    responsetext = 'na'
    chquestid = request.args[0]
    #reason = request.args[1]
    if auth.user is None:
        responsetext = 'You must be logged in to challenge a question'
    else:
        #find out if user has previously challenged the question - this will be a userchallenge record
        qcs = db((db.questchallenge.auth_userid == auth.user.id) & (db.questchallenge.questionid == chquestid)).select()
        qc = qcs.first()
        if qc is None:
            db.questchallenge.insert(questionid=chquestid, auth_userid=auth.user.id,
                                     challengereason=request.vars.challreason)
            #Now also need to add 1 to the numchallenges figure - I think this will reset when back to resolved and
            #It shouldn't be possible to challenge unless resolved
            questrows = db(db.question.id == chquestid).select()
            quest = questrows.first()
            numchallenges = quest.numchallenges + 1
            db(db.question.id == chquestid).update(numchallenges=numchallenges)
            if numchallenges >= 3:
                numchallenged = quest.numchallenged + 1
                newlevel = quest.level + 2
                #thinking behind this is to restore question two levels higher which is wher
                #it would have been if the 6 people had mixed up ie 3 think wrong and 3 that agreed
                db(db.question.id == chquestid).update(status='In Progress',
                                                       level=newlevel, numchallenges=0, numchallenged=numchallenged)
            responsetext = 'Challenge accepted'
        else:
            responsetext = 'You have already challenged this question and only 1 challenge is allowed at present'
    return responsetext


def agree():
    #This allows users to record if they agree or disagree with resolve questions
    #- whether or not they have answered them - only resolved questions can
    #be agreed or disagreed with

    responsetext = 'na'
    chquestid = request.args[0]
    agree = int(request.args[1])
    if auth.user == None:
        responsetext = 'You must be logged in to record agreement or disagreement'
    else:
        questrows = db(db.question.id == chquestid).select()
        quest = questrows.first()
        numagree = quest.numagree
        numdisagree = quest.numdisagree

        #find out if user has previously challenged the question - 
        #this will be a userchallenge record
        qcs = db((db.questagreement.auth_userid == auth.user.id) &
                 (db.questagreement.questionid == chquestid)).select()

        qc = qcs.first()

        if qc == None:
            db.questagreement.insert(questionid=chquestid,
                                     auth_userid=auth.user.id, agree=agree)
            #Now also need to add 1 to the numagreement or disagreement figure 
            #It shouldn't be possible to challenge unless resolved

            if agree == 1:
                numagree += 1
                responsetext = 'Agreement Recorded'
            else:
                numdisagree += 1
                responsetext = 'Disagreement Recorded'
        else:
            if agree == qc.agree:
                if agree == 1:
                    responsetext = 'You have already registered agreement'
                else:
                    responsetext = 'You have already registered your disagreement'
                    ' - you may be able to challenge'
            else:
                if agree == 1:
                    responsetext = 'Your vote has been changed to agreement'
                    numagree += 1
                    numdisagree -= 1
                else:
                    responsetext = 'Your vote has been changed to disagreement'
                    numagree += 1
                    numdisagree -= 1
                qc.update_record(agree=agree)

        db(db.question.id == chquestid).update(numagree=numagree,
                                               numdisagree=numdisagree)
    return responsetext


def flagcomment():
    #This allows users to record if they think a comment is inappropriate
    #if 3 separate users flag the comment then it is removed from display
    #permanently for now

    responsetext = ''
    commentid = request.args[0]
    requesttype = request.args[1]

    if auth.user is None:
        responsetext = 'You must be logged in to flage inappropriate comments'
    else:
        comment = db(db.questcomment.id == commentid).select(
            db.questcomment.id, db.questcomment.numreject,
            db.questcomment.usersreject, db.questcomment.status).first()

        if requesttype != 'admin':

            #chekc if user has previously challenged the question - 
            #this will be an entry in the usersreject field

            if comment.usersreject is not None and auth.user.id in comment.usersreject:
                responsetext = 'You have already flagged this comment'
            else:
                responsetext = 'Rejection recorded'
                comment.numreject += 1
                if comment.usersreject is not None:
                    comment.usersreject.append(auth.user.id)
                else:
                    comment.usersreject = [auth.user.id]
                if comment.numreject > 2:
                    comment.status = 'NOK'
                comment.update_record()
        else:
            responsetext = 'Admin hide successful'
            comment.update_record(status='NOK')

    return responsetext


def urgency():
    #This allows users to record or update their assessment of the urgency and
    #importance of an action as this helps with prioritising the actions that
    #are required - next step is to attempt to get the view sorted and will
    #retrieve this as part of main index controller

    if request.vars.urgslider2 is None:
        urgslider = 5
    else:
        urgslider = int(request.vars.urgslider2)

    if request.vars.impslider2 is None:

        impslider = 5
    else:
        impslider = int(request.vars.impslider2)

    responsetext = 'na'
    chquestid = request.args[0]
    if auth.user == None:
        responsetext = 'You must be logged in to record urgency and importance'
    else:
        questrows = db(db.question.id == chquestid).select()
        quest = questrows.first()
        qurgency = quest.urgency
        qimportance = quest.importance

        #find out if user has rated the question already
        qcs = db((db.questurgency.auth_userid == auth.user.id) &
                 (db.questurgency.questionid == chquestid)).select()

        qc = qcs.first()

        if qc == None:
            db.questurgency.insert(questionid=chquestid,
                                   auth_userid=auth.user.id,
                                   urgency=urgslider,
                                   importance=impslider)

            urgency = request.vars.urgslider2
            responsetext = 'Your assessment has been recorded'

        else:
            qc.update_record(urgency=request.vars.urgslider2,
                             importance=request.vars.impslider2)
            responsetext = 'Your assessment has been updated'

        if quest.totratings == 0:
            totratings = quest.totanswers
        else:
            totratings = quest.totratings

        urgency = (((quest.urgency * totratings) + urgslider) /
                   (totratings + 1))
        importance = (((quest.importance * totratings) + impslider) /
                      (totratings + 1))

        if qc is None:
            totratings += 1
        priority = urgency * importance  # perhaps a bit arbitary but will do for now

        db(db.question.id == chquestid).update(urgency=urgency,
                                               importance=importance, priority=priority, totratings=totratings)

    return responsetext



