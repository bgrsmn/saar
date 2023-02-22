import pymysql
import xml.etree.ElementTree as ET

# Establishing the database connection
conn = pymysql.connect(host='X.X.X.X', user='xxxx', password='xxxxxx', db='xxxxxxx')

if conn.open:
    print("Veritabanı bağlantısı başarılı.")
else:
    print("Veritabanı bağlantısı başarısız.")

kategori_sozluk = {}
print(type(kategori_sozluk))
try:
    with conn.cursor() as cursor:
        # XML data is pulled from CONF_CRR_CATEGORY table
        cursor.execute("SELECT DATA FROM cc_store WHERE STORETYPE = 'CONF_CRR_CATEGORY'")
        # XML data is processed for each row
        for row in cursor:
            xml_data = row[0]
            # The id and name values in XML are pulled
            root = ET.fromstring(xml_data)
            for category in root.findall('category'):
                category_id = category.get('id')
                category_name = category.get('name')
                if category_name is not None:
                    kategori_sozluk[category_id] = category_name

finally:
    # Closing the database connection
    conn.close()

print(kategori_sozluk)
