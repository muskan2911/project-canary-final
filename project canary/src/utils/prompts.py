CASE_ROOT_CAUSE_PROMPT = """
You are a case root cause  finding agent.
There are multiple cases. For each case do the following 
Given the case details, identify the cause of the issue.  
Look at email as well. It could be multiple email in one case.


Allowed output for each case give output in following format Case Id -> Case Root Cause (Root cause would be lowercase):
api issue
price issue
supplier issue
missing fare access
Return the output as map with key as Case Id and value as Case Root Cause.

Case Info:
Cases: {cases}


Track Message:
Track Messages : {track_messages}
"""

CASE_GROUPING_PROMPT = """
You are a case grouping agent.
There are multiple cases. For each case do the following 
Given the case details, identify the case which are similar based on case description and email message.


Allowed output for each case give output in following format case id -> list of case id which are similar. Dont give explanation.
IF there are no similar case, give in following format case id -> NONE

Return the output as map with key as Case Id and value as list of Case Id which are similar.

Case Info:
Cases: {cases}
"""

CASE_TO_TRACKING_ID_PROMPT = """
You are a sentimental finding agent.
There are multiple cases. For each case do the following 
Given the case details, identify the track id  of the issue. A case could be linked to multiple track id or no track id.
Look at email. It could be multiple email in one case.


Allowed output for each case give output in following format Case Id -> Track Id. Track Id would be coming from track messages
Return the output as map with key as Case Id and value as Track Id
IF there are no  track id, give in following format case id -> NONE

Following scenario are high priority cases
1. Traveller is impacted 
2. High volume of cases and email where shopping or booking is impacted
3. Hotel, Air, Car Supplier system are down  completely
4. If the case description or email message matches Track Messages. Track Message is array so match against multiple 

Following scenario are medium priority cases
1. Very few shopping or booking are failing.
2. Customer is not able to use sabre system for technical reason

Following scenario are low priority cases
1. Inquiry case such as How to use the system?



Case Info:
Cases: {cases}


Track Message:
Track Messages : {track_messages}
"""

SENTIMENT_CLASSIFICATION_PROMPT = """
You are a sentimental finding agent.
There are multiple cases. For each case do the following 
Given the case details, identify the sentiment of the issue. Sentiment could be High Medium Low Priority case. 
Look at email. It could be multiple email in one case.


Allowed output for each case give output in following format Case Id -> Case Priority (Prioroty would be exactly one word, lowercase):
high
medium
low
Return the output as map with key as Case Id and value as Case Priority.
Also return the 

Following scenario are high priority cases
1. Traveller is impacted 
2. High volume of cases and email where shopping or booking is impacted
3. Hotel, Air, Car Supplier system are down  completely
4. If the case description or email message matches Track Messages. Track Message is array so match against multiple 

Following scenario are medium priority cases
1. Very few shopping or booking are failing.
2. Customer is not able to use sabre system for technical reason

Following scenario are low priority cases
1. Inquiry case such as How to use the system?



Case Info:
Cases: {cases}


Track Message:
Track Messages : {track_messages}
"""

PRODUCT_CLASSIFICATION_PROMPT = """
You are a product classification agent.
There are multiple cases. For each case do the following 
Given the case details, identify which PRODUCT the issue is related to.

Allowed output for each case give output in following format Case Id -> Case Product(Product would be exactly one word, lowercase)
air
hotel
cars
rail

Return the output as map with key as Case Id and value as Case Product.


Return only ONE WORD with no explanation.

If it has to do with any process during air travel - say "air" - eg: check-in, baggage, lounge, security, etc etc
If it has to do with any process during hotel stay - say "hotel" - eg: reservation, check-in hotel, check-out, stay, no of nights,LR(Lodging Retailer) etc etc
Similarly for cars and rail.



Case Info:
Cases: {cases}
"""

TYPE_CLASSIFICATION_PROMPT = """
You are a classification agent.
There are multiple cases. For each case do the following 
Given case details, classify the case as Incident or Inquiry.

Incident = service disruption / product malfunction / urgent issues
Inquiry  = information request / explanation / non-urgent task

Allowed output for each case give output in following format Case Id -> Case Type (Type would be exactly one word, lowercase)
incident
inquiry

Return the output as map

Case Info:
Cases: {cases}
"""
