from wit import Wit

WIT_ACCESS_TOKEN = "GLRYCITZUVHT5S3MA6KPQWKMBKL25XI2"

client = Wit(access_token = WIT_ACCESS_TOKEN)

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
    print(resp_list)


print(wit_response("i am going from singapore to france next week for 3 days with 2 adults and 2 children"))
#print(wit_response("i am from singapore"))
#print(wit_response("i am going japan"))
#print(wit_response("i am going france next week"))

'''msg = "i am going from singapore to france next week for 3 days with 2 adults and 2 children"
resp = client.message(msg)
print(resp)'''
