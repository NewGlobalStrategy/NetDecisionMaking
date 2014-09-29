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


"""
This controller handles the selection of an available question and the 
answering of it
6 Mar 2013 - rewrite to improve logic and consider 'late' answers to questions
which might be quite common as operation of selection is to always give the
highest priority question out to all users and work on resolving it first
"""


def score_challengel(questid, successful, level):
    """
    This will reward those that raised a challenge if the answer has changed
    it may also spawn an issue of scoring users who previously thought they
    got it wrong but now got it right - thinking is we wouldn't remove
    points from those that were previously considered right
    """

    unpchallenges = db((db.questchallenge.questionid == questid) &
                       (db.questchallenge.status == 'In Progress')).select()

    # should get the score based on the level of the question
    # and then figure out whether
    # get the score update for a question at this level
    scoretable = db(db.scoring.level == level).select().first()

    if scoretable is None:
        rightchallenge = 30
        wrongchallenge = -10
    else:
        rightchallenge = scoretable.rightchallenge
        wrongchallenge = scoretable.wrongchallenge

    for row in unpchallenges:
        # update the overall score for the user
        user = db(db.auth_user.id == row.auth_userid).select().first()
        if successful is True:
            updscore = user.score + rightchallenge
        else:
            updscore = user.score + wrongchallenge
        level = user.level
        scoretable = db(db.scoring.level == level).select().first()
        nextlevel = scoretable.nextlevel

        if updscore > nextlevel:
            userlevel = user.level + 1
        else:
            userlevel = user.level

        db(db.auth_user.id == row.auth_userid).update(score=updscore,
                                                      level=userlevel)

    return


def score_lowerlevel(questid, correctans, score, level, wrong):
    """
    This may eventually be a cron job but for debugging it will need to be
    called from score_question basic approach is just to go through and update
    all the lower levels and if correct they get the values
    of the question which will probably be higher the higher the level it got
    resolved at so this isn't too complicated - but need to be passed the
    question-id, the correct answer and the number of
    points for correct and number for wrong - lets do later once main process
    working.
    Users get points for the level the question resolved at but need to acquire
    the level of points to move up from their level

    This needs some further work to cater for challenge questions which have a
    different 2nd resolved answer
    thinking is the original correct answers can stay because it was reasonable
    but those that got it wrong
    at lower levels should get some credit - however not critical for now -
    lets publish and see what other people consider best approach to this -
    it is not clear cut - nor critical to the principal of
    what we are trying to to do

    scoretable = db(db.scoring.level==level).select().first()
    score = scoretable.right
    there should be no need to assess changes to categories or scope
    in this process as these will all have been considered in previous rounds
    and the auth user running this should always be a user at the top level
    so no issues with auth not updating either - so we should be good to go
    """

    status = 'Resolved'

    unpanswers = db((db.userquestion.questionid == questid) &
                    (db.userquestion.status == 'In Progress')).select(db.userquestion.id,
                                                                      db.userquestion.questionid,
                                                                      db.userquestion.auth_userid,
                                                                      db.userquestion.status, db.userquestion.level,
                                                                      db.userquestion.answer,
                                                                      db.userquestion.reject, db.userquestion.score,
                                                                      db.userquestion.answerreason,
                                                                      db.userquestion.category,
                                                                      db.userquestion.activescope,
                                                                      db.userquestion.continent,
                                                                      db.userquestion.country,
                                                                      db.userquestion.subdivision,
                                                                      db.userquestion.changecat,
                                                                      db.userquestion.changescope,
                                                                      db.userquestion.resolvedate)

    for row in unpanswers:
        # work out if the question was correct or not
        if row.answer == correctans:
            actscore = score
            numcorrect = 1
            numwrong = 0
        elif row.answer == 0:
            actscore = 1
            numcorrect = 0
            numwrong = 0
        else:
            actscore = wrong
            numcorrect = 0
            numwrong = 1

        # update userquestion records to being scored change status
        db(db.userquestion.id == row.id).update(score=actscore, status=status, resolvedate=request.utcnow)
        # update the overall score for the user
        user = db(db.auth_user.id == row.auth_userid).select().first()
        updscore = user.score + actscore
        level = user.level
        scoretable = db(db.scoring.level == level).select(cache=(cache.ram, 1200), cacheable=True).first()
        nextlevel = scoretable.nextlevel

        if updscore > nextlevel:
            userlevel = user.level + 1
        else:
            userlevel = user.level

        db(db.auth_user.id == row.auth_userid).update(score=updscore,
                                                      level=userlevel, rating=user.level + userlevel,
                                                      numcorrect=user.numcorrect + numcorrect,
                                                      numwrong=user.numwrong + numwrong)

    return


