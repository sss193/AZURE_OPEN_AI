import re
import json

def getCleanedFeedback(feedback):
    cleaned_response = feedback.replace("```json", "").replace("```", "").strip()
    cleaned_res = cleaned_response.replace("\n", "")
    cleaned_feedback = re.sub(r'\s+', ' ', cleaned_res)
    return cleaned_feedback

def convertTextToDictionary(feedback, performanceRating, typeOfImprovment):
    data = json.loads(feedback)
    Understand = data["Understand"]
    Drive = data["Drive"]
    Solution = data["Solution"]
    HumanTouch = data["HumanTouch"]
    
    llmfeedback = {"understand": Understand,
                   "drive": Drive,
                   "solution": Solution,
                   "humanTouch": HumanTouch,
                   }

    response_data = {
        "feedback": llmfeedback,
        "performance_rating": performanceRating,
        "type_of_improvment": typeOfImprovment
    }
    return response_data