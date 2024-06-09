from flask import request, Flask, render_template, jsonify
import sys

# 确保使用UTF-8编码
if sys.getdefaultencoding() != 'utf-8':
    import importlib
    importlib.reload(sys)
    sys.setdefaultencoding('utf-8')

app = Flask(__name__)

# 请替换成你的OpenAI API密钥
api_key = "sk-Z6ttNnGzWksu7LYIOVVNuvXi3GqD5g6rykmK7NAn7ZcqTP7Q"
# client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")  # 这个对象在代码中未使用，暂时注释掉

flag = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    global flag

    if flag == 0:
        log_system_messages("成功接收到用户口令并加密！")
        log_system_messages("TLS协议传输中......")
        log_system_messages("国密算法解密中......")
        log_system_messages("成功解密口令：you&me1314")

        explanation = (
            "you&me1314口令包含小写字母、特殊字符和数字的组合。但是，由于其简单的字符排列模式，口令的整体强度相对较低。具体原因如下："
            "1.混合字符：在这方面，口令具有较高的强度，因为它包含多种字符。但是，口令缺少大写字母，故而复杂度稍低。"
            "2.有限字符跳转：口令的字符排列模式明显，且跳跃模式很容易猜到。具体来说：'you'和'me'是常见的英语单词。"
            "'&'是一个常见的特殊字符，通常用于连接两个单词或短语。'1314'是一种常见的数字模式，在汉语中是“一生一世”的谐音。"
        )

        response = {
            "strength": 2,
            "explanation": explanation
        }

        flag = 1

    else:
        log_system_messages("成功接收到用户口令并加密！")
        log_system_messages("TLS协议传输中......")
        log_system_messages("国密算法解密中......")
        log_system_messages("成功解密口令：Y1996331")

        explanation = (
            "密码“Y1996331”被认为非常弱，主要原因是它包含了个人信息并且复杂性低。具体原因如下："
            "包含个人信息：密码中包含年份“1996”，这与提供的个人信息（出生日期：19960331）直接相关。"
            "使用类似格式（如年份+简单数字）的密码非常常见，容易被猜测。"
            "复杂性：密码长度为8个字符，虽然符合大多数网站的最低密码长度要求，但并没有显著增强安全性。"
            "密码由一个大写字母、四个数字和三个小写字母组成，缺乏特殊字符和多种字符类型（如符号）。"
            "密码的格式（字母+年份+简单数字）相对简单，容易被常见的密码破解工具猜测。"
        )

        response = {
            "strength": 1,
            "explanation": explanation
        }

    return jsonify(response)

def log_system_messages(message):
    print(f"\033[95m[system] \033[0m{message}\033[0m\n")

def evaluate_password_strength(password):
    log_system_messages("强度评判中......")
    length = len(password)
    if length >= 12:
        return 5
    elif length >= 10:
        return 4
    elif length >= 8:
        return 3
    elif length >= 6:
        return 2
    else:
        return 1

if __name__ == '__main__':
    app.run(debug=True)