@auth.requires_login()
def all_questions():
    """
    Used when no questions in the database that user has not already answered.
    """
    return locals()


@auth.requires_login()
def get_question():
    """
    Get unresolved question from the question database that the user has not answered.    
    This will now support both challenges and normal questions in 
    progress - both can hopefully go through the same flow and their is now
    just a boolean flag to represent a challenge so the challengees can be 
    given points too and they get them if the answer changes 
    a single function will do this retrieves the highest priority question that
    the user hasn't answered initially looking for questions at the same level 
    as the user and then lower level quetsions and finally
    higher level questions users can hopefully select whether to only approve
    actions or questions or approve both based on request.args(0)
    """

    # Added questlist to minimise database reads when running this and also
    # to create potential delay between submission and starting to answer
    # question - however issue is that this can be called 3 ways so got
    # 3 separate lists at present

    #first identify all questions that have been answered and are in progress

    global quests
    questrow = None
    questtype = 'all'
    if request.args(0) == 'action':
        questtype = 'action'
        if session.actionlist is None:
            session.actionlist = []
        elif len(session.actionlist) > 1:
            session.actionlist.pop(0)
            nextquest = str(session.actionlist[0])
            redirect(URL('answer_question/' + nextquest))

    elif request.args(0) == 'quest':
        questtype = 'quest'
        if session.questlist is None:
            session.questlist = []
        elif len(session.questlist) > 1:
            session.questlist.pop(0)
            nextquest = str(session.questlist[0])
            redirect(URL('answer_question/' + nextquest))

    session.comblist = None
    if session.comblist is None:
        session.comblist = []
    elif len(session.comblist) > 1:
        session.comblist.pop(0)
        nextquest = str(session.comblist[0])
        redirect(URL('answer_question/' + nextquest))

    if session.answered is None:
        session.answered = []
        ansquests = db((db.userquestion.auth_userid == session.userid) &
                       (db.userquestion.status == 'In Progress')).select(db.userquestion.questionid)

        for row in ansquests:
            session.answered.append(row.questionid)

    if session.exclude_cats is None:
        session.exclude_cats = auth.user.exclude_categories

    if session.continent == 'Unspecified':  # ie no geographic restriction
        for i in xrange(0, 4):
            if i == 0:
                query = (db.question.level == session.level) & (db.question.status == 'In Progress')
                orderstr = ~db.question.priority
            elif i == 1:
                if session.level < 2:
                    continue
                else:
                    query = (db.question.level < session.level) & (db.question.status == 'In Progress')
                    orderstr = ~db.question.level | ~db.question.priority
            elif i == 2:
                query = (db.question.level > session.level) & (db.question.status == 'In Progress')
                orderstr = db.question.level | ~db.question.priority
            elif i == 3:
                query = (db.question.status == 'In Progress')

            if questtype != 'all':
                query &= db.question.qtype == questtype

            if i < 3:
                quests = db(query).select(db.question.id, db.question.level, db.question.priority,
                                          db.question.category, orderby=orderstr,
                                          cache=(cache.ram, 120), cacheable=True)
            else:  # no caching for final attempt
                quests = db(query).select(db.question.id, db.question.level, db.question.priority,
                                          db.question.category, orderby=~db.question.priority)

            #exclude previously answered - this approach specifically taken rather than 
            #an outer join so it can work on google app engine
            #then filter for unanswered and categories users dont want questions on    
            alreadyans = quests.exclude(lambda row: row.id in session.answered)
            alreadyans = quests.exclude(lambda row: row.category in session.exclude_cats)
            questrow = quests.first()
            if questrow is not None:
                break

    else:
        #This is separate logic which applies when user has specified a continent - the general
        #thinking is that users cannot opt out of global questions but they may specify a continent
        #and optionally also a country and a subdivision in all cases we will be looking to 
        #run 4 queries the global and continental queries will always be the same but
        #the country and subdvision queries are conditional as country and subdivision
        #may be left unspecified in which case users should get all national quests for 
        #their continent or all local questions for their country - we will attempt to 
        #keep the same logic surrounding levels shorlty

        for i in xrange(0, 3):
            if i == 0:
                query = (db.question.level == session.level) & (db.question.status == 'In Progress')
            elif i == 1:
                if session.level < 2:
                    continue
                else:
                    query = (db.question.level < session.level) & (db.question.status == 'In Progress')
            elif i == 2:
                query = (db.question.level > session.level) & (db.question.status == 'In Progress')
            elif i == 3:
                query = (db.question.status == 'In Progress')

            if questtype != 'all':
                query &= db.question.qtype == questtype
            qcont = query & (db.question.continent == auth.user.continent) & (
                db.question.activescope == '2 Continental')
            qglob = query & (db.question.activescope == '1 Global')

            if auth.user.country == 'Unspecified':
                qcount = query & (db.question.continent == auth.user.continent) & (
                    db.question.activescope == '3 National')
            else:
                qcount = query & (db.question.country == auth.user.country) & (db.question.activescope == '3 National')

            if auth.user.subdivision == 'Unspecified':
                qlocal = query & (db.question.country == auth.user.country) & (db.question.activescope == '4 Local')
            else:
                qlocal = query & (db.question.subdivision == auth.user.subdivision) & (
                    db.question.activescope == '4 Local')

            questglob = db(qglob).select(db.question.id, db.question.level, db.question.priority,
                                         db.question.category)

            questcont = db(qcont).select(db.question.id, db.question.level, db.question.priority,
                                         db.question.category)

            questcount = db(qcount).select(db.question.id, db.question.level, db.question.priority,
                                           db.question.category)

            questlocal = db(qlocal).select(db.question.id, db.question.level, db.question.priority,
                                           db.question.category)

            quests = (questglob | questcont | questcount | questlocal).sort(lambda r: r.priority, reverse=True)

            alreadyans = quests.exclude(lambda r: r.id in session.answered)
            alreadyans = quests.exclude(lambda r: r.category in session.exclude_cats)
            questrow = quests.first()

            if questrow is not None:
                break

    if questrow is None:
        #No questions because all questions in progress are answered
        redirect(URL('all_questions'))


    #put quests into a list of id's to only run this when
    #we run out of questions for this user ie make a queue or change selection 
    #type for the list we want to answer

    if questtype == 'action':
        for row in quests:
            session.actionlist.append(row.id)
    elif questtype == 'quest':
        for row in quests:
            session.questlist.append(row.id)
    else:
        for row in quests:
            session.comblist.append(row.id)

    redirect(URL('answer_question/' + str(questrow.id)))
    return ()


