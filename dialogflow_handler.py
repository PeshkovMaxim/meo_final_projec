import google.cloud.dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

DIALOGFLOW_PROJECT_ID = 'supportbot-memb'
DIALOGFLOW_LANGUAGE_CODE = 'ru'
SESSION_ID = 'me'
PROJECT_NUM = '814510649371'
USER = 'max'


def df_text_handler(text):
    text_to_be_analyzed = text
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
# отладочная информация
    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Fulfillment text:", response.query_result.fulfillment_text)
    with open('resources/request_stats.txt', 'a+') as log:
        log.write("\n" + f'{response.query_result.query_text}: {response.query_result.intent_detection_confidence}')
    return response.query_result.fulfillment_text
