import ftplib
import openpyxl
import csv
import pandas as pd
import pyautogui

try:
    ftp_host = 'ek-product-data.ek-fileserver.de'
    ftp_user = 'compravo'
    ftp_pass = 'Ue76!3hh'

    ftp_host2 = 'sftp3.inwebs.com'
    ftp_port2 = 12022
    ftp_dir2 = '/40010/out/Bestand'
    ftp_user2 = 'compravo'
    ftp_pass2 = 'Adk!2390AmLopEzt!23'


    remote_filename = 'EK_stock.csv'
    local_filename = 'BESTAND_EK.csv'


    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)


    with open(local_filename, 'wb') as local_file:
        ftp.retrbinary('RETR ' + remote_filename, local_file.write)


    ftp2 = ftplib.FTP_TLS(ftp_host2, ftp_user2, ftp_pass2)
    ftp2.cwd(ftp_dir2)


    local_csv_file = 'lokal.csv'


    with open(local_csv_file, 'wb') as local_file:
        ftp.retrbinary('RETR ' + remote_filename, local_file.write)


    new_rows = []
    with open(local_csv_file, 'r', newline='' ) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        fieldnames = ['H', 'INVRPT', 'Debitor', 'GLN', 'DatRpt', 'Ek Artikelnummer', 'EANUPC', 'EANTyp', 'verf']
        
        for row in reader:
            cleaned_row = [cell.replace(',', '') for cell in row] 
            new_row = {
                'H': '',
                'INVRPT': '',
                'Debitor': '',
                'GLN': '',
                'DatRpt': '',
                'Ek Artikelnummer': cleaned_row[1],
                'EANUPC': cleaned_row[0],
                'EANTyp': '',
                'verf': cleaned_row[3]
            }
            new_rows.append(new_row)


    counter = 0
    with open(local_csv_file, 'w', newline='') as csvfile:
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in new_rows:
            if counter != 0:
                writer.writerow(row)
            counter += 1

    with open(local_csv_file, 'rb') as local_file:
        ftp2.storbinary('STOR ' + local_filename, local_file)


    ftp.quit()

except:
    print('Fehler')