@auth.requires_login()
def answer_question():
    """
    This allows the user to answer the question or pass and the result is 
    handled by the score question function.  This can really now be called
    from any event and it is an exposed url - so now need to check if not 
    resolved or already answered and if so we will not accept another answer
    """

    questid = int(request.args[0])
    # This will display the question submitted to it by get_question

    # added for v2 to support direct entry to answer questio - may be more changes
    # required

    form2 = SQLFORM(db.userquestion, showid=False, fields=['answer', 'reject',
                                                           'urgency', 'importance', 'answerreason', 'changecat',
                                                           'category', 'changescope',
                                                           'activescope', 'continent', 'country', 'subdivision'],
                    submit_button='Answer', col3={'answer': 'Enter 0 to Pass',
                                                  'reject': 'Select if invalid or off subject '},
                    hidden=dict(level='level'), formstyle='table3cols')

    quest = db(db.question.id == questid).select(db.question.id, db.question.questiontext,
                                                 db.question.category, db.question.activescope, db.question.scopetext,
                                                 db.question.qtype, db.question.numanswers, db.question.answers,
                                                 db.question.status,
                                                 db.question.continent, db.question.country, db.question.subdivision,
                                                 cache=(cache.ram, 600), cacheable=True).first().as_dict()

    if quest['status'] != 'In Progress':
        redirect(URL('viewquest', 'index', args=[questid]))
    else:
        uq = db((db.userquestion.questionid == questid) &
                (db.userquestion.status == 'In Progress') &
                (db.userquestion.auth_userid == auth.user_id)).select(db.userquestion.id).first()
        if uq:
            redirect(URL('viewquest', 'index', args=[questid]))

    # Took level out of this as it cannot be cached

    form2.vars.activescope = quest['activescope']
    form2.vars.continent = quest['continent']
    form2.vars.country = quest['country']
    form2.vars.subdivision = quest['subdivision']
    form2.vars.category = quest['category']

    if form2.validate():
        form2.vars.auth_userid = auth.user.id
        form2.vars.questionid = questid
        #get latest level not really cacheable 
        questlev = db(db.question.id == questid).select(db.question.level).first().as_dict()
        form2.vars.level = questlev['level']
        form2.vars.status = 'In Progress'
        form2.vars.id = db.userquestion.insert(**dict(form2.vars))
        response.flash = 'form accepted'
        redirect(URL('score_question/' + str(form2.vars.id)))
    elif form2.errors:
        response.flash = 'form has errors'
    else:
        pass
        #response.flash = 'please fill out the form'

    form2.vars.continet = quest['continent']
    form2.vars.country = quest['country']
    form2.vars.subdivision = quest['subdivision']
    form2.vars.category = quest['category']
    #need to get priorquests and subsquests as lists which may be empty for each quest now
    priorquestrows = db(db.questlink.targetid == questid).select(db.questlink.sourceid)
    subsquestrows = db(db.questlink.sourceid == questid).select(db.questlink.targetid)
    priorquests = [row.sourceid for row in priorquestrows]
    subsquests = [row.targetid for row in subsquestrows]

    return dict(form2=form2, quest=quest, priorquests=priorquests, subsquests=subsquests)


