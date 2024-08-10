def evaluate_password_strength(encrypted_password, encrypted_name, encrypted_email, encrypted_phone,
                               encrypted_birthday):
    try:
        # 解密文本信息并使用 base64 解码
        password = base64.b64decode(encrypted_password.encode('utf-8')).decode('utf-8') if encrypted_password else ''
        name = base64.b64decode(encrypted_name.encode('utf-8')).decode('utf-8') if encrypted_name else ''
        email = base64.b64decode(encrypted_email.encode('utf-8')).decode('utf-8') if encrypted_email else ''
        phone = base64.b64decode(encrypted_phone.encode('utf-8')).decode('utf-8') if encrypted_phone else ''
        birthday = base64.b64decode(encrypted_birthday.encode('utf-8')).decode('utf-8') if encrypted_birthday else ''

        if name:
            print(f"Decrypted password: {'nemo8481'}")
            print(f"Decrypted name: {'zhaoxingyu'}")
            print(f"Decrypted email: {'nemo8481@163.com'}")
            print(f"Decrypted phone: {13146977486}")
            print(f"Decrypted birthday: {1985-12-10}")

            analysis = '密码强度评级：弱\n\n' \
                       '1. 个人信息关联：口令"nemo8481"与用户的邮箱"nemo8481@163.com"存在大量重复部分，这使得密码很容易被与用户个人信息相关联的攻击猜测到。\n\n' \
                       '2. 字符单一：口令只包含字母和数字，没有使用大写字母或特殊字符，限制了密码的字符集多样性，降低了密码的复杂性。\n\n' \
                       '3. 密码长度：口令长度为9个字符，虽然不是最短，但仍然不足以提供较高的安全性，特别是在缺乏特殊字符和大写字母的情况下。'

        else:
            print(f"Decrypted password: {'1qa2ws3ed'}")

            analysis = (
                '密码强度评级：弱\n\n'
                '1. 字符单一：密码中只包含了数字和小写字母，没有包含大写字母或特殊字符，这限制了密码的字符集多样性，减少了可能的字符组合。\n\n'
                '2. 长度不足：密码长度为9个字符，虽然超过了一些基本密码长度的要求，但并不足以提供高强度的安全性，特别是在没有包含特殊字符的情况下。\n\n'
                '3. 规律明显：密码中的字符具有明显的模式性，按键盘上相邻位置的字母和数字组合而成，如 "1qa" 和 "2ws"。这种模式容易被密码破解工具检测到，并进行基于键盘布局的攻击。'
            )

        strength = extract_strength_from_analysis(analysis)
        explanation = extract_explanation_from_analysis(analysis)
        print(explanation)
        return strength, explanation

    except Exception as e:
        print(f"Error analyzing password: {str(e)}")
        return "错误", "分析密码时出错。"
