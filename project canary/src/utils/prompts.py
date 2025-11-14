
PRODUCT_CLASSIFICATION_PROMPT = """
You are a product classification agent.
Given the case details, identify which PRODUCT the issue is related to.

Allowed outputs (exactly one word, lowercase):
air
hotel
cars
rail

Return only ONE WORD with no explanation.

If it has to do with any process during air travel - say "air" - eg: check-in, baggage, lounge, security, etc etc
If it has to do with any process during hotel stay - say "hotel" - eg: reservation, check-in hotel, check-out, stay, no of nights, etc etc
Similarly for cars and rail.


Case Info:
Case ID: {case_id}
Name: {case_name}
Description: {case_description}
Customer Info: {case_customer_info}
Emails: {case_emails}
Priority: {customer_priority}
"""

TYPE_CLASSIFICATION_PROMPT = """
You are a classification agent.
Given case details, classify the case as Incident or Inquiry.

Incident = service disruption / product malfunction / urgent issues
Inquiry  = information request / explanation / non-urgent task

Return only one word: Incident or Inquiry.

Case Info:
Case ID: {case_id}
Name: {case_name}
Description: {case_description}
Customer Info: {case_customer_info}
Emails: {case_emails}
Priority: {customer_priority}
"""