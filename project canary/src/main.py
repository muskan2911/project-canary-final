from agents.type_classifier_agent import TypeClassifierAgent
from agents.product_classifier_agent import ProductClassifierAgent
from agents.sentimental_classifier_agent import SentimentalClassifierAgent
from agents.case_grouping_agent import CaseGroupingAgent
from utils.BigQueryWriteUtil import BigQueryWriteUtil
import json

if __name__ == "__main__":
    TypeAgent = TypeClassifierAgent(project_id="sab-dev-nghp-jobs-4063")
    ProductAgent = ProductClassifierAgent(project_id="sab-dev-nghp-jobs-4063")
    SentimentalAgent = SentimentalClassifierAgent(project_id="sab-dev-nghp-jobs-4063")
    CaseGroupingAgent = CaseGroupingAgent(project_id="sab-dev-nghp-jobs-4063")

    sample_case = [{
        "id": "500Uo00000Spi6vIAB",
        "name": "1000 MILE TRAVEL GROUP",
        "description": "Sabre Red 360  Topic Price or search fares  Subtopic     Hi Sabre     We have been advised by our Qantas Rep to contact you regarding fare loading for the QF Wholesale Fare   Attached is an example of the fare loaded in PCC V1G9 showing code UQW however in PCC PP3K the same fare is not showing     See remarks from the QF rep below    We have checked and confirm that both sabre PCCs PP3KV1G9 are filed correctly If V1G9 can access fares then PP3K should also be able to access because both are filed correctly I would suggest you check with Sabre     Thank you Tenneale",
        "customer": "1000 MILE TRAVEL GROUP",
        "emails": "abre Support Team This is an automated message Dear Valued Customer Thank you for contacting Sabre Support Team We appreciate the opportunity to serve your business needs and will answer your query as soon as possible We have opened a case 08714936 for your request Thank you very much Sabre Support Team",
        "priority": "Medium",
        "status":"Open",
        "created_date":"2025-08-26 15:28:23.133598 UTC"
    },
    {
        "id": "500Uo00000S0A4KIAV",
        "name": "10117552 CANADA INC",
        "description": "Hi Team 5JML reports issues with KL   1st wash codejavaMARKET DUB DEL CXRFLTDEPDATE ARRDATE BRDOFFSCORETAI  1KL113411Oct055511Oct0830DUBAMS50 0 AVSRC0DCACACHEAVS6 J9 C9 D9 I9 Z0 O0 Y9 B9 M9 P9 U9 F9 K0 W9 H9 S9 L9 A9 Q9 T9 E9 N9 R9 V9 X9 G9  2KL 87711Oct120012Oct0015AMSBOM50 0 AVSRC0DCACACHEAVS6 J9 C9 D0 I0 Z0 O0 W9 S9 A0 Y9 B9 M9 U9 K9 H9 L9 Q9 T9 E9 N9 R9 V0 X0 G0  3KL364912Oct050012Oct0705BOMDEL50 0 AVSRC0DCACACHEAVS6 J0 C0 D0 I0 Z0 O0 Y9 B9 M9 U9 K9 H9 L9 Q9 T9 E9 N9 R9 V9 X9 KL 1134KL 0877KL 3649code 505 codejava  GETSPECIFIC  OK  GCPUSCENTRAL1PRODDCA  PARTITIONID21  ZONEIDC  HOST101433827  61321  SOLUTION	 DUBDELKL3SEGONL20251011DUBAMS1134KLAMSBOM877KLBOMDEL3649KL  SEGMENT	 DUBAMSKL1134202510110555202510110830  RESPONSE	  NOT FOUND  code Its another scenario where it jumped to AVS because DCACACHE returned NOT FOUND As our customer is filtering through Revalidate were not able to obtain impact metrics from the TDW Dashboard Would you advise to have KL traffic moved to 2nd wash or is there some magic that you could do from your side to keep this CACHE better updated Thank you",
        "customer": "10117552 CANADA INC",
        "emails": "Sabre Support Team This is an automated message Dear Valued Customer Thank you for contacting Sabre Support Team We appreciate the opportunity to serve your business needs and will answer your query as soon as possible We have opened a case 08691267 for your request Thank you very much Sabre Support Team",
        "priority": "Medium",
        "status":"In Progress",
        "created_date":"2025-10-24 15:28:23.133598 UTC"
    },
	 {
        "id": "500Uo00000KJ803IAD",
        "name": "AA CORP TVL SVC",
        "description": "Sabre Red 360  Topic Sabre Profile  Subtopic Create  Modify a profile    Hello   We have issues if we click Edit on a Sabre profile on the Sabre sideIf updating a traveler profile it duplicates the Associated profiles which causes error responses when copying the profile overThere are no issues if we use AdminSabre Profiles tab to editI have attached a document with screen shots    Let me know if you have any questions    Thanks  Barb",
        "customer": "AAA CORP TVL SVC",
        "emails": "Sabre Support Team This is an automated message Dear Valued Customer Thank you for contacting Sabre Support Team We appreciate the opportunity to serve your business needs and will answer your query as soon as possible We have opened a case 08366857 for your request Thank you very much Sabre Support Team",
        "priority": "Medium",
        "status":"In Progress",
        "created_date":"2025-10-24 15:28:23.133598 UTC"
    },
	 {
        "id": "500Uo00000KJ803IAD",
        "name": "AA CORP TVL SVC",
        "description": "10117552 CANADA INC",
        "customer": "1 Customer Environment  Production or CVT PROD 2 Detailed description of the problem Group Wizard Incompatible with Java 17 3 Step by step on how the problem can be reproduced Asign Group wizard 181202503122123 last published version to an EPR with JAVA17 Open Sabre Red 360 Open Group Wizard from the application side panel ERROR Message Please Sign in to Sabre and relaunch Group Wizard If the EPR is downgraded to JAVA 8 the issue is prevented 4 The current Result Group wizard panel fails to load successfully in the webkit panel JAVA 17 5 Expected Result Group wizard panel load successfully in the webkit panel with JAVA 17 6 Document the Defects in a word template as attachment if you take screen shots screenshots and diagnostic logs attached 7 Reproduced in  EnvironmentVersionDatabase 255",
        "emails": "Hi Crystal We received reports from a JAVA 17 tester in PROD that Group Wizard might have compatibility issues with that Java version causing the error in the screenshot Have you received this report too We opened a JIRA ticket for this with the SDK team as the migration to JAVA17 is around the corner but we need to know if you and Michael are aware of this or if your developer is working on this Cheers Mauricio Fuentes Technical Product Support Analyst III Montevideo  LAC Together we make travel happen ref00D150GKhq500Uo0Pd8ydref",
        "priority": "Medium",
        "status":"In Progress",
        "created_date":"2025-10-24 15:28:23.133598 UTC"
    },
	 {
        "id": "500Uo00000Pd8ydIAB",
        "name": "AA CORP TVL SVC",
        "description": "1 Customer Environment  Production or CVT PROD 2 Detailed description of the problem Group Wizard Incompatible with Java 17 3 Step by step on how the problem can be reproduced Asign Group wizard 181202503122123 last published version to an EPR with JAVA17 Open Sabre Red 360 Open Group Wizard from the application side panel ERROR Message Please Sign in to Sabre and relaunch Group Wizard If the EPR is downgraded to JAVA 8 the issue is prevented 4 The current Result Group wizard panel fails to load successfully in the webkit panel JAVA 17 5 Expected Result Group wizard panel load successfully in the webkit panel with JAVA 17 6 Document the Defects in a word template as attachment if you take screen shots screenshots and diagnostic logs attached 7 Reproduced in  EnvironmentVersionDatabase 255",
        "customer": "AAA CORP TVL SVC",
        "emails": "EXTERNAL Email Notification Treat content with extra caution TO REPORT PHISHING Click the Report Phish icon in the Outlook toolbar  Hi team  Just to clarify  the Group Wizard currently running in PROD is built on Java 8 The Java 17 version of Group Wizard is still undergoing testing in the CERT environment Well keep you informed if any compatibility issues are identified during this phase Best regards Michael From scmsupportsabrecom scmsupportsabrecom Sent Friday June 20 2025 714 PM To crystaldunklesabrecom Cc SabreRed3rdLevelSupportsabrecom Michael Shwarts MichaelShwartslognetsystemscom Subject groupwizard Incompatibility with Java 17 08603088  ref00D150GKhq500Uo0Pd8ydref  Hi Crystal We received reports from a JAVA 17 tester in PROD that Group Wizard might have compatibility issues with that Java version causing the error in the screenshot Have you received this report too We opened a JIRA ticket for this with the SDK team as the migration to JAVA17 is around the corner but we need to know if you and Michael are aware of this or if your developer is working on this cidimage001png01DBE36A8A472B00 Cheers Mauricio Fuentes Technical Product Support Analyst III Montevideo  LAC Together we make travel happenhttpsurldefenseproofpointcomv2urluhttps3AsabremysalesforcecomservletservletImageServer3Foid3D00D15000000GKhq26esid3D018Uo00000Im5uL26from3DextdDwIGaQcFXJfUb1oWgygD0uNzujnAriv0FrzFakBkYGfmIYTgCEd5JSPUGOzoe7cQ1Mq4mNngPYUmNGWyVRNpXLS6w8yjBdbY1JkNkRv3u8xZOzTrGLY6AqX8oBKOBu3bKds2PM64qhPrCziTM8pLyi6iHLiRs7AWvd1vzGfpMKkXZQe  ref00D150GKhq500Uo0Pd8ydref",
        "priority": "Medium",
        "status":"In Progress",
        "created_date":"2025-10-24 15:28:23.133598 UTC"
    }
]

    track_messages = [
        {"message":"Hilton","id":"TRACK-001"},
        {"message":" Fare for PCC V1G9 ","id":"T678"},
        {"message":"BCD","id":"TRACK-002"},
        {"message":"BCD/Marriott","id":"TRACK-004"}
    ]

    type_agent_output = TypeAgent.classify(sample_case)
    product_agent_output = ProductAgent.classify(sample_case)
    sentimental_agent_output = SentimentalAgent.classify(sample_case,track_messages)
    case_grouping_agent_output = CaseGroupingAgent.classify(sample_case)
    case_to_track_id_mapping = SentimentalAgent.caseToTrackId(sample_case,track_messages)
    case_to_track_id_mapping = SentimentalAgent.caseToTrackId(sample_case,track_messages)
    case_root_cause_mapping = SentimentalAgent.getRootCause(sample_case,track_messages)

    print("Type:", type_agent_output)
    print("Product:", product_agent_output)
    print("Priority:", sentimental_agent_output)
    print("Grouping:", case_grouping_agent_output)
    print("Tracking", case_to_track_id_mapping)
    print("Root Caue", case_root_cause_mapping)
    BigQueryWriteUtil.insert(sample_case,json.loads(type_agent_output),json.loads(product_agent_output),json.loads(sentimental_agent_output),json.loads(case_grouping_agent_output),json.loads(case_to_track_id_mapping),json.loads(case_root_cause_mapping))
