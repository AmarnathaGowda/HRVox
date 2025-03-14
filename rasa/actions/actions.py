
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2
import requests


import logging
logger = logging.getLogger(__name__)
logger.info("Loading actions.py")

DB_CONFIG = {
    'dbname': 'hrvox_db',
    'user': 'hrvox_user',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

class ActionGetPolicy(Action):
    def name(self):
        logger.info("ActionGetPolicy.name() called")
        return "action_get_policy"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
       
        policy_type = tracker.get_slot("policy_type") or "general"

        policy_data = {
            "leave_policy": "You are entitled to 20 days of leave per year.",
            "sick_leave": "Sick leave is granted based on medical certification.",
            "general": "Sick leave is granted based on medical certification.You are entitled to 20 days of leave per year.",
            "policy_type": "You are entitled to 20 days of leave per year."
        }

        logger.info(policy_data)
        logger.info(tracker)

        policy_type = tracker.get_slot("policy_type") or "general"
        
        logger.info(f"Debug: policy_type = {policy_type}")

        if policy_type is None:
            dispatcher.utter_message(text="Which policy would you like to know about?")
        else:
            response = policy_data.get(policy_type, "Policy not found.")
            dispatcher.utter_message(text=f"The policy is: {response}")

        
        # try:
        #     # Connect to the database
        #     conn = psycopg2.connect(**DB_CONFIG)
        #     cursor = conn.cursor()
        #     logger.info("policy_type")
        #     logger.info(policy_type)

        #     logger.info("SELECT policy_text FROM hr_policies WHERE policy_type = %s", (policy_type,))
        #     # Query the policy

        #     cursor.execute("SELECT policy_text FROM hr_policies WHERE policy_type = %s", (policy_type,))
        #     result = cursor.fetchone()
        #     if result:
        #         response = result[0]
        #     else:
        #         response = "Policy not found."
        #     # Close the connection
        #     cursor.close()
        #     conn.close()
        # except Exception as e:
        #     response = f"Error retrieving policy: {str(e)}"
        # # Send the response
        # dispatcher.utter_message(text=response)
        
        # # dispatcher.utter_message(text=response)
        # return []

    # def run(self, dispatcher, tracker, domain):
    #     print("Loading actions.py -- action_get_policy")
    #     dispatcher.utter_message(text="Fetching policy details...")
    #     return []
    
class ActionApplyLeave(Action):
    def name(self):
        return "action_apply_leave"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        # Mock API call (replace with actual API endpoint)
        leave_dates = tracker.get_slot("leave_dates") or "unspecified"
        response = requests.post("https://mock-leave-api.com/apply", data={"dates": leave_dates})

        response.status_code = 200
        if response.status_code == 200:
            dispatcher.utter_message(text="Your leave request has been submitted successfully. Your current avilable balance is 19")
        else:
            dispatcher.utter_message(text="There was an issue submitting your leave request.")
        return []