import ftplib
import openpyxl
import csv
import pandas as pd
import pyautogui

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

# CSV-Datei herunterladen
with open(local_csv_file, 'wb') as local_file:
    ftp.retrbinary('RETR ' + remote_filename, local_file.write)

# CSV-Datei bearbeiten
new_rows = []
with open(local_csv_file, 'r', newline='' ) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';',)
    fieldnames = ['H;', 'INVRPT;', 'Debitor;', 'GLN;', 'DatRpt;', 'Ek Artikelnummer', ';EANUPC', 'EANTyp;', 'verf;']
    writer = csv.DictWriter(csvfile, fieldnames= fieldnames, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    
    for row in reader:
        new_row = {
            'H;': ';',
            'INVRPT;': ';',
            'Debitor;': ';',
            'GLN;': ';',
            'DatRpt;': '',
            'Ek Artikelnummer': ';' +  row['Artikel_Nr'],
            ';EANUPC;': ';' + row['EAN'],
            'EANTyp;': ';' + ';',
            'verf;': row['BSTD']
        }
        new_rows.append(new_row)

# CSV-Datei mit den neuen Spalten speichern
with open(local_csv_file, 'w', newline='') as csvfile:
    fieldnames = ['H;', 'INVRPT;', 'Debitor;', 'GLN;', 'DatRpt;', 'Ek Artikelnummer', ';EANUPC;', 'EANTyp;', 'verf;']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

# CSV-Datei zurück auf den FTP-Server hochladen
with open(local_csv_file, 'rb') as local_file:
    ftp2.storbinary('STOR ' + local_filename, local_file)

# FTP-Verbindung schließen
ftp.quit()