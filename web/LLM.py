from flask import request, Flask, render_template, jsonify
from flask_sslify import SSLify
import sys
from openai import OpenAI

# 请替换成你的OpenAI API密钥
api_key = "sk-Z6ttNnGzWksu7LYIOVVNuvXi3GqD5g6rykmK7NAn7ZcqTP7Q"

client = OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",
)

# 确保使用UTF-8编码
if sys.getdefaultencoding() != 'utf-8':
    import importlib
    importlib.reload(sys)
    sys.setdefaultencoding('utf-8')

app = Flask(__name__)
sslify = SSLify(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    password = data.get('password', '')

    print(password)

    strength, explanation = evaluate_password_strength(password)

    response = {
        "strength": strength,
        "explanation": explanation
    }

    return jsonify(response)

def evaluate_password_strength(password):
    try:
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。"
                        "你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，"
                        "种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
                    )
                },
                {
                    "role": "user",
                    "content": f"请分析以下密码的强度，并解释为什么它强或弱：\n\n密码: {password}"
                },
            ],
            temperature=0.3,
        )

        analysis = completion.choices[0].message.content.strip()
        strength = extract_strength_from_analysis(analysis)
        explanation = extract_explanation_from_analysis(analysis)
        return strength, explanation

    except Exception as e:
        print(f"Error analyzing password: {str(e)}")
        return 0, "Error analyzing password."

def extract_strength_from_analysis(analysis):
    if "非常强" in analysis:
        return 5
    elif "强" in analysis:
        return 4
    elif "中等" in analysis:
        return 3
    elif "弱" in analysis:
        return 2
    else:
        return 1

def extract_explanation_from_analysis(analysis):
    return analysis

if __name__ == '__main__':
    context = ('.E:\大三\信安作品赛\代码\pass\cert.pem', 'E:\大三\信安作品赛\代码\pass\key.pem')  # 替换成你的证书和密钥文件路径
    app.run(debug=True, ssl_context=context)
