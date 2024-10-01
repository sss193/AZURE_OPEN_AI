from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
import logging
from incidentQualityAnalysisPrompt import getIncidentQualityAnalysisPromptMessages
from incidentQualityAnalysisPrompt import getPerformanceRatingPromptMessages
from incidentQualityAnalysisPrompt import getTypeOfImprovmentPromptMessages
from utils import getCleanedFeedback
from utils import convertTextToDictionary
from aoaiChatCompletion import getLLMResponse



app = Flask(__name__)

load_dotenv(override=True)


# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler() 
                    ])
logger = logging.getLogger(__name__)


@app.route('/feedback', methods=['GET'])
def get_feedback():
    incident_id = request.args.get('incident_id')
    if not incident_id:
        return jsonify({"error": "incident_id query parameter is required"}), 400
    
    return get_incident_details(incident_id)



def get_incident_details(incident_id):
    api_url = os.environ['SERVICENOW_URL'] + '/api/now/table/incident?number='+incident_id+'&sysparm_display_value=true'
    user = os.environ['SERVICENOW_ADMIN_USERNAME']
    pwd = os.environ['SERVICENOW_ADMIN_PASSWORD']
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    try:
        response = requests.get(api_url, auth=(user, pwd), headers=headers,verify=False)
        if response.status_code != 200:
            logger.error(f"Unexpected Error: {response.json()}")
            return jsonify(error="An unexpected error occurred for Incident details"), 400 

        data = response.json()['result']

        if len(data)==0:
            return jsonify({"error": "Invalid Incident Id"}), 400
        
        short_description = data[0].get("short_description")
        description = data[0].get("description")
        u_solution = data[0].get("u_solution")
        u_comments_and_work_notes = data[0].get("work_notes") + data[0].get("comments")
        userProfileLink = data[0].get("caller_id").get("link")
        vipProfileStatus = getVipProfileStatus(userProfileLink, user, pwd, headers)
        print(f'this is vipStatus-------->>>{vipProfileStatus}')
    except ValueError as ve:
        logger.error(f"ValueError Error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        return jsonify(error="An unexpected error occurred"), 400
    return get_feedback_from_LLM(short_description, description, u_solution, u_comments_and_work_notes, vipProfileStatus)
  
def getVipProfileStatus(userProfileLink, user, pwd, headers):
    vipStatus = False
    try:
        response = requests.get(userProfileLink, auth=(user, pwd), headers=headers,verify=False)  
        if response.status_code != 200:
            logger.error(f"Unexpected Error: {response.json()}")
            return jsonify(error="An unexpected error occurred for Incident details"), 400  
        
        data = response.json()['result']
        vipStatus = data.get("vip")
        if len(data)==0:
            return jsonify({"error": "Invalid user sys Id"}), 400
        
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        return jsonify(error="An unexpected error occurred for user profile"), 400 
    return vipStatus     

def get_feedback_from_LLM(short_description, description, u_solution, u_comments_and_work_notes, vipProfileStatus):
    try:   
        response = getLLMResponse(getIncidentQualityAnalysisPromptMessages( short_description, description, u_solution, u_comments_and_work_notes, vipProfileStatus))
        cleaned_feedback = getCleanedFeedback(response)
        performanceRating = getLLMResponse(getPerformanceRatingPromptMessages(cleaned_feedback))
        typeOfImprovment = getLLMResponse(getTypeOfImprovmentPromptMessages(cleaned_feedback))
        result = convertTextToDictionary(cleaned_feedback, performanceRating, typeOfImprovment)
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")   
        return jsonify({"error": str(e)}), 400
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)