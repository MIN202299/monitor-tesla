import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime

class EmailSender:
    def __init__(self, config):
        """
        初始化邮件发送器
        config: 包含邮件配置的字典
        """
        self.smtp_server = config.get('smtp_server', 'smtp.qq.com')
        self.smtp_port = config.get('smtp_port', 465)
        self.sender_email = config.get('sender_email')
        self.sender_password = config.get('sender_password')
        self.receiver_email = config.get('receiver_email')
        self._server = None

    def test_connection(self):
        """测试SMTP服务器连接和登录"""
        try:
            print(f"正在连接到 {self.smtp_server}:{self.smtp_port}...")
            self._server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            print("连接成功！正在尝试登录...")
            
            # 尝试登录
            self._server.login(self.sender_email, self.sender_password)
            print(f"登录成功！邮箱 {self.sender_email} 配置正确。")
            
            # 关闭连接
            self._server.quit()
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"登录失败！认证错误：{e}")
            print("请检查邮箱地址和授权码是否正确。")
            return False
        except Exception as e:
            print(f"连接失败！错误信息：{e}")
            return False

    def send_update_notification(self, url):
        """发送网站更新通知邮件"""
        subject = "Tesla官网更新通知"
        current_time = datetime.now()
        
        content = f"""
        <html>
        <body>
            <h2>Tesla官网内容已更新</h2>
            <p>更新时间：{current_time}</p>
            <p>网站地址：<a href="{url}">{url}</a></p>
            <p>请及时查看最新内容！</p>
        </body>
        </html>
        """
        
        return self.send_email(subject, content)

    def send_email(self, subject, content):
        """发送邮件的具体实现"""
        try:
            # 创建邮件对象
            message = MIMEMultipart()
            message['From'] = self.sender_email  # 直接使用邮箱地址，不用Header
            message['To'] = self.receiver_email  # 直接使用邮箱地址，不用Header
            message['Subject'] = Header(subject, 'utf-8')
            
            # 添加邮件正文
            message.attach(MIMEText(content, 'html', 'utf-8'))
            
            # 创建SMTP_SSL连接
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            try:
                # 登录
                server.login(self.sender_email, self.sender_password)
                # 发送邮件
                server.sendmail(
                    self.sender_email, 
                    [self.receiver_email], # 使用列表形式
                    message.as_string()
                )
                print(f"邮件发送成功：{subject}")
                return True
            finally:
                # 确保连接被关闭
                server.quit()
            
        except Exception as e:
            print(f"邮件发送失败：{str(e)}")
            return False 