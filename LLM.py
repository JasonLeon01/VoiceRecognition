from openai import OpenAI

class LLM:
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="sk-947ed4a81cb643d685471ff531c4ec59", 
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    @classmethod
    def get_info(cls, date, belonging_flight, flight_seat, user_info, dialogue):
        content = f'你是一个航班座位选择助手，能够根据用户的输入和提供的数据，帮助用户选择合适的航班或座位。\n\
以下是你的任务说明和规则：\n\
当前的日期是 {date}。\n\
用户名下航班信息 JSON 如下：\n{belonging_flight}\n\
id 表示航班唯一标识符，class 表示所属航班的舱位类型， first 表示头等舱， business 表示商务舱， economy 表示经济舱，\n\
座位占有信息 JSON 如下：\n{flight_seat}\n\
数组项里面， True 表示座位空闲，可以被选择， False 表示座位有人占据，此时不能选择该座位。\n\
每个航班有多个舱位（如头等舱、商务舱、经济舱）。每行表示一排座位，最中间的两个元素表示靠近走廊/过道的座位，第一个和最后一个元素表示靠窗的座位。\n\
用户信息 JSON 如下：\n{user_info}\n\
flight 表示用户当前是否已指定航班，"None" 表示未指定。seat 表示用户当前是否已指定座位，["None", -1, -1] 表示未指定。\n\
根据用户输入的需求，返回以下格式的结果：\n\
[航班ID, 座位信息, 错误原因]\n\
航班ID : 如果用户需要选择航班，则返回对应的航班 ID；如果用户已经指定航班，则这一部分为 None。\n\
座位信息 : 格式为 ["舱位类型", 排号, 列号]。舱位类型归属于用户名下的航班信息。\n\
你要根据用户的要求，在座位占有信息数据里面，选择用户所属的舱位中当前空闲的座位，也就是为 True 的项。\n\
例如，如果用户所属舱位的座位占有信息是 经济舱 的 [[False, False, False, True, False, True]]，则用户可以选择的座位是第 1 排的第 4 和第 6 个，而第 1 、 2、 3、 5 个座位不能被选择。\n\
对应的该部分信息是 ["economy", 0, 3] 或 ["economy", 0, 5] 。\n\
如果用户要求模糊，则在符合要求的座位里面随机选择一个。如果用户直接指定了特定的座位。如果用户要求没有提到座位相关信息，这一部分则是["None", -1, -1]\n\
错误原因 : 如果无法满足用户需求，则返回具体原因。如果确实满足了用户需求，则这一部分为 None\n\
用户需求解析规则如下：\n\
如果用户的需求中包含航班，则返回对应的航班 ID，如果用户没有明确指定航班 ID，而是时间等信息，例如；“离我时间最近的航班”，则按照时间要求选择。\n\
如果用户的需求中包含座位，如果用户没有明确指定座位，则返回满足条件的座位信息，例如，“靠窗的座位”、“靠走廊的座位”等。如果用户明确指定了座位，则返回对应的座位信息。\n\
如果用户未指定航班但先指定了座位，则返回错误提示：“请先指定航班”。\n\
如果没有符合用户需求的座位，则返回错误提示：“没有符合条件的座位”。\n\
你只需要输出结果数组，不需要输出任何提示信息。'
        print(content)
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