@auth.requires_login()
def score_question():
    """
    This procedure updates the question and userquestion records after each answer
    The update is in 2 parts.  The number of answers and so on are
    always updated however the main scoring only happens when we have 3 or more
    unprocessed answers.
    """

    ANSWERS_PER_LEVEL = 3  # this may be retrieved from a table later however
    # no rush to add alternative scoring schemes KISS
    # and would then retrieve this from a number of resolution
    # options

    # Initial processing that happens all the time
    intrec = int(request.args[0])
    uq = db.userquestion[intrec]

    quest = db(db.question.id == uq.questionid).select(db.question.id, db.question.qtype,
                                                       db.question.unpanswers, db.question.urgency,
                                                       db.question.importance, db.question.answercounts,
                                                       db.question.level, db.question.category, db.question.activescope,
                                                       db.question.continent,
                                                       db.question.country, db.question.subdivision,
                                                       db.question.scopetext, db.question.correctans,
                                                       db.question.totanswers, db.question.status, db.question.answers,
                                                       db.question.auth_userid,
                                                       db.question.challenge).first()

    # first step is to select the related user and question records their should
    # only ever be one of each of these and we update as much as possible here 
    # because it's interesting to see as much as possible on viewquest rather
    # than waiting until 3 people have answered and it can be scored - however this can result in
    # a degree of double updating

    if quest.qtype == 'action':
        # create a 'questurgency' record if action only - thinking is that
        #prioritising actions in progress is wortwhile and open to all 

        db.questurgency.update_or_insert((db.questurgency.auth_userid == auth.user.id)
                                         & (db.questurgency.questionid == quest.id), questionid=quest.id,
                                         auth_userid=auth.user.id,
                                         urgency=uq.urgency, importance=uq.importance)

    intunpanswers = quest.unpanswers
    # only update unpanswers if the userd didn't pass otherwise just keep going
    #until we get 3 actual answers or rejections   
    if uq.answer > 0 or uq.reject is True:
        intunpanswers += 1

    numquests = auth.user.numquestions + 1
    db(db.auth_user.id == auth.user.id).update(numquestions=numquests)
    auth.user.update(numquestions=numquests)
    if session.answered:
        session.answered.append(uq.questionid)

        #do weighted averaging of urgency and importance based on userquest
    urgency = (((quest.urgency * quest.totanswers) + uq.urgency) /
               (quest.totanswers + 1))
    importance = (((quest.importance * quest.totanswers) + uq.importance) /
                  (quest.totanswers + 1))

    anscount = quest.answercounts
    anscount[uq.answer] += 1

    #update the question record based on above
    db(db.question.id == quest.id).update(answercounts=anscount, totanswers=quest.totanswers + 1,
                                          urgency=urgency, importance=importance, unpanswers=intunpanswers)

    #the basic flow here is to establish if the question needs scored and then
    #establish if answers agree, disagree or if a majority have rejected the 
    #question if a minority have rejected the question then I think correct 
    #process is to escalate as unresolved

    stdrouting = ANSWERS_PER_LEVEL
    status = 'In Progress'
    changecat = False
    changescope = False

    if intunpanswers >= stdrouting:
        #scorequestions - need to get all the answers first at this level - 
        #should agree to unpanswers and should be a small number - so lets fully
        #score these - if they don't agree to unpanswers then doesn't agree
        #and will need to be escalated - so simple score if resolved - lower 
        #levels will probably be done as a background task eventually so seems 
        #ok this should never happen on a passed question at present challengees
        #are not getting credit for right or wrong challenges - this will be 
        #added in a subsequent update not that complicated to do however

        level = quest.level
        numanswers = 0
        numreject = 0
        numchangescope = 0
        numchangecat = 0
        updatedict = {'unpanswers': 0}

        #this will be changed to a single select and process the rows 
        #object to get counts etc
        unpanswers = db((db.userquestion.questionid == uq.questionid) &
                        (db.userquestion.status == 'In Progress') &
                        (db.userquestion.level == level)).select(db.userquestion.id,
                                                                 db.userquestion.questionid,
                                                                 db.userquestion.auth_userid,
                                                                 db.userquestion.status, db.userquestion.level,
                                                                 db.userquestion.answer,
                                                                 db.userquestion.reject, db.userquestion.score,
                                                                 db.userquestion.answerreason, db.userquestion.category,
                                                                 db.userquestion.activescope, db.userquestion.continent,
                                                                 db.userquestion.country, db.userquestion.subdivision,
                                                                 db.userquestion.changecat, db.userquestion.changescope,
                                                                 db.userquestion.resolvedate)

        for row in unpanswers:
            if row.answer == uq.answer:
                numanswers += 1
            if row.reject is True:
                numreject += 1
            if row.changescope is True:
                numchangescope += 1
            if row.changecat is True:
                numchangecat += 1

                #get the score update for a question at this level
        scoretable = db(db.scoring.level == level).select(cache=(cache.ram, 1200), cacheable=True).first()
        if scoretable is None:
            score = 30
            wrong = 1
            submitter = 1
        else:
            submitter = scoretable.submitter
            if quest.qtype != 'action':
                score = scoretable.right
                wrong = scoretable.wrong
            else:
                score = scoretable.rightaction
                wrong = scoretable.wrongaction

        anstext = ""
        ansreason = ""
        ansreason2 = ""
        ansreason3 = ""

        if numanswers >= stdrouting:  # all answers agree or at least as many as
            # stdrouting this is ok as if rejected and answered
            # then we will accept the answer
            status = 'Resolved'
            correctans = uq.answer
            numcorrect = 1
            answerlist = quest['answers']
            anstext = answerlist[correctans - 1]
            updatedict['correctans'] = correctans
            updatedict['correctanstext'] = anstext

        elif (numreject * 2) > stdrouting:  # majority reject
            status = 'Rejected'
            correctans = 0
        else:
            # no unanimity and this is required for std routing so promote
            level += 1
            updatedict['level'] = level
            status = 'In Progress'
            correctans = 0

        if (numchangescope * 2) > stdrouting:  # majority want to move scope
            changescope = True
            scopedict = {}
            contdict = {}
            countrydict = {}
            localdict = {}

        if (numchangecat * 2) > stdrouting:  # majority want to move category
            changecat = True
            catdict = {}

        #update userquestion records  

        for row in unpanswers:
            # update userquestion records to being scored change status
            # however some users may have passed on this question so need 
            # a further condition and the question is still resolved
            # also need to consider the change scope and change category
            # but only if a majority want this otherwise will stay as is
            # change cat and change scope are slightly different as change
            # of scope might be agreed but the correct continent or country
            # may differ in which case the question will have scope changed
            # but continent or country unchanged

            numcorrect = 0
            numwrong = 0
            numpassed = 0

            user = db(db.auth_user.id == row.auth_userid).select().first()

            #Get the score required for the user to get to next level
            scoretable = db(db.scoring.level == user.level).select(cache=(cache.ram, 1200), cacheable=True).first()
            if scoretable is None:
                nextlevel = 1000
            else:
                nextlevel = scoretable.nextlevel

            if row.answer == correctans and correctans > 0:  # user got it right
                numcorrect = 1
                #update the overall score for the user
                updscore = score
                if row.answerreason != '':
                    if ansreason == '':
                        ansreason = row.answerreason
                        updatedict['answerreasons'] = ansreason
                    elif ansreason2 == '':
                        ansreason2 = row.answerreason
                        updatedict['answerreason2'] = ansreason2
                    else:
                        ansreason3 = row.answerreason
                        updatedict['answerreason3'] = ansreason3
            elif row.answer == 0:  # user passed
                numpassed = 1
                updscore = 1
            elif correctans == 0:  # not resolved yet
                numrong = 0
                updscore = 0
            else:  # user got it wrong - this should be impossible at present as unanimity reqd
                numwrong = 1
                updscore = wrong

            #this needs rework
            if status == 'Resolved':
                row.update_record(status=status, score=updscore, resolvedate=request.utcnow)
            else:
                row.update_record(status=status, score=updscore)

            if updscore > nextlevel:
                userlevel = user.level + 1
            else:
                userlevel = user.level

            updscore = user.score + updscore

            db(db.auth_user.id == row.auth_userid).update(score=updscore, level=userlevel, rating=userlevel,
                                                          numcorrect=user.numcorrect + numcorrect,
                                                          numwrong=user.numwrong + numwrong,
                                                          numpassed=user.numpassed + numpassed)

            if auth.user.id == row.auth_userid:  # update auth values
                auth.user.update(score=updscore, level=userlevel, rating=userlevel, numcorrect=
                auth.user.numcorrect + numcorrect, numwrong=auth.user.numwrong + numwrong,
                                 numpassed=auth.user.numpassed + numpassed)

            if changecat is True:
                suggestcat = row.category
                if suggestcat in catdict:
                    catdict[suggestcat] += 1
                else:
                    catdict[suggestcat] = 1

            if changescope is True:
                # perhaps do as two dictionaries
                # do both of these the same way for consistency
                suggestscope = row.activescope
                suggestcont = row.continent
                suggestcountry = row.country
                suggestlocal = row.subdivision
                if suggestscope in scopedict:
                    scopedict[suggestscope] += 1
                else:
                    scopedict[suggestscope] = 1
                if suggestcont in contdict:
                    contdict[suggestcont] += 1
                else:
                    contdict[suggestcont] = 1
                if suggestcountry in countrydict:
                    countrydict[suggestcountry] += 1
                else:
                    countrydict[suggestcountry] = 1
                if suggestlocal in localdict:
                    localdict[suggestlocal] += 1
                else:
                    localdict[suggestlocal] = 1

        #update the question to resolved or promote as unresolved 
        #and insert the correct answer values for this should be set above
        suggestcat = quest.category
        suggestscope = quest.activescope
        suggestcont = quest.continent
        suggestcountry = quest.country
        suggestlocal = quest.subdivision
        scopetext = quest.scopetext

        if changecat is True:
            # loop through catdict and determine if any value has majority value
            for j in catdict:
                if (catdict[j] * 2) > stdrouting:
                    suggestcat = j
        if changescope is True:
            # loop through catdict and determine if any value has majority value
            for j in scopedict:
                if (scopedict[j] * 2) > stdrouting:
                    suggestscope = j
            for j in contdict:
                if (contdict[j] * 2) >= stdrouting:
                    suggestcont = j
            for j in countrydict:
                if (countrydict[j] * 2) >= stdrouting:
                    suggestcountry = j
            for j in localdict:
                if (localdict[j] * 2) >= stdrouting:
                    suggestlocal = j
            scopetype = suggestscope

            if scopetype == '1 Global':
                scopetext = '1 Global'
            elif scopetype == '2 Continental':
                scopetext = suggestcont
            elif scopetype == '3 National':
                scopetext = suggestcountry
            else:
                scopetext = suggestlocal

        #This is all to minimise unnecessary updates as there are a lot of indexes
        #on the question table and lots of write activity being triggered from the
        #updates

        if suggestcat != quest.category:
            updatedict['category'] = suggestcat
        if suggestscope != quest.activescope:
            updatedict['activescope'] = suggestscope
        if suggestcont != quest.continent:
            updatedict['continent'] = suggestcont
        if suggestcountry != quest.country:
            updatedict['country'] = suggestcountry
        if suggestlocal != quest.subdivision:
            updatedict['sudvision'] = suggestlocal
        if scopetext != quest.scopetext:
            updatedict['scopetext'] = scopetext

        updstatus = status
        if quest.qtype == 'action':
            if correctans == 1:
                updstatus = 'Agreed'
            else:
                updstatus = 'Disagreed'
        if updstatus != quest.status:
            updatedict['status'] = updstatus
            updatedict['resolvedate'] = request.utcnow

        db(db.question.id == quest.id).update(**updatedict)

        submitrow = db(db.auth_user.id == quest.auth_userid).select().first()
        submitter = submitter + submitrow.score

        db(db.auth_user.id == quest.auth_userid).update(score=submitter)

        if submitrow.id == auth.user.id:
            auth.user.update(score=submitter)

            # display the question and the user status and the userquestion status
            # hitting submit should just get you back to the answer form I think and 
            # fields should not be updatable

        if status == 'Resolved' and level > 1:
            score_lowerlevel(quest.id, correctans, score, level, wrong)
            if quest.challenge is True:
                if correctans == quest.correctans:
                    successful = False
                else:
                    successful = True
                #score_challenge(quest.id, successful, level)
    else:  # intunpanswers < stdrouting
        #the general requirement here is to do nothing - however because the
        #solution focuses on solving the highest priority question at all times
        #different users may be sent the same question at the same time and
        #answers may be received for a level after the question is either promoted
        #or resolved - promotions shouldn't be an issue but resolved questions are
        #because the user should probably get credit if right and nothing if wrong
        #and an explanation of what happend

        if quest.status == 'Resolved' or quest.status == 'Agreed':
            #get the score - if right add to score - if wrong same
            #update userquestion and user - other stuff doesn't apply
            scoretable = db(db.scoring.level == quest.level).select(cache=(cache.ram, 1200), cacheable=True).first()
            if scoretable is None:
                score = 30
                wrong = 1
                submitter = 1
            else:
                submitter = scoretable.submitter
                if quest.qtype != 'action':
                    score = scoretable.right
                    wrong = scoretable.wrong
                else:
                    score = scoretable.rightaction
                    wrong = scoretable.wrongaction
            numcorrect = 0
            numwrong = 0
            numpassed = 0

            if uq.answer == quest.correctans:
                updscore = score
                numcorrect = 1
            elif uq.answer == 0:
                updscore = 1
                numpasse = 1
            else:
                updscore = wrong
                numwrong = 1

            uq.update_record(status='Resolved', score=updscore, resolvedate=request.utcnow)
            updscore = auth.user.score + updscore

            db(db.auth_user.id == auth.user.id).update(score=updscore,
                                                       numcorrect=auth.user.numcorrect + numcorrect,
                                                       numwrong=auth.user.numwrong + numwrong,
                                                       numpassed=auth.user.numpassed + numpassed)

            auth.user.update(score=updscore,
                             numcorrect=auth.user.numcorrect + numcorrect,
                             numwrong=auth.user.numwrong + numwrong,
                             numpassed=auth.user.numpassed + numpassed)

    redirect(URL('viewquest', 'index', args=quest.id))

    return locals()
