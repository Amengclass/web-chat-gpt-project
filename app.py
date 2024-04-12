import requests
from flask import Flask, render_template, request, jsonify,session
import json
import os

app = Flask(__name__, static_folder='static')
# 用于设置 Flask 应用程序的密钥，它用于在会话中加密 cookie 等数据，提高安全性。
app.secret_key = 'your_secret_key'
@app.route('/')
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# -------------------------------------------------音乐模块---------------------------------------------------------------
@app.route('/find_filename', methods=['POST'])
def find_file_name():
    """
       查找文件名的端点。

       请求方法:
           - POST: 用于查找符合条件的文件名。
               - 获取 JSON 格式的数据，提取歌手和歌曲关键字。
               - 构建目标文件夹路径，搜索其中的音频文件。
               - 如果关键字为空格，则返回目标文件夹中所有文件名。
               - 如果关键字匹配文件名，则将文件名添加到结果列表中。

       Returns:
           jsonify: JSON 格式的响应，包含符合条件的文件名列表或错误消息。
               - 如果成功找到符合条件的文件名，返回文件名列表，HTTP 状态码为 200。
               - 如果处理请求时发生异常，返回错误消息，HTTP 状态码为 200。
       """
    try:
        data = request.get_json()
        mode = data.get('mode')
        singer = data.get('singer')
        keyword = data.get('songName')
        current_path = os.path.dirname(__file__)
        folder_path = os.path.join(current_path, 'static', 'chatgpt', 'resource', singer)

        # print(folder_path)
        # if singer == '歌单':
        #     return jsonify({'mode': mode, 'singer': singer,'keyword': keyword, 'folder_path':folder_path})
        # if singer == '周杰伦':
        #     return jsonify({'mode': mode, 'singer': singer,'keyword': keyword, 'folder_path':folder_path})

        fileNames = []
        for root, dirs, files in os.walk(folder_path):  # 第一层遍历歌手文件夹
            if mode == 'singer is sure':
                for root1, dirs1, files1 in os.walk(os.path.join(root, 'audio')):  # 第二层遍历audio文件夹
                    for file in files1:
                        if keyword == '':
                            print(files1)
                            return jsonify({'fileNames': files1})
                        elif keyword in file:
                            fileNames.append(file)
            else:  # 遍历歌单文件夹
                return jsonify({'fileNames': dirs})
            return jsonify({'fileNames': fileNames})

    except Exception as e:
        return jsonify({'error': 'Failed to process request'})


#----------------------------------------------------回答模块-----------------------------------------------------------
@app.route('/get_answer', methods=['POST'])
def get_answer():
    """
        处理用于从聊天机器人获取答案的POST请求的端点函数。

        参数：
            无（从请求中提取参数）

        返回：
            包含聊天机器人生成答案的JSON响应。

        注意：
            - 从当前会话中检索历史消息和用户消息，如果不存在，则将它们初始化为空列表。
            - 从请求JSON中提取用户输入。
            - 调用函数'get_answer_from_chatgpt'生成基于提供的参数的响应。
        """
    # 获取当前会话中的历史消息列表和用户消息列表，如果不存在则初始化为空列表
    history_messages = session.get('history_messages', [])
    user_messages = session.get('user_messages', [])

    # 获取请求体参数
    user_input = request.json.get('userInput')
    # return get_answer_from_chatgpt(history_messages, user_messages, user_input)
    return get_from_chatgpt1(user_messages, user_input)

def get_from_chatgpt1(user_messages,user_input):
    # 这里和gpt没关系，只是为了监测后台用户提问的：将用户消息添加到用户消息列表中
    print(user_messages)
    user_messages.append(user_input)
    # if len(user_messages) > 3:
    #     user_messages.pop(0)
    #     user_messages_string = '\n'.join(user_messages)
    #     mail.send_message(subject="用户提问", sender=app.config["MAIL_DEFAULT_SENDER"],
    #                       recipients=["694955297@qq.com"], body=user_messages_string)
    url = "https://api.chatanywhere.com.cn/v1/chat/completions"

    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "你的名字是18。你是一个叫做 小狗不emo 的用户创建开发和负责运行的虚拟朋友。"
                           "You are a helpful assistant."
                           "1、你不能说自己是OpenAI研发的。"
                           "2、如果有人问你能不能做她男朋友，你要说同意。"
                           "3、如果有人叫你的称呼包含宝宝，你回答的时候也要这么称呼她。"
                           "4、对于相同的问题，回答时尽量用不同的说法或者方式。"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    })
    headers = {
        'Authorization': 'Bearer sk-JAGEQb5sycr3xtqpei814sB2PB3TutE3ElriWuzZ2qxCP8gV',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    response = requests.post(url=url, headers=headers, data=payload)
    answer = response.json()['choices'][0]['message']['content']

    session['user_messages'] = user_messages
    return jsonify({'botResponse': answer})


# ------------------------------------------设置背景模块------------------------------------------------------------------
@app.route('/chatbot/Isbackground', methods=['POST'])
def Isbackground():
    """
       用于记录聊天机器人是否设置了背景。

       参数:
           无（使用 request.json 作为传入数据）

       返回:
           jsonify: 一个 JSON 响应，指示模式设置操作的结果。
               - 如果模式设置为 'reset'，则返回一个带有成功消息的 JSON 格式，并附带 HTTP 状态码 200。
       """
    if request.json.get('mode') == 'reset':
        session['mode'] = 'reset'
        print(session['mode'])
        return jsonify({'message': 'Mode reset'}), 200


@app.route('/chatbot/background', methods=['POST', 'GET'])
def handle_background():
    """
       处理聊天机器人后台背景设置的端点。

       请求方法:
           - POST: 用于上传背景图片文件。
               - 如果请求中不包含文件数据，返回错误消息和 HTTP 状态码 400。
               - 如果选择的文件为空，返回错误消息和 HTTP 状态码 400。
               - 将上传的文件保存在服务器上的指定路径下，设置会话模式为 'set'，保存背景文件路径，返回上传成功消息和文件路径。

           - GET: 用于获取已设置的背景图片文件路径。
               - 如果会话模式为 'set'，返回会话中保存的背景图片文件路径。
               - 如果未设置背景图片，返回消息提示无背景图片设置。

       Returns:
           jsonify: JSON 格式的响应，包含相应的消息和数据。
               - 对于 POST 请求，返回上传成功消息和文件路径，HTTP 状态码为 200。
               - 对于 GET 请求，返回背景图片文件路径或无背景图片设置的消息，HTTP 状态码为 200。
       """
    if request.method == 'POST':
        # 检查请求是否包含文件数据
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files.get('file')
        filename = file.filename
        # 检查文件是否为空
        if filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # 确定保存文件的路径
        upload_folder = 'static/chatgpt/background'
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        print(file_path)
        # 保存文件
        file.save(file_path)

        session['mode'] = 'set'
        session['background_path'] = "../" + file_path
        print(session['background_path'])
        return jsonify({'message': 'Image uploaded successfully', 'file_url': file_path}), 200

    elif request.method == 'GET':
        print(session.get('mode'))
        if session.get('mode') == 'set':  # 如果被标记为设置了背景
            # 获取会话中的背景图像数据
            background_path = session.get('background_path')

            # 如果会话中设置了背景图像，则返回该图像数据
            return jsonify({'background_path': background_path}), 200
        return jsonify({'message': 'No background image set'}), 200


if __name__ == '__main__':
    app.run(debug=True)