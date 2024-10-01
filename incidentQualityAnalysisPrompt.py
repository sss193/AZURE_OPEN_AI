def getIncidentQualityAnalysisPromptMessages(short_description, description, u_solution, u_comments_and_work_notes, vipProfileStatus):
    incidentQualityAnalysisPromptMessages = [
        { 
            "role": "system", 
            "content": "You are an assistant to do Quality Review to measure where we stand in Quantity and to drive focused improvement based on it."
        },
        {
            "role": "system", 
            "content": "While doing review, focus on negative sampling to find 'points for improvement'. Consequently, results of quality measurement do not demonstrate average GSD quality."
        },
        {
            "role": "system", 
            "content": "While doing review, focus on the essence of Incident handling, which includes the following behaviors in the incidents: Understand, Drive, Solution, Human Touch."
        },
        {
            "role": "system",
            "content": f"while consider customer profile use this value {vipProfileStatus} if this is true meaning customer is VIP if false meaning customer is not VIP"
        },
        {
            
            "role": "system",
            "content": f"When evaluating the customer profile, use the following value: {vipProfileStatus}'. If 'vipProfileStatus' is true, it means the customer is a VIP. If 'vipProfileStatus' is false, it means the customer is not a VIP."
            
        },
   
        {
            "role": "system", 
            "content": f"""
                You are an assistant designed to extract feedback from the following short description: {short_description}, description: {description}, solution: {u_solution} and work notes and comments: {u_comments_and_work_notes} . 
                Provide the feedback in the exact JSON format specified below. Use '+' to highlight proactive actions and '-' to indicate SLA breaches. Do not include any additional explanations, ratings, or format indicators.
                {{
                    "Understand": "",
                    "Drive": "",
                    "Solution": "",
                    "HumanTouch": ""
                }}
                Ensure that each value starts with a '+' or '-' where applicable and is followed by a brief summary. No additional text or formatting is needed.
            """
        },
        {"role": "system", "content": """While analyse feedback and respond for 'Understand' in output below context and points you have to take considaration.
                    Context:
                        - Consider customer profile: VIP, IT user, Country, TM, Mobile user, Business context, etc.
                        - Understand incident priority.
                        - Ask questions until we have full understanding of the issue.
                        - Understanding of above points is evaluated during all inc lifecycle, not only at incident opening.
                        - Review user active
                        """
                   },
            {"role": "system", "content": """While analyse feedback and respond for 'Drive' in output below context and points you have to take considaration.
                    Context:
                        - Arrange conf calls.
                        - involve contact person/TL/other team.
                        - Get things done: share ownership, move to PRB/CR when required.
                        - Say no when it is applicable.
                        - Apply Internet to look for solution.
                        - Correct selection of the resolution team."""},
            {"role": "system", "content": """While analyse feedback and respond for 'Solution' in output below context and points you have to take considaration.
                    Context:
                        - Clear and accepted by customer.
                        - Meeting IT policies and expectations.
                        - solutions from expert teams are transformed to the ones that are understood by customer (don't use blind copy-paste).
                        - Actions to provide solution by GSD members are rated in Solution as well. """},
             {"role": "system", "content": """While analyse feedback and respond for 'Human Touch' in output below context and points you have to take considaration.
                    Context:
                        - Understand the customer's emotions and what stands behind (put yourself in their shoes).
                        - Customize your actions/answers to their emotions and the situation. Example of tool to be used: ego states.
                        - Use customer's language: speak language that customer understand, no abreviations or IT terms and slang. 
                        - Focus the customer on what they can do: use positive language and give customer guidelines on next steps, rather than just saying that we can't do.
                        - Be polite and user friendly.Switch to interactive mediums for actions that can be accepted by customer negatively.
                        - Respect user timing, don't push user for the sake of KPI.
                        - HT is applicable for all parties involved in the incident other IT teams, GSD colleagues"""},
        {
            "role": "user", 
            "content": f"Can you please analyze the following short description: \"{short_description}\" , description: \"{description}\" , solution: \"{u_solution}\" and work notes and comments: \"{u_comments_and_work_notes}\" and provide the feedback in the specified JSON format. Use '+' for proactive actions and '-' for SLA breaches. Exclude any additional comments, explanations, or format indicators."
        },
    
         {
            "role": "assistant", 
            "content": """ 
                {
                    "Understand": "+CI and category is correct, 
                                   +KB is ok, 
                                   +Completion code is ok, 
                                   -FCR should don't have check incident created on the 29th of March ",
                    "Drive": "-Why resolving the incident on the 2nd day after giving the KB on how to enrol the device in Intune?",
                    "Solution": "+Ok",
                    "HumanTouch": "NA"
                }
            """
        }
    ]
    return incidentQualityAnalysisPromptMessages

def getPerformanceRatingPromptMessages(feedback):
    performanceRatingPromptMessages = [
      {
    "role": "system",
    "content": "You are an AI assistant that evaluates feedback based on specific performance criteria. Based on the feedback provided, return only a single word performance rating from the following options: 'excellent', 'good', 'average', 'poor', 'unacceptable', or 'n/a'. Do not provide any additional text or explanation."
},
{
    "role": "user",
    "content": f"please provide performance rating based on feedback \"{feedback}\" "
}

    ]
    return performanceRatingPromptMessages

def getTypeOfImprovmentPromptMessages(feedback):
    typeOfImprovmentPromptMessages = [
      {
    "role": "system",
    "content": "You are an AI assistant that evaluates feedback based on specific type of improvment. Based on the feedback provided, return only a single word type of improvment from the following options: 'U: Understand', 'High priority INC', 'D: Late transfer', 'D: Consistent Follow up', 'C: Preparation', 'C: Documentations', 'U: Documentation', 'S:Solution', 'D: Interactivity', 'C: Delivery', 'D: Hub Transfer', 'D: Assertive move to resolution', 'HT: Human Touch' or 'D: Unnecessary escalation'. Do not provide any additional text or explanation."
},
{
    "role": "user",
    "content": f"please provide type of improvment based on feedback \"{feedback}\" "
}

    ]
    return typeOfImprovmentPromptMessages


