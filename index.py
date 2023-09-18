import ftplib
import pandas as pd

# FTP-Zugangsdaten
ftp_host = 'Server'
ftp_user = 'benutzername'
ftp_pass = 'pass'

ftp_host2 = 'Server'
ftp_user2 = 'benutzername'
ftp_pass2 = 'pass'

# Dateinamen
remote_filename = 'EK_stock.csv'
local_filename = 'BESTAND_EK.csv'

# Verbindung zum FTP-Server herstellen
ftp = ftplib.FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)

ftp2 = ftplib.FTP(ftp_host2)
ftp2.login(ftp_user2, ftp_pass2)

# CSV-Datei herunterladen
with open(local_filename, 'wb') as local_file:
    ftp.retrbinary('RETR ' + remote_filename, local_file.write)

# CSV-Datei transformieren
df = pd.read_csv(local_filename)
df['H'] = df['']
df['INVRPT'] = df['']
df['Debitor'] = df['']
df['GLN'] = df['']
df['DatRpt'] = df['']

# Umbenennen der Spalte "EAN" in "EK Artikelnummer"
df.rename(columns={'EAN': 'EK Artikelnummer'}, inplace=True)
df['EK Artikelnummer'] = local_filename['EK Artikelnummer']

# Umbenennen der Spalte "Artikel_Nr" in "EANUPC"
df.rename(columns={'Artikel_Nr': 'EANUPC'}, inplace=True)
df['EANUPC'] = local_filename['EANUPC']
df['EANTyp'] = df['']
df['Verf'] = df['']
df['KZ-Planlieferz'] = df['']
df['H'] = df['']


# Transformierte CSV-Datei lokal speichern
transformed_filename = 'BESTAND_EK.csv'
df.to_csv(transformed_filename, index=False)

# Transformierte CSV-Datei auf den FTP-Server hochladen
with open(transformed_filename, 'rb') as transformed_file:

    ftp2.storbinary('STOR ' + transformed_filename, transformed_file)

# Verbindung zum FTP-Server schließen
ftp.quit()
ftp2.quit()

print("Operation erfolgreich abgeschlossen.")