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
# This file in particular borrows heavily from web2py appliance tiny website
#########################################################################

#Things to be initialized before main model

from os import path
import datetime


not_empty = IS_NOT_EMPTY()

db.define_table('website_parameters',
                Field('website_name_long', label=T('Website name long'), comment=T('Shown in the banner footer')),
                Field('website_name', label=T('Website name'), comment=T('Shown in top left logo')),
                Field('website_title', label=T('Website title'),
                      comment=T('Displayed instead of the banner if "with_banner"=False')),
                Field('website_subtitle', label=T('Website subtitle'), comment=T('Shown in the banner footer')),
                Field('website_url', label=T('Url'), comment=T('URL of the website')),
                Field('longdesc', 'text', label=T('Long Description'), comment=T('Subject of the website')),
                Field('shortdesc', label=T('Url'), comment=T('Short Description of the website')),
                Field('level1desc', label=T('Level1Desc'), comment=T('First Location Level')),
                Field('level2desc', label=T('Level2Desc'), comment=T('Second Location Level')),
                Field('level3desc', label=T('Level3Desc'), comment=T('Third Location Level')),
                Field('force_language', label=T('Force a language (en, it, es, fr, ...)')),
                Field('mailserver_url', label=T('Mail server url'),
                      comment=T('URL of the mailserver (used to send email in forms)')),
                Field('mailserver_port', 'integer', label=T('Mail server port'),
                      comment=T('Port of the mailserver (used to send email in forms)')),
                Field('mailserver_sender_mail', label=T('Mail server sender email'),
                      comment=T('Sender email adress of the mailserver (used to send email in forms)')),
                Field('mailserver_sender_login', label=T('Mail server sender login'),
                      comment=T('Login of the mailserver (used to send email in forms)')),
                Field('mailserver_sender_pass', label=T('Mail server sender pass'),
                      comment=T('Pass of the mailserver (used to send email in forms)')),
                Field('google_analytics_id', label=T('Google analytics id'),
                      comment=T('Your Google Analytics account ID')),
                Field('seo_website_title', label=T('SEO : Website title'),
                      comment=T('Displayed in <title> tag of the HTML source code')),
                Field('seo_meta_author', label=T('SEO : Meta "author"'),
                      comment=T('Displayed in <meta author> tag of the HTML source code')),
                Field('seo_meta_description', label=T('SEO : Meta "description"'),
                      comment=T('Displayed in <meta description> tag of the HTML source code')),
                Field('seo_meta_keywords', label=T('SEO : Meta "keywords"'),
                      comment=T('Displayed in <meta keywords> tag of the HTML source code')),
                Field('seo_meta_generator', label=T('SEO : Meta "generator"'),
                      comment=T('Displayed in <meta generator> tag of the HTML source code')),
                Field('quests_per_page', 'integer', default=20, label=T('Mail server port'),
                      comment=T('Port of the mailserver (used to send email in forms)')),
                Field('comments_per_page', 'integer', default=20, label=T('Mail server port'),
                      comment=T('Port of the mailserver (used to send email in forms)')))

db.website_parameters.website_url.requires = IS_EMPTY_OR(IS_URL())
db.website_parameters.mailserver_sender_mail.requires = IS_EMPTY_OR(IS_EMAIL())

db.define_table('category',
                Field('cat_desc', 'string', label='Category'),
                Field('categorydesc', 'text', label='Description'),
                format='%(cat_desc)s')

db.define_table('continent',
                Field('continent_name', 'string', label='Continent'),
                format='%(continent_name)s')

db.define_table('country',
                Field('country_name', 'string', label='Country'),
                Field('continent', 'string', label='Continent'),
                format='%(country_name)s')

db.define_table('subdivision',
                Field('subdiv_name', 'string', label='Sub-Division eg State, Province, County'),
                Field('country', 'string'),
                format='%(subdiv_name)s')

db.define_table('scope',
                Field('description', 'string'),
                format='%(description)s')

db.define_table('download',
                Field('title', unique=True),
                Field('file', 'upload'),
                Field('description', 'text'),
                Field('version', 'string', default='1'),
                format='%(title)s')

