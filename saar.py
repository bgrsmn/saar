import xml.etree.ElementTree as ET
import pymysql
import os

# Veritabanı bağlantısının açılması
conn = pymysql.connect(host='X.X.X.X', user='XXXX', password='XXXX', db='XXXX')

if conn.open:
    print("Veritabanı bağlantısı başarılı.")
else:
    print("Veritabanı bağlantısı başarısız.")


kategori_sozluk = {}
print(type(kategori_sozluk))
try:
    with conn.cursor() as cursor:
        # CONF_CRR_CATEGORY tablosundan xml verileri çekilir
        cursor.execute("SELECT DATA FROM cc_store WHERE STORETYPE = 'CONF_CRR_CATEGORY'")
        # Her bir satır için XML verileri işlenir
        for row in cursor:
            xml_data = row[0]
            # XML içindeki id ve name değerleri çekilir
            root = ET.fromstring(xml_data)
            for category in root.findall('category'):
                category_id = category.get('id')
                category_name = category.get('name')
                if category_name is not None:
                   kategori_sozluk[category_id] = category_name

finally:
    # Veritabanı bağlantısının kapatılması
    conn.close()


#print(kategori_sozluk)


conn = pymysql.connect(host='X.X.X.X', user='XXXX', password='XXXX', db='XXXX')

if conn.open:
    print("Veritabanı bağlantısı başarılı.")
else:
    print("Veritabanı bağlantısı başarısız.")

root_dizin = r"/root/ruletest"
kategori_dosyalari = {}

cursor = conn.cursor()

# en yüksek kural ID'sini bul
cursor.execute("SELECT * FROM cc_store WHERE STORETYPE = 'CONF_CRR_PLUGIN' ORDER BY id DESC LIMIT 0, 1")
data = cursor.fetchone()
#print(data)
if data is not None:
    #print(type(data[1]))
    count = int(data[1])
else:
    count = 0

for kategori in os.listdir(root_dizin):
    kategori_dizini = os.path.join(root_dizin, kategori)
    if os.path.isdir(kategori_dizini):
        dosyalar = os.listdir(kategori_dizini)
        for dosya in dosyalar:
            dosya_yolu = os.path.join(kategori_dizini, dosya)
            if os.path.isfile(dosya_yolu):
                veri = ""
                with open(dosya_yolu, "r") as f:
                    veri = f.read()
                    # Verileri burada kullanabilirsiniz
                #print(veri)
                #print("------------------------------------------")

                # Kural adını dosya isminden al
                kural_adi = dosya.split(".")[0]

                # Veritabanında aynı isimde bir kural var mı diye kontrol et
                cursor.execute("SELECT * FROM cc_store WHERE DATA LIKE '%name=\"{}\"%' AND STORETYPE = 'CONF_CRR_PLUGIN'".format(kural_adi))
                data = cursor.fetchone()
                if data is not None:
                    print(f"Kural {kural_adi} zaten veritabanında var.")
                else:
                    # Yeni kuralı veritabanına ekle
                    cursor.execute("INSERT INTO cc_store (NAME, STORETYPE, ISSYSTEM, DATA, ENTERDATE, DESCRIPTION, VIEWRIGHT, EDITRIGHT, ISDELETED) VALUES (%s, 'CONF_CRR_PLUGIN', 0, %s, '2022-09-22 17:00:00', NULL, NULL, NULL, NULL)", (str(count + 1), veri))
                    conn.commit()
                    count += 1
                    if kategori not in kategori_dosyalari:
                       kategori_dosyalari[kategori] = [dosya_yolu]
                    else:
                       kategori_dosyalari[kategori].append(dosya_yolu)
                    print(f"Kural {kural_adi} eklendi.")

#Bağlantıyı Kapat
#conn.close()

# veritabanındaki kategori listesi

#print(kategori_sozluk)


#print(kategori_dosyalari)

# örnek listenin her bir kategorisi için veritabanındaki kategorileri kontrol et
for kategori in kategori_dosyalari.keys():
    for category_id, category in kategori_sozluk.items():
        if category == kategori:
            for path in kategori_dosyalari[kategori]:
              # XML dosyasının okunması
              tree = ET.parse(path)
              root = tree.getroot()
              for plugin in root.iter('rule'):
                 # Sadece belirli bir kategoriye sahip olanları işleme alma
                 categoryid = plugin.find('category_id')
                 # Eğer category_id etiketi yoksa, etiketi oluşturma ve 10001 değerini verme
                 if categoryid is None:
                    category = ET.SubElement(plugin, 'category_id')
                    category.text = category_id
                    print("category_id:{}".format(str(category_id)))
                 else:
                    categoryid.text = category_id
              print("------------")
              # XML dosyasını kaydetme
              tree.write(path)
              #print(ET.tostring(root))


dizin = r"/root/ruletest"
dosyalar = os.listdir(dizin)

cursor = conn.cursor()

# en yüksek kural ID'sini bul
cursor.execute("SELECT * FROM cc_store WHERE STORETYPE = 'CONF_CRR_PLUGIN' ORDER BY id DESC LIMIT 0, 1")
data = cursor.fetchone()
#print(data)
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
        #print(veri)
        print("------------------------------------------")
        sql = "INSERT INTO cc_store (NAME, STORETYPE, ISSYSTEM, DATA, ENTERDATE, DESCRIPTION, VIEWRIGHT, EDITRIGHT, ISDELETED) VALUES (%s, 'CONF_CRR_PLUGIN', 0, %s, '2022-09-22 17:00:00', NULL, NULL, NULL, NULL)"
        cursor.execute(sql, (str(count + 1), veri))
        conn.commit()
    count += 1


# Veritabanı bağlantısının kapatılması

conn.close()
