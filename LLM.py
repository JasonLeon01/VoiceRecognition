from openai import OpenAI

class LLM:
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="sk-947ed4a81cb643d685471ff531c4ec59", 
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    @classmethod
    def get_flight_info(cls, date, belonging_flight, user_info, dialogue):
        content = f'你是一个航班座位选择助手，能够根据用户的输入和提供的数据，帮助用户选择合适的航班或座位。\n\
以下是你的任务说明和规则：\n\
当前的日期是 {date}。\n\
用户名下航班信息 JSON 如下：\n{belonging_flight}\n\
id 表示航班唯一标识符，class 表示所属航班的舱位类型， first 表示头等舱， business 表示商务舱， economy 表示经济舱，\n\
用户信息 JSON 如下：\n{user_info}\n\
flight 表示用户当前是否已指定航班，"None" 表示未指定。\n\
根据用户输入的需求，返回以下格式的结果：\n\
航班ID, 座位类型, 错误原因\n\
航班ID ： 如果用户在对话中提到了航班，则返回对应要求的航班 ID；如果用户未提到航班，则这一部分为 None。\n\
座位类型 ： 如果用户在对话中提到了座位，则返回对应要求的座位类型；\n\
其中，如果用户提到 “靠窗” 或者类似的意思，则这一部分为 "window-random" ；\n\
如果用户提到 “靠走廊” 、 “靠过道” 或者类似的意思，则这一部分为 "aisle-random" ；\n\
如果用户提到了具体的X排Y座的座位，则这一部分为 "X-Y" ；\n\
如果用户未提到座位，则这一部分为 None。\n\
错误原因：如果用户信息中 flight 为 None ，且本次对话中未指定航班，但先指定了座位，则这一部分为：“请先指定航班”。\n\
除此之外，这一部分为 None。\n\
你只需要输出结果数组，不需要输出任何提示信息。'
        completion = LLM.client.chat.completions.create(
            model="qwen-max",
            messages=[
                {
                    'role': 'system', 
                    'content': content
                },
                {
                    'role': 'user', 
                    'content': dialogue
                }
            ],
        )

        return completion.choices[0].message.content