db.download.title.requires = IS_NOT_IN_DB(db, db.download.title)

db.define_table('scoring',
                Field('level', 'integer'),
                Field('right', 'integer'),
                Field('wrong', 'integer'),
                Field('rightchallenge', 'integer'),
                Field('wrongchallenge', 'integer'),
                Field('rightaction', 'integer'),
                Field('wrongaction', 'integer'),
                Field('nextlevel', 'integer'),
                Field('submitter', 'integer'),
                format='%(level)')


#location table is a holder for a group of events - it may be a physical place
#or virtual
db.define_table('location',
                Field('location_name', label='Location Name'),
                Field('address1', label='Address 1', writable=False, readable=False),
                Field('address2', label='Address 2', writable=False, readable=False),
                Field('address3', label='Address 3', writable=False, readable=False),
                Field('address4', label='Address 4', writable=False, readable=False),
                Field('addrcode', label='Postal Code', writable=False, readable=False),
                Field('addrurl', label='Location Website'),
                Field('continent', default='Unspecified', label='Continent'),
                Field('country', default='Unspecified', label='Country'),
                Field('subdivision', default='Unspecified', label='Subdivision'),
                Field('geox', 'double', default=0.0, label='Longitude', writable=False, readable=False),
                Field('geoy', 'double', default=0.0, label='Latitude', writable=False, readable=False),
                Field('description', 'text'),
                Field('shared', 'boolean', default=False, comment='Allows other users to link events'),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False, default=auth.user_id),
                Field('createdate', 'datetime', default=request.utcnow, writable=False, readable=False),
                format='%(location_name)s')


#db.location.linkable = Field.Virtual(
#    'linkable',
#    lambda row: row.shared or (row.auth_user == auth.user_id))

if settings.init is not True or settings.init is False:
    settings.continents = []
    continents = db(db.continent.id > 0).select(db.continent.continent_name)

    settings.continents = [x.continent_name for x in continents]

    if settings.continents is None:
        settings.continents = ['Unspecified']

    if db(db.location.location_name == "Unspecified").isempty():
        locid = db.location.insert(location_name="Unspecified",shared=True)


db.define_table('event',
                Field('event_name', label='Event Name', requires=not_empty),
                Field('locationid', 'reference location', label='Location',
                    default=db(db.location.location_name=='Unspecified').
                    select(db.location.id).first().id),
                Field('eventurl', label='Location Website'),
                Field('startdatetime', 'datetime', label='Start Date Time',
                      default=(request.utcnow + datetime.timedelta(days=10))),
                Field('enddatetime', 'datetime', label='End Date Time',
                      default=(request.utcnow + datetime.timedelta(days=11))),
                Field('description', 'text'),
                Field('shared', 'boolean', default=False, comment='Allows other users to link questions'),
                Field('owner', 'reference auth_user', writable=False, readable=False, default=auth.user_id,
                      label='Owner'),
                Field('createdate', 'datetime', default=request.utcnow, writable=False, readable=False),
                format='%(event_name)s')

#, default = db(db.location.locationname == 'Unspecified').select(db.location.id).first().id
#default = session.locationid??
#, default=db(db.location.location_name=='Unspecified').select(db.location.id,cache=(cache.ram,3600)).first().id

db.location.location_name.requires = [not_empty, IS_NOT_IN_DB(db, 'location.location_name')]
db.location.continent.requires = IS_IN_SET(settings.continents)
db.location.addrurl.requires = IS_EMPTY_OR(IS_URL())

db.event.eventurl.requires = IS_EMPTY_OR(IS_URL())
db.event.event_name.requires = IS_NOT_IN_DB(db, 'event.event_name')
db.event.startdatetime.requires = IS_DATETIME_IN_RANGE(format=T('%Y-%m-%d %H:%M:%S'),
                                                       minimum=datetime.datetime(2014, 6, 15, 00, 00),
                                                       maximum=datetime.datetime(2021, 12, 31, 23, 59),
                                                       error_message='must be YYYY-MM-DD HH:MM::SS!')
