import ftplib
import openpyxl
import csv
import pandas as pd


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


df = pd.read_csv(local_filename, sep=',')
print(df.columns)


df[';H;'] = ''
df[';H;'] = df[';H;'].str.replace(',', '')
df[';INVRPT;'] = ''
df[';Debitor;'] = ''
df[';GLN;'] = ''
df[';DatRpt;'] = ''

df.rename(columns={'EAN': 'EK Artikelnummer'}, inplace=True)
df.rename(columns={'Artikel_Nr': 'EANUPC'}, inplace=True)


transformed_filename = 'BESTAND_EK_transformed.csv'
df.to_csv(transformed_filename, index=False)

df = pd.read_csv(transformed_filename)
df = df.astype(str)
df = df.apply(lambda x: x.str.replace('nan', '//'))
df.to_csv(transformed_filename, index=False)



with open(transformed_filename, 'rb') as transformed_file:
    ftp2.storbinary('STOR ' + transformed_filename, transformed_file)

ftp.quit()
ftp2.quit()

print("Operation erfolgreich abgeschlossen.")
