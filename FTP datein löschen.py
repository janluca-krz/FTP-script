from ftplib import FTP
from datetime import datetime, timedelta
import openpyxl
import pandas as pd
import pyautogui
import smtplib, ssl
from email.mime.text import MIMEText


try:
    ftp_host = 'ek-product-data.ek-fileserver.de'
    ftp_user = 'compravo'
    ftp_pass = 'Ue76!3hh'

    ftp_host2 = 'sftp3.inwebs.com'
    ftp_port2 = 12022
    ftp_dir2 = '/40010/out/Bestand'
    ftp_user2 = 'compravo'
    ftp_pass2 = 'Adk!2390AmLopEzt!23'  
    # FTP-Verbindung herstellen
    ftp = FTP('ftp.example.com')
    ftp.login(user='username', passwd='password')

    folders_to_check = ['/folder1', '/folder2']

    days_to_keep = 10

    def delete_old_files(folder):
        ftp.cwd(folder)
        files = ftp.nlst()
        for file in files:
            if file.endswith('.txt'):
                file_mod_time = ftp.sendcmd('MDTM ' + file)
                file_mod_time = datetime.strptime(file_mod_time[4:], "%Y%m%d%H%M%S")
                if file_mod_time < datetime.now() - timedelta(days=days_to_keep):
                    print(f"Lösche {file}")
                    ftp.delete(file)

    for folder in folders_to_check:
        delete_old_files(folder)

    ftp.quit()
except:
    def sendEmail():
        smtp_server = "smtp.office365.com"
        port = 587
        sender_email = "media@ek-servicegroup.com"
        password = 'Start123'  
        receiver_email = ["j.krumpholz@ek-retail.com", "f.hahn@ek-retail.com", "m.ramoeller@ek-retail.com"]
        msg = MIMEText("""body""")

        msg['Subject'] = "Fehler beim Löschen von den Datein!"
        msg['From'] = sender_email
        msg['To'] = ", ".join(receiver_email)

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls(context=context)
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            print("E-Mail wurde erfolgreich gesendet.")
        except Exception as e:
            print("Fehler beim Senden der E-Mail:", str(e))

sendEmail()

