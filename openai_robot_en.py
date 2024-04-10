import os
import openai
from openai import OpenAI
# import panel as pn  # GUI
# pn.extension()

# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv()) # read local .env file

import os
os.environ["OPENAI_API_KEY"] = "###"
os.environ["TAVILY_API_KEY"] = "##"
os.environ['https_proxy'] = '##'
os.environ['http_proxy'] = '##'
os.environ['all_proxy'] = '##'

openai.api_key  = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
    )

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    # response = openai.ChatCompletion.create(
    #     model=model,
    #     messages=messages,
    #     temperature=0, # this is the degree of randomness of the model's output
    # )
    response = client.chat.completions.create(
            messages=messages,
            model=model,  # "gpt-3.5-turbo"  "text-davinci-003"
            #max_tokens=100  # 生成的最大标记数
            temperature=0,
        )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    # response = openai.ChatCompletion.create(
    #     model=model,
    #     messages=messages,
    #     temperature=temperature, # this is the degree of randomness of the model's output
    # )
    response = client.chat.completions.create(
            messages=messages,
            model=model,  # "gpt-3.5-turbo"  "text-davinci-003"
            #max_tokens=100  # 生成的最大标记数
            temperature=temperature,
        )
    # print(str(response.choices[0].message))
    return response.choices[0].message.content



# def collect_messages(_):
#     prompt = inp.value_input
#     inp.value = ''
#     context.append({'role':'user', 'content':f"{prompt}"})
#     response = get_completion_from_messages(context) 
#     context.append({'role':'assistant', 'content':f"{response}"})
#     panels.append(
#         pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
#     panels.append(
#         # pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
#         pn.Row('Assistant:', pn.pane.Markdown(response, width=600)))
 
#     return pn.Column(*panels)



context = [ {'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""} ]  # accumulate messages

# inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
# button_conversation = pn.widgets.Button(name="Chat!")
# panels = [] # collect display 


# interactive_conversation = pn.bind(collect_messages, button_conversation)

# dashboard = pn.Column(
#     inp,
#     pn.Row(button_conversation),
#     pn.panel(interactive_conversation, loading_indicator=True, height=300),
# )



while True:
    query = input("agent:")
    if query.startswith(':'):
        command_words = query[1:].strip().split()
        if not command_words:
            command = ''
        else:
            command = command_words[0]
        if command in ['exit', 'quit', 'q']:
            break

    prompt = query
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    print(response)
    context.append({'role':'assistant', 'content':f"{response}"})


messages =  context.copy()
messages.append(
{'role':'system', 'content':'create a json summary of the previous food order. Itemize the price for each item\
 The fields should be 1) pizza, include size 2) list of toppings 3) list of drinks, include size   4) list of sides include size  5)total price '},    
)
 #The fields should be 1) pizza, price 2) list of toppings 3) list of drinks, include size include price  4) list of sides include size include price, 5)total price '},    

response = get_completion_from_messages(messages, temperature=0)
print(response)

