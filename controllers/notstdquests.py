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

#This adds std questions and actionsto the database - only run this if you are 
#looking to test a std system or have some desire to reperform the demo questions in a different environment
#so coding of this is awful think we need a list and then iterate through - but different questions have different params
#and now got the challenge of setting up the links as well and needs to work on gae so a bit more than just looping through
#but probably can create a new list as we go of the questids inserted and then create the questlink table from that somehow
#need the list of links in a table and just map to the questids actually generated


@auth.requires_membership('manager')
def stdquest():
    #still got most of this to populate but probably look at the links piece next
    #think we just need a list of questionids which are appended whenever we have a question even if for some reason already in there
    
    stdquests = [{'questiontext':r'Should we develop a global strategy as outlined at: http://www.ted.com/talks/        jamie_drummond_how_to_set_goals_for_the_world.html ?','answers':["Yes","No"],'urgency':6,'importance':8, 'category':'Strategy'},
{'questiontext':r'Is it possible to live for more than 130 years?','answers':["Yes","No"],'urgency':4,'importance':6, 'category':'Healthcare'},
{'questiontext':r'Do we know if nothing is a stable state?','numanswers':3,'answers':["Yes","No","We don't know we just assume it is"],'urgency':3,'importance':6, 'category':'Philosophy'},
{'questiontext':r'Is it reasonable to try and promote biogerontology research?','answers':["Yes","No"],'urgency':6,'importance':6, 'category':'Healthcare'},
{'questiontext':r'Is there sufficient education on when to compete and when to co-operate?','answers':["Yes","No"],'urgency':4,'importance':8, 'category':'Strategy'},
{'questiontext':r'Are you aware of the global strategy?','answers':["Yes","No"],'urgency':7,'importance':7, 'category':'Strategy'},
{'questiontext':r'Did you choose where you were born?','answers':["Yes","No"],'urgency':4,'importance':4, 'category':'Philosophy'},
{'questiontext':r'Is it right that place of birth determines so much of your life and restricts so many people?','answers':["Yes","No"],'urgency':4,'importance':7, 'category':'Philosophy'},
{'questiontext':r'Do we need to localise decision making?','answers':["Yes","No"],'urgency':6,'importance':8, 'category':'Organisation'},
{'questiontext':r'Could we unite theists and atheists on a project to create heaven on earth?','answers':["Yes","No"],'urgency':7,'importance':7, 'category':'Philosophy'},
{'questiontext':r'What is the optimum number of countries in the world?','answers':["Just right", "Too many","Too few","One"],'urgency':5,'importance':8, 'category':'Organisation'},
{'questiontext':r'What are the best solutions to work on right now?','numanswers':5,'answers':["Prevention of HIV/Aids", "Networked Decision Making","Malaria","Malnutrition","Global Warming"],'urgency':8,'importance':8, 'category':'Strategy'},
{'questiontext':r'Is the world under-achieving?','answers':["Yes","No"],'urgency':7,'importance':7, 'category':'Organisation'},
{'questiontext':r'What is the main problem with the world right now?','numanswers':6,'answers':["There is no problem - everything is perfect","There simply isn't enough food in the world so some people have to starve","Many people don't care if other people are starving","Humans lack the skills to organise the planet","Humans derive pleasure from having more than other people","Lack of vision to see that creating alignment on objectives will get us all much better futures and longer and happier lives"],'urgency':7,'importance':8, 'category':'Strategy'},
{'questiontext':r'Does God Exist?','answers':["Yes","No"],'urgency':3,'importance':7, 'category':'Philosophy'},
{'questiontext':r'Is God rational?','answers':["Yes","No"],'urgency':5,'importance':7, 'category':'Philosophy'},
{'questiontext':r'Is it rational to believe in an irrational God?','answers':["Yes","No"],'urgency':6,'importance':7, 'category':'Philosophy'},
{'questiontext':r'Is aging a disease or is it just inevitable and we should accept it?','answers':["A disease","Inevitable"],'urgency':4,'importance':7, 'category':'Healthcare'},
{'questiontext':r'Do countries assist or hinder the operation of the world?','answers':["Assist","Hinder"],'urgency':6,'importance':7, 'category':'Organisation'},
{'questiontext':r'Why are so many people unemployed?','numanswers':5,'answers':["The unemployed are all useless", "Just a cost of human progress that many are left with lots of leisure but little income","Inability to co-operate, share and work together","Many people are just lazy","Something else"],'urgency':8,'importance':7, 'category':'Organisation'},
{'questiontext':r'Did JFK speed-up or slow down progress in getting to the moon by explaining that was the intention in 1962  http://www.astrosociology.com/Library/PDF/JFK%201962%20Rice%20University%20Speech%20Transcript.pdf ?','answers':["Speed Up","Slow Down"],'urgency':7,'importance':7, 'category':'Organisation'},
{'questiontext':r"If stating we were going to the moon was important to getting there is there not a similarly strong case for saying we are going to extend human lifespans?",'answers':["Yes","No"],'urgency':7,'importance':7, 'category':'Organisation'},
{'questiontext':r'Should Scotland become an independent country?','answers':["Yes","No"],'urgency':4,'importance':7, 'category':'Organisation','continent':'Europe (EU)','country':'United Kingdom (EU)','activescope':'3 National'},
{'questiontext':r'Should we develop social network integration features for networked decision making?','answers':["Yes","No"],'urgency':4,'importance':7, 'category':'Net Decision Making'},
{'questiontext':r'Which social networking platform should be developed first?','numanswers':4,'answers':["Facebook","Twitter","Google+","Other"],'urgency':4,'importance':7, 'category':'Net Decision Making'},
{'questiontext':r'Should we look to use advertising to fund the running costs of NDS?','answers':["Yes","No"],'urgency':4,'importance':7, 'category':'Net Decision Making'},
{'questiontext':r'Is the United States a corruption as alleged at http://www.ted.com/talks/lawrence_lessig_we_the_people_and_the_republic_we_must_reclaim.html ?','answers':["Yes","No"],'urgency':7,'importance':7, 'category':'Organisation', 'continent':'North America (NA)','country':'United States (NA)','activescope':'3 National'},
{'questiontext':r'The distribution of wealth on the planet is radically different than that predicted by micro-economic theory.  The question therefore arises does acquisition of great wealth require exploitation of others?','numanswers':3,'answers':["Yes","No","Usually"],'urgency':4,'importance':4, 'category':'Strategy'},
{'qtype':'action','questiontext':r'Unless they have already done so, all global citizens with net assets in excess of US$100 million should invest 1% of their assets in biogerontology or related research and action. Eg The Gates Foundation activities and Ellison medical would both count so several leading individuals have done this already.','numanswers':2,'answers':['Approve','Disapprove','OK'],'urgency':8,'importance':8, 'category':'Healthcare','responsible':'people with >$100M'},
{'qtype':'action','questiontext':r'Daylight saving time should operate all year in Europe to reduce accidents and CO2 emissions','numanswers':2,'answers':['Approve','Disapprove','OK'],'urgency':8,'importance':9, 'category':'Organisation','responsible':'Jose Manuel Barroso','continent':'Europe (EU)','activescope':'2 Continental'},
{'qtype':'action','questiontext':r'The funding model for US politics must change','numanswers':2,'answers':['Approve','Disapprove','OK'],'urgency':8,'importance':9, 'category':'Organisation','responsible':'Barrack Obama','continent':'North America (NA)','country':'United States (NA)','activescope':'3 National'},
{'qtype':'action','questiontext':r'All African health centres and schools should get internet access to improve access and trust in the global knowledge base, this should be provided by leading pharmaceutical and technology companies working together','numanswers':2,'answers':['Approve','Disapprove','OK'],'urgency':5,'importance':9, 'category':'Healthcare','responsible':'CEOs of leading pharma & IT Companies','continent':'Africa (AF)','activescope':'2 Continental'},
{'qtype':'action','questiontext':r'A national solution to the problem of misfuelling cars with petrol instead of diesel should be establised in the UK the costs of this problem are  estimated at around $120M per year and magnets, RFID readers on fuel pumps, better fuel caps or some other agreed approach should be able to permanently eliminate this waste for less than half that cost','numanswers':2,'answers':['Approve','Disapprove','OK'],'urgency':5,'importance':6, 'category':'Organisation','responsible':'CEOs of leading Auto & Oil Companies','continent':'Europe (EU)','country':'United Kingdom (EU)','activescope':'3 National'},
{'qtype':'action','questiontext':r'The programme to deliver better housing as explained at http://www.ted.com/talks/paul_pholeros_how_to_reduce_poverty_fix_homes.html should be rolled out globally with associated crowdsourced measurement of progress.','numanswers':2,'answers':['Approve','Disapprove','OK'],'urgency':8,'importance':9, 'category':'Healthcare','responsible':'All global leaders'},
{'qtype':'action','questiontext':r'Google should develop a globally scaleable version of the network decision making system outlined here','numanswers':2,'answers':['Approve','Disapprove','OK'],'urgency':7,'importance':7, 'category':'Net Decision Making','responsible':'Eric Schmidt'},
{'qtype':'action','questiontext':r'The top priority action from the 2012 Copenhagen Consensus (http://copenhagenconsensus.com) to use bundled micronutrient interventions to fight hunger and improve education should be actioned and funded by a $75bn cut to US defence spending','numanswers':2,'answers':['Approve','Disapprove','OK'],'urgency':8,'importance':9, 'category':'Food','responsible':'Barrack Obama'}]


    #link micronutrient to copenhagen consensus

    insertlist = []
    for x in stdquests:
        qtext = x['questiontext']
        q=0
        if not request.env.web2py_runtime_gae:
            if db(db.question.questiontext == qtext).isempty():
                q = db.question.insert(**x)
        else:
            q = db.question.insert(**x)
        insertlist.append(q)
    #have assumed id of first action is 28 - this needs checked    
    stdlinks = [[4,0],[6,7],[15,16],[20,21],[23,24],[26,30],[11,27]]

    #then if we have inserted those questions we would create related link
    #
    for x in stdlinks:
        source_id = insertlist[x[0]]
        target_id = insertlist[x[1]]
        if source_id > 0 and target_id > 0:
            if db(db.questlink.sourceid == source_id and db.questlink.targetid == target_id).isempty():
                db.questlink.insert(sourceid=source_id,targetid=target_id, createcount=1, deletecount=0)
        
    return locals()