db.event.enddatetime.requires = IS_DATETIME_IN_RANGE(format=T('%Y-%m-%d %H:%M:%S'),
                                                     minimum=datetime.datetime(2014, 6, 15, 00, 00),
                                                     maximum=datetime.datetime(2021, 12, 31, 23, 59),
                                                     error_message='must be YYYY-MM-DD HH:MM::SS!')

#availevents = db((db.event.shared == True) | (db.event.owner==auth.user_id))
#availevents = db(db.event.id >1)
#db.question.event_name.requires = IS_IN_DB(db, 'event.event_name', _and=IS_IN_DB(availevents, 'event.name'))

#availevents = db((db.event.shared == True) | (db.event.owner==auth.user_id)).
#db.table.field.requires=IS_IN_DB(db(query),....)

# line below fails on gae so remove for now
#db.event.locationid.requires = IS_IN_DB(db((db.location.shared==True) | (db.location.auth_userid==auth.user_id)), 'location.id', '%(location_name)s')


## configure email
mail = auth.settings.mailer
mail.settings.server = 'gae'
mail.settings.sender = 'newglobalstrategy@gmail.com'
##mail.settings.login = 'username:password'

filename = 'private/emaillogin.key'
path = os.path.join(request.folder, filename)

if os.path.exists(path):
    mail.settings.login = open(path, 'r').read().strip()

##initialisation of things before main module
if settings.init is not True or settings.init is False:

    if db(db.event.event_name == "Unspecified").isempty():
        evid = db.event.insert(event_name="Unspecified", shared=True,
                               startdatetime=request.utcnow - datetime.timedelta(days=10),
                               enddatetime=request.utcnow - datetime.timedelta(days=9))
    settings.categories = []
    #categories= db(db.category.id>0).select(db.category.cat_desc, cache=(cache.ram,1200), cacheable=True).as_list()
    categories = db(db.category.id > 0).select(db.category.cat_desc)
    #for x in categories:
    #    settings.categories.append(x['cat_desc'])

    settings.categories = [x.cat_desc for x in categories]
    if len(settings.categories) == 0:
        settings.categories = ['None']

    settings.scopes = ['1 Global', '2 Continental', '3 National', '4 Local']
    settings.init == True


db.auth_user.exclude_categories.requires = IS_IN_SET(settings.categories, multiple=True)
#db.auth_user.exclude_categories.requires = IS_IN_DB(db, 'category.cat_desc', cache=(cache.ram,3600),multiple=True)
db.auth_user.continent.requires = IS_IN_SET(settings.continents)

mail = None
WEBSITE_PARAMETERS = db(db.website_parameters).select().first()

if WEBSITE_PARAMETERS:
    if WEBSITE_PARAMETERS.mailserver_url and WEBSITE_PARAMETERS.mailserver_port:
        ## configure email
        mail = auth.settings.mailer
        mail.settings.server = '%s:%s' % (WEBSITE_PARAMETERS.mailserver_url, WEBSITE_PARAMETERS.mailserver_port)
        mail.settings.sender = WEBSITE_PARAMETERS.mailserver_sender_mail
        mail.settings.login = '%s:%s' % (
            WEBSITE_PARAMETERS.mailserver_sender_login, WEBSITE_PARAMETERS.mailserver_sender_pass)

    ## your http://google.com/analytics id
    response.google_analytics_id = None if request.is_local else WEBSITE_PARAMETERS.google_analytics_id
    response.subtitle = WEBSITE_PARAMETERS.website_name

    if WEBSITE_PARAMETERS.force_language:
        T.force(WEBSITE_PARAMETERS.force_language)


def userinit():
    """
    This initialises user variables into the session. These are used to save
    settings for view and the likes ie short term storage of defaults without
    changing the auth values
    """

    session.userid = auth.user
    session.continent = auth.user.continent
    session.country = auth.user.country
    session.subdivision = auth.user.subdivision
    session.level = auth.user.level

    return

#setup session variables for the user if logged in and not setup
#probably these should be elsewhere but lets leave here for now
if session.userinit is None and auth.user:
    #establish session variables for user
    userinit()
    session.userinit = True
