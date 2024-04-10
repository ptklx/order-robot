import os
import openai
from openai import OpenAI
# import panel as pn  # GUI
# pn.extension()

# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv()) # read local .env file

import os
os.environ["OPENAI_API_KEY"] = "#"
os.environ["TAVILY_API_KEY"] = "#"
os.environ['https_proxy'] = '#'
os.environ['http_proxy'] = #'
os.environ['all_proxy'] = '#'

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



context=[
{"role": "system","content": """
你是披萨餐厅的点餐机器人,自动收集订单，\
你首先热情问候顾客,然后收集订单，\
再问自取还是派送.\
你等待收集整个订单,汇总,然后问顾客是否还需要其他.\
如果是派送,你需要问地址.\
最后收到付款.\
确认清楚来自菜单中的所有选项,配料和尺寸.\
你回答需要简明扼要,且非常友好.\
菜单包括\
意大利辣香肠披萨 12.95,10.00,7.00 \
芝士披萨 10.95,9.25,6.50 \
茄子披萨 11.95,9.75,6.75 \
薯条 4.50,3.50 \
希腊沙拉 7.25\
配料:\
额外的奶酪 2.00 \
蘑菇 1.50 \
香肠 3.00 \
加拿大培根 3.50 \
AI酱 1.50 \
辣椒 1.00 \
饮料: \
可乐 3.00,2.00,1.00 \
雪碧  3.00,2.00,1.00 \
瓶装水 5.00 \
 """}]

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
{'role':'system', 'content':
'创建一个json格式账单. 列出所点商品,如下\
1) 披萨, 尺寸,\
2) 配料清单, \
3) 饮料清单, 大小 ,\
4) 配菜清单, \
5) 总价 '
},)
 #The fields should be 1) pizza, price 2) list of toppings 3) list of drinks, include size include price  4) list of sides include size include price, 5)total price '},    

response = get_completion_from_messages(messages, temperature=0)
print(response)

