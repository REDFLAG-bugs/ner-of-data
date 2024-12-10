#!/usr/bin/env python
# coding: utf-8

# In[15]:


from dotenv import load_dotenv
import os
import json
import ast

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

if api_key is None:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")


# In[16]:


from langchain_groq import ChatGroq

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

def extract_json(content):
    start = content.find('```json\n') + 7
    end = content.find('```', start)
    json_str = content[start:end].strip()
    return ast.literal_eval(json_str)
def extract_json_manual(content):
    start = content.find('```json\n') + 7
    end = content.find('```', start)
    json_str = content[start:end].strip()
    import json 
    return json.loads(json_str)

def get_ai_msg(patient_prompt):
    messages = [  
        {
            "role": "system",
            "content": """
              You are a medical assistant capable of extracting structured details from unstructured clinical text. Your task is to identify specific categories of information from the provided text. Additionally, you need to identify and flag any unknown or unfamiliar terms that may need further clarification or special handling.
            The categories you need to extract from the text are:
         1. **Status**: Identify the patient's health status, such as "stable," "critical," "recovering," "improving," etc.
         2. **Pharmacy**: Extract references to medication, prescriptions, or pharmacy-related details (e.g., medication names, dosages, directions).
         3. **Services**: Extract any references to medical services, tests, or procedures mentioned (e.g., lab tests, imaging, surgeries).
         4. **Unknown Words**: Flag any terms or phrases that are unfamiliar or do not fit within the recognized categories, indicating the need for further clarification or special handling.

         Please note that further clarification or special handling may be needed for the patient's health status and the interpretation of their symptoms."""
        },
        {
            "role": "system",
            "content": """Based on the provided information, you can provide a structured response. Here is the response:
             {
                  "status": "stable",
                  "pharmacy": {
                  "medications": [**separate new medicines, each medicines prescribed should be made put into another category of medicine, expanding their name, dosage, unit, ICD code, frequency of medication**]
         [
            {
                  "name": medicine name,  // This is a literal string, not a placeholder 
                  "dosage": amount,
                  "unit" : amount,
                  "ICD code": ICD code, [(**search the web, get the ICD code form the web**)]
                  "frequency": frequency [(**Should be detailed about the time period**)]
             },
         ]
     }, ```Observe carefully the format of the response, extracting all the services```
     "services": {  
         "tests": [
            // Provide all the tests that are being prescribed to the patient, if any
         ]           
     },
     "unknown_words": [ 
     ]
            """


        },
        {
            "role": "user",
            "content": patient_prompt
        }
    ]
    ai_msg = llm.invoke(messages)
    ai_msg_json=extract_json(ai_msg.content)
    ai_msg_json= extract_json_manual(ai_msg.content)
    ai_msg_json_file = json.dumps(ai_msg_json, indent=4)
    return ai_msg_json_file

def get_ai_msg_manual(patient_prompt):
    return get_ai_msg(patient_prompt)