# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []



from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2
import requests


import logging
logger = logging.getLogger(__name__)
logger.info("Loading actions.py")

class ActionGetPolicy(Action):
    def name(self):
        logger.info("ActionGetPolicy.name() called")
        return "action_get_policy"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        logger.info("ActionGetPolicy.run() called b")
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
      
        
        # dispatcher.utter_message(text=response)
        return []

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