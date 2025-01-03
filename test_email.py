from email_sender import EmailSender
from config import EMAIL_CONFIG
from datetime import datetime

def test_email_sender():
    # 初始化邮件发送器
    email_sender = EmailSender(EMAIL_CONFIG)
    
    # 首先测试连接
    print("=== 测试SMTP服务器连接 ===")
    if not email_sender.test_connection():
        print("连接测试失败，退出测试。")
        return
    
    print("\n=== 测试邮件发送 ===")
    # 测试发送一封简单的邮件
    subject = "测试邮件"
    content = """
    <html>
    <body>
        <h2>这是一封测试邮件</h2>
        <p>如果你收到这封邮件，说明邮件发送配置正确！</p>
        <p>时间：{}</p>
        <hr>
        <p style="color: blue;">来自Python脚本的测试</p>
    </body>
    </html>
    """.format(datetime.now())

    # 尝试发送邮件
    success = email_sender.send_email(subject, content)
    print(success)
    
    if success:
        print("测试邮件发送成功！请检查你的收件箱。")
    else:
        print("测试邮件发送失败，请检查配置。")

if __name__ == "__main__":
    print("开始测试邮件发送功能...")
    test_email_sender() 