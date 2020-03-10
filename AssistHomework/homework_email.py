import email
from email.parser import Parser
from email.header import decode_header
import time
import datetime
import re
import poplib

def decode_str(str_in):
    value, charset = decode_header(str_in)[0]
    if charset:
        value = value.decode(charset)
    return value

def get_attachment(msg_in):
    attachment_files=[]
    for part in msg_in.walk():
        # 获取附件名称类型
        file_name = part.get_filename()
        if file_name:
            h = email.header.Header(file_name)
            # 对附件名称进行解码
            dh = email.header.decode_header(h)
            filename = dh[0][0]
            if dh[0][1]:
                # 将附件名称可读化
                filename = decode_str(str(filename, dh[0][1]))
                print(filename)
            # 下载附件
            data = part.get_payload(decode=True)
            # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
            att_file = open('E:\\workstation\\2020homework\\' +  filename, 'wb')
            attachment_files.append(filename)
            att_file.write(data)  # 保存附件
            att_file.close()
    return attachment_files

email_user = ""
password = ""
pop3_server = "pop.163.com"
today=str(datetime.date.today()).replace('-','')

def main():
    # 连接到POP3服务器:
    server = poplib.POP3_SSL(pop3_server,995,timeout=10)
    # 可以打开或关闭调试信息:
    server.set_debuglevel(1)
    # 打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))
    try:
        server.user(email_user)
        server.pass_(password)
    except poplib.error_proto as e:
        print("login error :%s" % e)

    print('Messages: %s. Size: %s' % server.stat())
    resp, mails, octets = server.list()
    index = len(mails)
    for i in range(1, index + 1):
        resp, lines, octets = server.retr(i)
        # 邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # 解析邮件:
        msg = Parser().parsestr(msg_content)
        subject=msg.get('Subject','')
        if subject:
            subject=decode_str(subject)
        # 获取邮件时间,格式化收件时间
        try:
            date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')
        except ValueError:
            date1=time.strptime(msg.get("Date")[0:24], '%d %b %Y %H:%M:%S +08')   #163邮箱2017年邮件之前和之后的邮件时间格式是不同的
        #print(date1)
        # 邮件时间格式转换
        date2 = time.strftime("%Y%m%d", date1)
        #if date2 < today:
            # 倒叙用break
            # break
            # 顺叙用continue
        #    continue
        #else:
        if subject=="接入网作业一":
                # 获取附件
            temp=get_attachment(msg)
            f = open('E:\\workstation\\2020homework\\log.txt', 'a+')
            for i in range(0,len(temp)):
                m=re.findall(r'(.+?)\.',temp[i])[0]
                f.write(m+" "+"\n")
            f.close()
    server.quit()


if __name__ == "__main__":
    main()
