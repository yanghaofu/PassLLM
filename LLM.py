from flask import request, Flask, render_template, jsonify
from openai import OpenAI
import requests

app = Flask(__name__)

# 请替换成你的OpenAI API密钥
api_key = "sk-Z6ttNnGzWksu7LYIOVVNuvXi3GqD5g6rykmK7NAn7ZcqTP7Q"
client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # 获取表单数据
    data = request.json

    # 使用 .get() 方法从 JSON 数据中获取每个字段，如果字段不存在则默认为 None
    username = data.get('username')
    email = data.get('email')
    birthday = data.get('birthday')  # 注意：这里假设字段名是 'birthday' 而不是 'brithday'
    password = data.get('password')

    print(password)

    # 检查口令强度
    strength, explanation = check_password_strength(password)

    # 返回密码强度和解释信息
    return jsonify({
        'message': 'Password strength evaluated',
        'strength': strength,
        'explanation': explanation
    })

def check_password_strength(password):
    # 构造API请求消息
    messages = [
        {"role": "system", "content": "评估以下口令的强度："},
        {"role": "user", "content": password}
    ]

    # 调用OpenAI API
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=messages,
        temperature=0.3,
    )

    # 直接访问ChatCompletionMessage对象的content属性
    response_message = completion.choices[0].message.content

    print(response_message)

    # 根据OpenAI的响应来确定密码强度和解释
    # 这里需要根据实际返回的内容来编写逻辑，以下是一个示例
    if "强" in response_message:  # 假设模型返回包含“强”字表示密码强
        strength = 5

    else:
        strength = 1

    return strength, response_message


if __name__ == '__main__':
    app.run(debug=True)
