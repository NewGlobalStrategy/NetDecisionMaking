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


# The first user to register gets given admin privileges
# However for now the only routing supported will be standard routing - but
# may add different numbers of participants at each layer and %age agreement
# below 100% at some stage
# probably should be a manager page of links

import time


@auth.requires_membership('manager')
def index():
    return locals()


# @auth.requires_membership('manager')
# def config():
# grid = SQLFORM.grid(db.config)
#    return dict(grid=grid)

@auth.requires_membership('manager')
def scoring():
    grid = SQLFORM.grid(db.scoring, orderby=[db.scoring.level])
    return dict(grid=grid)


# This allows editing of the website_parameters of the decision making system
@auth.requires_membership('manager')
def website_parameters():
    grid = SQLFORM.grid(db.website_parameters)
    return dict(grid=grid)


# This allows editing of the categories within the subject of the system
@auth.requires_membership('manager')
def category():
    grid = SQLFORM.grid(db.category)
    #form = crud.create(db.category,message='category added')    
    return dict(grid=grid)


@auth.requires_membership('manager')
def mgr_questions():
    grid = SQLFORM.grid(db.question, ignore_rw=True, orderby=[~db.question.createdate],
                        formstyle=SQLFORM.formstyles.bootstrap3_inline)
    return locals()


@auth.requires_membership('manager')
def mgr_answers():
    grid = SQLFORM.grid(db.userquestion, ignore_rw=True, orderby=[~db.userquestion.ansdate])
    return locals()


@auth.requires_membership('manager')
def mgr_users():
    grid = SQLFORM.grid(db.auth_user, ignore_rw=True, orderby=[~db.auth_user.id])
    return locals()


@auth.requires_membership('manager')
def mgr_resolved():
    grid = SQLFORM.grid(db.question.status == 'Resolved', orderby=[~db.question.resolvedate])
    return locals()


@auth.requires_membership('manager')
def continent():
    grid = SQLFORM.grid(db.continent)
    return dict(grid=grid)


@auth.requires_membership('manager')
def country():
    grid = SQLFORM.grid(db.country)
    return dict(grid=grid)


@auth.requires_membership('manager')
def subdivision():
    grid = SQLFORM.grid(db.subdivision)
    return dict(grid=grid)


@auth.requires_membership('manager')
def messages():
    grid = SQLFORM.grid(db.message)
    return dict(grid=grid)


@auth.requires_membership('manager')
def company():
    grid = SQLFORM.grid(db.company)
    return dict(grid=grid)


@auth.requires_membership('manager')
def individual():
    grid = SQLFORM.grid(db.individual)
    return dict(grid=grid)


@auth.requires_membership('manager')
def event():
    grid = SQLFORM.grid(db.event)
    return dict(grid=grid)


@auth.requires_membership('manager')
def eventmap():
    grid = SQLFORM.grid(db.eventmap)
    return dict(grid=grid)


@auth.requires_membership('manager')
def location():
    grid = SQLFORM.grid(db.location)
    return dict(grid=grid)


@auth.requires_membership('manager')
def upload():
    grid = SQLFORM.grid(db.download)
    return dict(grid=grid)


@auth.requires_membership('manager')
def approveusers():
    users = db(db.auth_user.registration_key == 'pending').select(db.auth_user.id,
                                                                  db.auth_user.first_name, db.auth_user.last_name,
                                                                  db.auth_user.email,
                                                                  db.auth_user.registration_key)

    return dict(users=users)


@auth.requires_membership('manager')
def zeroscores():
    users = db(db.auth_user.id > 0).select(db.auth_user.id, db.auth_user.numquestions,
                                           db.auth_user.score, db.auth_user.rating, db.auth_user.level,
                                           db.auth_user.numcorrect, db.auth_user.numwrong, db.auth_user.numpassed)

    for user in users:
        user.numquestions = 0
        user.score = 0
        user.rating = 1
        user.level = 1
        user.numcorrect = 0
        user.numwrong = 0
        user.numpassed = 0
        user.update_record()

    return dict(message='All scores reset to zero')


