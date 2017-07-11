from wit import Wit

WIT_ACCESS_TOKEN = "GLRYCITZUVHT5S3MA6KPQWKMBKL25XI2"

client = Wit(access_token = WIT_ACCESS_TOKEN)

# returns a list of lists with the first item being the user input and subsequent items being the [entity, value] pairs
def wit_response(message_text):
    user_input = client.message(message_text)
    entity = None
    value = None
    input_dict = user_input['entities']
    resp_list = []
    resp_list.append([user_input['_text']])

    for key in input_dict:
        entity = key
        value = input_dict[key][0]['value']
        resp_list.append([entity, value])
    
    return resp_list