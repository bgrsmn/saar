import pymysql
import os

conn = pymysql.connect(host='X.X.X.X', user='xxxxx', password='xxxxxx', db='xxxxxxx')

if conn.open:
    print("Veritabanı bağlantısı başarılı.")
else:
    print("Veritabanı bağlantısı başarısız.")

dizin = r"/root/rulestest"
dosyalar = os.listdir(dizin)

cursor = conn.cursor()

# en yüksek kural ID'sini bul
cursor.execute("SELECT * FROM cc_store WHERE STORETYPE = 'CONF_CRR_PLUGIN' ORDER BY id DESC LIMIT 0, 1")
data = cursor.fetchone()
print(data)
if data is not None:
    print(type(data[1]))
    count = int(data[1])
else:
    count = 0

for dosya in dosyalar:
    dosya_yolu = os.path.join(dizin, dosya)
    if os.path.isfile(dosya_yolu):
        veri = ""
        with open(dosya_yolu, "r") as f:
            veri = f.read()
            # Verileri burada kullanabilirsiniz
        print(veri)
        print("------------------------------------------")
        sql = "INSERT INTO cc_store (NAME, STORETYPE, ISSYSTEM, DATA, ENTERDATE, DESCRIPTION, VIEWRIGHT, EDITRIGHT, ISDELETED) VALUES (%s, 'CONF_CRR_PLUGIN', 0, %s, '2022-09-22 17:00:00', NULL, NULL, NULL, NULL)"
        cursor.execute(sql, (str(count + 1), veri))
        conn.commit()
    count += 1
# Veritabanı bağlantısının kapatılması
conn.close()