@auth.requires_membership('manager')
def clearquests():
    db.eventmap.truncate()
    db.userquestion.truncate()
    db.questagreement.truncate()
    db.questchallenge.truncate()
    db.questcomment.truncate()
    db.question.truncate()
    db(db.event.event_name != 'Unspecified').delete()
    return dict(message='All quests cleared')


@auth.requires_membership('manager')
def clearall():
    db.userquestion.truncate()
    db.questagreement.truncate()
    db.questurgency.truncate()
    db.questlink.truncate()
    db.questchallenge.truncate()
    db.questcomment.truncate()
    db.question.truncate()
    db.event.truncate()
    db.location.truncate()
    db.viewscope.truncate()
    db.subdivision.truncate()
    db.country.truncate()
    db.continent.truncate()
    db.scoring.truncate()
    #db.download.truncate()
    db.category.truncate()
    db.eventmap.truncate()
    db.website_parameters.truncate()

    return dict(message='Entire Database cleared out')


@auth.requires_login()
def datasetup():
    #This now needs reworked as some of the data needs to be creaed prior to the models execution
    #and so tables won't be empty - I think approach is to add all missing data which is slow
    #but effective will pull everything and then add the missing ones

    if db(db.category.id > 0).isempty():
        db.category.insert(cat_desc="None",
                           categorydesc="Set to select all questions")
        db.category.insert(cat_desc="Unspecified",
                           categorydesc="Catchall category")

    #setup the basic scopes that are to be in use and populate some default
    #continents, countrys and regions

    if db(db.scope.description == "1 Global").isempty():
        db.scope.insert(description="1 Global")
    if db(db.scope.description == "2 Continental").isempty():
        db.scope.insert(description="2 Continental")
    if db(db.scope.description == "3 National").isempty():
        db.scope.insert(description="3 National")
    if db(db.scope.description == "4 Local").isempty():
        db.scope.insert(description="4 Local")

    if db(db.continent.continent_name == "Unspecified").isempty():
        db.continent.insert(continent_name="Unspecified")

    if db(db.country.country_name == "Unspecified").isempty():
        db.country.insert(country_name="Unspecified", continent="Unspecified")

    settings.init = False
    return locals()


@auth.requires_login()
def init():
    #This function will be called to initialise the system the following 
    #activities are required here
    #1  Give the intial user manager role to admin the system
    #2  Populate the scoring table
    #3  Key in the subject of the database
    #4  Provide details of how to admin the system
    #5  Add a default category

    if db(db.website_parameters.id > 0).isempty():
        db.website_parameters.insert(shortdesc="This system should be used for any topic",
        longdesc='This system should be used for questions on any topic that you consider important to human progress')

    # Need to also ensure unspecified continent,region and country are present
    # think values will now be mandatory for new user registration

    #   Populate the scoring table
    scores = db(db.scoring.id > 0).select().first()

    if scores is None:
        for k in xrange(1, 30):
            db.scoring.insert(level=k, right=k * 10, wrong=k, rightchallenge=15 + (k * 10),
                              wrongchallenge=(5 + (k * 10)) * -1, rightaction=k * 5, wrongaction=k,
                              nextlevel=k * k * 20, submitter=k * 10)

        db.commit()

    # Update the first user to have manager access
    # Add an auth_group record of manager if it doesn't exist

    mgr = db(db.auth_group.role == 'manager').select().first()
    if mgr is None:
        mgr = auth.add_group('manager', 'The admin group for the app')
        time.sleep(2)  # for gae
        auth.add_membership(mgr, auth.user_id)

    # Think this will do and populate the website_parameters as well with redirect from the init
    # at present the initial user is the only manager as there shouldn't be much to
    # manage
    #datasetup()

    return locals()


@auth.requires_membership('manager')
def addstdcategories():
    categories = [["None", "Set to select all questions"], ["Unspecified", "Catchall category"], ["Water", "Water"],
                  ["Food", "Food"], ["Shelter", "Shelter"],
                  ["Healthcare", "Healthcare"], ["Freedom", "Freedom"], ["Fairness", "Fairness"], ["Fun", "Fun"],
                  ["Net Decision Making", "Net Decision Making"], ["Strategy", "Strategy"],
                  ["Organisation", "Organisation"], ["Education", "Education"], ["Philosophy", "Philosophy"]]

    for x in categories:
        if db(db.category.cat_desc == x[0]).isempty():
            db.category.insert(cat_desc=x[0], categorydesc=x[1])

    settings.init = False
    return locals()


