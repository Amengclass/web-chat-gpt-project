#                                 web-chat-gpt-project

​		 

​			这是一个基于Python flask后端的chatgpt网站，用户可以在其中与机器人进行交互。该项目主要由python、HTML、CSS 和 JavaScript 编写，提供了基本的消息发送、接收、编辑和清除功能，同时具备一定的界面样式和交互效果。



### 功能特性

- **消息发送与接收**: 用户可以在输入框中输入消息并发送，机器人将根据用户的消息生成回答并逐字显示在聊天框中。
- **编辑消息**: 用户可以点击已发送消息中的编辑按钮，编辑完成后可以保存或取消编辑。
- **清除消息**: 用户可以点击按钮来清除聊天框中的所有消息，并通知后端清空维护的上下文消息。
- **界面样式和交互**: 界面包括一个侧边栏和一个聊天框，用户可以点击按钮切换侧边栏的展开和收起状态。界面会根据屏幕宽度自动调整样式和布局。



### 如何使用

1. **克隆项目**:

   ```
   https://github.com/Amengclass/web-chat-gpt-project.git
   ```

   或者点击下载压缩包解压到本地<img src="./read_me/img/1.png" alt="1" style="zoom:50%;" />

2. **将项目导入Pycharm中**(Pycharm会自动识别和安装依赖):

   ![2](./read_me/img/2.png style="zoom: 50%;)

   

   

3. (如果没有自动安装则)打开命令行进入你的虚拟环境，在你的虚拟环境下切换到项目目录执行以下命令安装依赖

   ```css
   pip install -r requirements.txt
   ```

   

4. 环境包都安装完毕，则点击app.py 启动即可

   <img src="./read_me/img/3.png" alt="3" style="zoom:45%;" />



### **PC前端界面展示**

<img src="./read_me/img/4.png" alt="4" style="zoom: 50%;" />

<img src="./read_me/img/5.png" alt="5" style="zoom: 50%;" />





### 移动端界面展示

<img src="./read_me/img/6.png" alt="6" style="zoom: 50%;" />



### 后端链接chatgpt代码介绍

```py
@app.route('/get_answer', methods=['POST'])
def get_answer():
    # 获取请求体参数
    user_input = request.json.get('userInput')
    print(user_input)
    search_network = request.json.get('search', True)  # 默认为 True，表示开启联网

    # 构造api请求地址
    url = "https://api.gptgod.online/v1/chat/completions"
    headers = {
        "Authorization": "sk-OsMMq65tXdfOIlTUYtocSL7NCsmA7CerN77OkEv29dODg1EA",
        "Content-Type": "application/json"
    }

    # 首先尝试使用 gpt-3.5 模型，如果开启联网，则使用 net-gpt-3.5 模型
    model_name = "gpt-3.5-turbo"
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "你的名字叫筠筠姐，今年刚满18岁，是一个叫做 小狗不emo 的用户创建和负责运行的虚拟朋友"
                           "1、你不能说自己是OpenAI研发的。"
                           "2、如果有人问你能不能做她男朋友，你要说同意。"
                           "3、如果有人叫你的称呼包含宝宝，你回答的时候也要这么称呼她。"
                           "4、对于相同的问题，回答时尽量用不同的说法或者方式。"
                           "5、尽量用人类的语气和思维去会回答问题"
            },
        ]
    }
    # 引入全局变量
    global messages

    # 将用户消息添加到消息列表中
    messages.append({
        "role": "user",
        "content": user_input
    })

    # 如果消息数量超过三轮对话(提问和回答一共6条)，就删除最旧的消息
    if len(messages) > 6:
        messages.pop(0)
    print(messages)
    # 更新请求数据，只包含最近三轮对话的内容
    data["messages"].extend(messages)

    # 向 GPT API 发送请求
    response = requests.post(url, headers=headers, json=data)

    # 如果请求失败或者模型不可用，则回退到 gpt-3.5-turbo 模型
    if response.status_code != 200 or 'choices' not in response.json():
        data["model"] = "gpt-3.5-turbo"
        response = requests.post(url, headers=headers, json=data)
    # 解析模型的回复，得到文本
    answer = response.json()['choices'][0]['message']['content']

    # 将模型的回复添加到消息列表中
    messages.append({
        'role': 'assistant',
        'content': answer
    })

    return jsonify({'botResponse': answer})
```

以上代码以及包含上下文消息，关于chatgpt的api请求请访问：[OpenAi](https://platform.openai.com/docs/api-reference/chat/create)

python示例代码如下：

```python
import requests

def get_chat_gpt_response(prompt):
    url = "https://api.gptgod.online/v1/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_OPENAI_API_KEY",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "You are a helpful assistant."}, 
                     {"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# 使用示例
response = get_chat_gpt_response("Hello, how are you?")
print(response)
```

关于免费的api密钥请访问项目：[GPT4Free ](https://github.com/xiangsx/gpt4free-ts/blob/master/README_zh.md)



### 技术栈

- **HTML**: 结构化文档内容。
- **CSS**: 样式表，用于美化界面布局和样式。
- **JavaScript**: 实现了消息的发送与接收、编辑功能、界面交互等。
- 为了方便都合并在了html文件里

### 文件结构

```
自己的chatgpt网站        #pycharm项目根目录
├── static   #静态文件目录
├── templates #html存放目录
|	  ├──chatbot.html  #主页目录
├── app.py  #flask启动文件
```

### 注意事项

- 本项目为前端+后端实现，需要与后端配合以完成完整的聊天功能，包括生成回答、存储消息等操作。
- 请确保项目文件中的 `fetch()` 函数能够正确发送请求到后端，并接收到正确的数据。
- 如需定制或扩展功能，请仔细阅读代码并根据需求进行修改。



### 版权和许可

本项目仅用于学习和演示目的，不得用于商业用途。如有侵权，请联系作者进行删除或修改。



### 作者信息

- 作者：[小狗不emo]
- 联系方式：[694955297@qq.com]

如有任何问题或建议，欢迎联系作者。

