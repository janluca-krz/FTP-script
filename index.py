import ftplib
import pandas as pd

# FTP-Zugangsdaten
ftp_host = 'ek-product-data.ek-fileserver.de'
ftp_user = 'compravo'
ftp_pass = 'Ue76!3hh'

ftp_host2 = 'sftp3.inwebs.com'
ftp_port2 = 12022
ftp_dir2 = '/40010/out/Bestand'
ftp_user2 = 'compravo'
ftp_pass2 = 'Adk!2390AmLopEzt!23'

# Dateinamen
remote_filename = 'EK_stock.csv'
local_filename = 'BESTAND_EK.csv'

# Verbindung zum FTP-Server herstellen
ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)

# CSV-Datei herunterladen
with open(local_filename, 'wb') as local_file:
    ftp.retrbinary('RETR ' + remote_filename, local_file.write)

# Verbindung zum zweiten FTP-Server herstellen
ftp2 = ftplib.FTP_TLS(ftp_host2, ftp_user2, ftp_pass2)
ftp2.cwd(ftp_dir2)

# CSV-Datei transformieren
df = pd.read_csv(local_filename, sep=',')
print(df.columns)

# Hier füge die entsprechenden Zuordnungen der Spalten ein
df['H;'] = ''
df['INVRPT;'] = ''
df['Debitor;'] = ''
df['GLN;'] = ''
df['DatRpt;'] = ''

df.rename(columns={'EAN': 'EK Artikelnummer'}, inplace=True)
df.rename(columns={'Artikel_Nr': 'EANUPC'}, inplace=True)

# Transformierte CSV-Datei lokal speichern
transformed_filename = 'BESTAND_EK_transformed.csv'
df.to_csv(transformed_filename, index=False)

# Transformierte CSV-Datei auf den zweiten FTP-Server hochladen
with open(transformed_filename, 'rb') as transformed_file:
    ftp2.storbinary('STOR ' + transformed_filename, transformed_file)

# Verbindung zum FTP-Server schließen
ftp.quit()
ftp2.quit()

print("Operation erfolgreich abgeschlossen.")