@auth.requires_membership('manager')
def stdmessages():
    stdmsg = """You have been identified as a significant global leader either through a political or corporate leadership position, or due to having significant wealth or influence within a region.
We are frustrated at the lack of progress this planet appears to be making towards providing the majority of its inhabitants with longer happier lives.
 
A key issue we have identified is the lack of an agreed global strategy and we are proposing the adoption of a short term objective of getting global life expectancy to 80 by the year 2020. This can be considered to be our 2020 vision and can also be described as a re-definition of the 80/20 rule or pareto principal with which you may already be familiar. 

We will be holding you accountable to help drive this vision forward and make an active contribution to achieving this strategy.  In our eyes you are now accountable to the planet as a whole rather than just your current stakeholders or citizens.  We will be assessing how well you align your activities with our vision and we will be sending you reports periodically advising you of how well we assess you are performing.  We will also be setting up an on-line tracking system so other people can review and comment on our assessment of your performance.

As an added incentive to your participation in our vision it is proposed that we migrate entitlement to more advanced and expensive healthcare treatments which you may require in future towards those whose behaviour is well aligned with our strategy.  The precise eligibility criteria in future will depend on resource availability but you should be clear that evidence that you have failed to align your activities with the global strategy will not be helpful to your chances of being eligible for some of the advanced treatments which may become available.

Obviously at present we lack full credibility in this mission, however we will be building this up over the coming years.  The improvements in communication technology now make global crowdsourcing of strategy for planet earth a viable activity and we will be refining the strategy as more people come on board.  Our longer term aim is very much to make dying optional/reversible as eternal life seems to be a popular global concept and it seems many people would be interested in this if we could address some of the other inequalities of life at present.  

However eternal life for all poses some challenges and so we think it’s sensible to suggest that good behaviour rather than accumulated wealth will be the correct criteria for entitlement to longevity as it is theoretically possible for everybody to be well behaved, whereas it is presently impossible for everyone to be wealthy at the same time, and the competition for wealth is arguably the greatest blight on the world today.

Your time in power will be relatively fleeting – however our objective is to establish a system that can run the world for many years to come.  It will be built on the established technologies we have today and using them to empower the best people to make decisions that are right for the planet as a whole rather than the specific benefactors most closely associated with the decision maker.

We look forward to your help in making the world a better place."""

    actmsg = """You have been identified as responsible or partly responsible for an action identified as part of an initiative to develop a global strategy for the planet.

We are frustrated at the lack of progress this planet appears to be making towards providing the majority of its inhabitants with longer happier lives.
 
We look forward to your help in making the world a better place.  The specific action you have been tasked with supporting is:"""

    if db(db.message.msgtype == 'std').isempty():
        db.message.insert(msgtype='std', description='This is a general message without a specific action',
                          message_text=stdmsg)

    if db(db.message.msgtype == 'act').isempty():
        db.message.insert(msgtype='act', description='This is a message related to an  action',
                          message_text=actmsg)

    return locals()


@auth.requires_membership('manager')
def ajaxapprove():
    #This allows managers to approve pending registrations
    userid = request.args[0]
    upd = ''
    responsetext = 'User ' + str(userid) + ' has been approved'
    messagetxt = 'Your registration request has been approved'
    link = URL('default', 'index', scheme=True, host=True)
    footnote = 'You can now access the site at: ' + link
    if len(request.args) > 1:
        upd = 'denied'
        responsetext = 'User ' + str(userid) + ' has been denied access for now'
        messagetxt = 'Your registration request has been denied'
        footnote = 'A specific email will be sent to explain why or request more information'

    db(db.auth_user.id == userid).update(registration_key=upd)

    email = db(db.auth_user.id == userid).select(
        db.auth_user.email).first().email

    messagetxt = messagetxt + '\n' + footnote
    mail.send(to=email,
              subject='Networked Decision Making Registration Request',
              message=messagetxt)

    return responsetext
