# Tesla 官网监控器

一个用于监控 Tesla 中国官网变化的自动化工具。当检测到网页内容发生变化时，会自动发送邮件通知。

## 功能特点

- 实时监控 Tesla 中国官网的内容变化
- 智能过滤动态内容，减少误报
- 自动邮件通知功能
- 支持环境变量配置，安全管理敏感信息

## 安装要求

- Python 3.6+
- 依赖包：
  ```bash
  pip install requests beautifulsoup4
  ```

## 环境变量配置

在运行程序前，需要设置以下环境变量：

```bash
Linux/Mac
export SENDER_EMAIL="your_email@example.com"
export SENDER_PASSWORD="your_email_password"
export RECEIVER_EMAIL="receiver@example.com"

Windows
set SENDER_EMAIL=your_email@example.com
set SENDER_PASSWORD=your_email_password
set RECEIVER_EMAIL=receiver@example.com
```

注意：如果使用 QQ 邮箱，`SENDER_PASSWORD` 需要使用授权码而不是邮箱密码。

## 使用方法

1. 克隆仓库：
   ```bash
   git clone [repository_url]
   cd tesla-monitor
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 设置环境变量（见上文）

4. 运行程序：
   ```bash
   python monitor.py
   ```

## 工作原理

1. 程序每5分钟获取一次 Tesla 官网内容
2. 使用 BeautifulSoup 清理 HTML 内容，移除动态内容
3. 计算清理后内容的 MD5 值进行比对
4. 发现变化时通过邮件通知指定收件人

## 注意事项

- 建议使用 QQ 邮箱作为发送邮箱
- 确保网络连接稳定
- 程序使用长期运行，建议在服务器上部署

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
