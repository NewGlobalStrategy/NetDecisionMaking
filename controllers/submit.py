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

#
# This controller handles submission of questions and actions and confirmation 
# that the question has been submitted
###############################################################################


@auth.requires_login()
def new_question():
    #This allows creation of both questions and actions so the first
    #thing to do is establish whether question or action being submitted the
    #default is question unless action specified

    if request.args(1) > '0':
        priorquest = int(request.args(1))
    else:
        priorquest = 0

    if request.args(0) != 'action':
        heading = 'Submit Question'
        labels = {'questiontext': 'Question'}

        fields = ['questiontext', 'eventid', 'category', 'activescope',
                  'continent', 'country', 'subdivision', 'numanswers']

        extrafield1 = TR(LABEL('Answer 1:'), INPUT(_name='ans1', value="", _type="text"))
        extrafield2 = TR(LABEL('Answer 2:'), INPUT(_name='ans2', value="", _type="text"))
        extrafield3 = TR(LABEL('Answer 3:'), INPUT(_name='ans3', value="", _type="text"))
        extrafield4 = TR(LABEL('Answer 4:'), INPUT(_name='ans4', value="", _type="text"))
        extrafield5 = TR(LABEL('Answer 5:'), INPUT(_name='ans5', value="", _type="text"))
        extrafield6 = TR(LABEL('Answer 6:'), INPUT(_name='ans6', value="", _type="text"))
        extrafield7 = TR(LABEL('Answer 7:'), INPUT(_name='ans7', value="", _type="text"))
        extrafield8 = TR(LABEL('Answer 8:'), INPUT(_name='ans8', value="", _type="text"))
        extrafield9 = TR(LABEL('Answer 9:'), INPUT(_name='ans9', value="", _type="text"))
        extrafield10 = TR(LABEL('Answer 10:'), INPUT(_name='ans10', value="", _type="text"))
        form = SQLFORM(db.question, fields=fields, labels=labels, formstyle='table3cols')
        form[0].insert(-1, extrafield1)
        form[0].insert(-1, extrafield2)
        form[0].insert(-1, extrafield3)
        form[0].insert(-1, extrafield4)
        form[0].insert(-1, extrafield5)
        form[0].insert(-1, extrafield6)
        form[0].insert(-1, extrafield7)
        form[0].insert(-1, extrafield8)
        form[0].insert(-1, extrafield9)
        form[0].insert(-1, extrafield10)

    else:
        #action form submission
        heading = 'Submit Action'
        labels = {'questiontext': 'Action'}

        fields = ['questiontext', 'eventid', 'category', 'activescope',
                  'continent', 'country', 'subdivision', 'responsible',
                  'respemail', 'duedate']

        form = SQLFORM(db.question, fields=fields, labels=labels, formstyle='table3cols')

    if session.event_name:
        form.vars.eventid = session.eventid


    #this can be the same for both questions and actions
    if form.validate():
        form.vars.auth_userid = auth.user.id
        if request.args(0) == 'action':
            form.vars.qtype = 'action'
            form.vars.answers = ['Approve', 'Disapprove', 'OK']
            form.vars.numanswers = 2
        else:
            form.vars.answers = [form.vars.ans1, form.vars.ans2, form.vars.ans3,
                                 form.vars.ans4, form.vars.ans5, form.vars.ans6, form.vars.ans7,
                                 form.vars.ans8, form.vars.ans9, form.vars.ans10]
        scope = form.vars.activescope

        #if scope == '1 Global':
        #    activetext = 'Global'
        #elif scope == '2 Continental':
        #    activetext = form.vars.continent
        #elif scope == '3 National':
        #    activetext = form.vars.country
        #else:
        #    activetext = form.vars.subdivision

        #form.vars.scopetext = activetext
        form.vars.createdate = request.utcnow

        #form.vars.priorquests = priorquest - now need to process separately
        if request.args(0) != 'action':
            del form.vars['ans1']
            del form.vars['ans2']
            del form.vars['ans3']
            del form.vars['ans4']
            del form.vars['ans5']
            del form.vars['ans6']
            del form.vars['ans7']
            del form.vars['ans8']
            del form.vars['ans9']
            del form.vars['ans10']

        form.vars.id = db.question.insert(**dict(form.vars))
        response.flash = 'form accepted'
        session.lastquestion = form.vars.id
        session.eventid = form.vars.eventid
        if priorquest > 0 and db(db.questlink.sourceid == priorquest and
                                 db.questlink.targetid == form.vars.id).isempty():
            db.questlink.insert(sourceid=priorquest, targetid=form.vars.id)

        redirect(URL('accept_question', args=[form.vars.qtype]))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    return dict(form=form, heading=heading)


def accept_question():
    response.flash = "Details Submitted"
    if request.args(0) == 'action':
        qtype = 'action'
    else:
        qtype = 'question'
    # will now update priorquest with the subsequent question details
    # and this question with priorquest details
    if session.priorquest > 0:
        #append into priorquests and subsquests
        quest = db(db.question.id == session.priorquest).select(db.question.id,
                                                                db.question.subsquests).first()
        subsquests = quest.subsquests
        subsquests.append(session.lastquestion)
        quest.update_record(subsquests=subsquests)
        quest = db(db.question.id == session.lastquestion).select(db.question.id,
                                                                  db.question.priorquests).first()
        priorquests = quest.priorquests
        priorquests.append(session.priorquest)
        quest.update_record(priorquests=priorquests)
        session.lastquestion = 0
        session.priorquest = 0

    return locals()


#This is called via Ajax to populate the subdivision dropdown on change of country
#now changed to derelationalise country subdivision

def multi():
    #placeholder for discussion of the topic at present
    pass
    return locals()


def subdivn():
    result = "<option value='Unspecified'>Unspecified</option>"

    subdivns = db(db.subdivision.country == request.vars.country).select(
        db.subdivision.subdiv_name, cache=(cache.ram, 1200), cacheable=True)
    for row in subdivns:
        result += "<option value='" + str(row.subdiv_name) + "'>" + row.subdiv_name + "</option>"

    return XML(result)


def country():
    result = "<option value='Unspecified'>Unspecified</option>"
    countries = db(db.country.continent == request.vars.continent).select(
        db.country.country_name, cache=(cache.ram, 6000), cacheable=True)
    for countrie in countries:
        result += "<option value='" + str(countrie.country_name) + "'>" + countrie.country_name + "</option>"

    return XML(result)
