import xml.etree.ElementTree as ET
import pymysql
import os

# Opening the database connection
conn = pymysql.connect(host='172.17.7.59', user='clog', password='Ctech77.77clog', db='cryptosimpir')

if conn.open:
    print("Database connection successful.")
else:
    print("Database connection failed.")

# Dictionary to hold categories
kategori_sozluk = {}

try:
    with conn.cursor() as cursor:
        # Fetch XML data from the CONF_CRR_CATEGORY table
        cursor.execute("SELECT DATA FROM cc_store WHERE STORETYPE = 'CONF_CRR_CATEGORY'")
        # Processing XML data for each row
        for row in cursor:
            xml_data = row[0]
            # Extracting id and name values from XML
            root = ET.fromstring(xml_data)
            for category in root.findall('category'):
                category_id = category.get('id')
                category_name = category.get('name')
                if category_name is not None:
                   kategori_sozluk[category_id] = category_name

finally:
    # Closing the database connection
    conn.close()

conn = pymysql.connect(host='172.17.7.59', user='clog', password='Ctech77.77clog', db='cryptosimpir')

if conn.open:
    print("Database connection successful.")
else:
    print("Database connection failed.")

root_dizin = r"/root/ruletest"
kategori_dosyalari = {}

cursor = conn.cursor()

# Find the highest rule ID
cursor.execute("SELECT * FROM cc_store WHERE STORETYPE = 'CONF_CRR_PLUGIN' ORDER BY id DESC LIMIT 0, 1")
data = cursor.fetchone()

if data is not None:   
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

                # Get the rule name from the file name
                kural_adi = dosya.split(".")[0]

                # Check if a rule with the same name already exists in the database
                cursor.execute("SELECT * FROM cc_store WHERE DATA LIKE '%name=\"{}\"%' AND STORETYPE = 'CONF_CRR_PLUGIN'".format(kural_adi))
                data = cursor.fetchone()
                if data is not None:
                    print(f"Rule {rule_name} already exists in the database.")
                else:
                    # Add the new rule to the database
                    cursor.execute("INSERT INTO cc_store (NAME, STORETYPE, ISSYSTEM, DATA, ENTERDATE, DESCRIPTION, VIEWRIGHT, EDITRIGHT, ISDELETED) VALUES (%s, 'CONF_CRR_PLUGIN', 0, %s, '2022-09-22 17:00:00', NULL, NULL, NULL, NULL)", (str(count + 1), veri))
                    conn.commit()
                    count += 1
                    if kategori not in kategori_dosyalari:
                       kategori_dosyalari[kategori] = [dosya_yolu]
                    else:
                       kategori_dosyalari[kategori].append(dosya_yolu)
                    print(f"Rule {rule_name} added.")

# Database categories


# Check database categories for each category in the sample list
for kategori in kategori_dosyalari.keys():
    for category_id, category in kategori_sozluk.items():
        if category == kategori:
            for path in kategori_dosyalari[kategori]:
              # Parsing the XML file
              tree = ET.parse(path)
              root = tree.getroot()
              for plugin in root.iter('rule'):
                 # Process only those with a specific category
                 categoryid = plugin.find('category_id')
                 # If the category_id tag does not exist, create the tag and set it to 10001
                 if categoryid is None:
                    category = ET.SubElement(plugin, 'category_id')
                    category.text = category_id
                    #print("category_id:{}".format(str(category_id)))
                 else:
                    categoryid.text = category_id
              # Save the XML file
              tree.write(path)
              
			  
dizin = r"/root/ruletest"
dosyalar = os.listdir(dizin)

cursor = conn.cursor()

# Find the highest rule ID
cursor.execute("SELECT * FROM cc_store WHERE STORETYPE = 'CONF_CRR_PLUGIN' ORDER BY id DESC LIMIT 0, 1")
data = cursor.fetchone()

if data is not None:
    count = int(data[1])
else:
    count = 0

for dosya in dosyalar:
    dosya_yolu = os.path.join(dizin, dosya)
    if os.path.isfile(dosya_yolu):
        veri = ""
        with open(dosya_yolu, "r") as f:
            veri = f.read()
            # You can use the data here
        sql = "INSERT INTO cc_store (NAME, STORETYPE, ISSYSTEM, DATA, ENTERDATE, DESCRIPTION, VIEWRIGHT, EDITRIGHT, ISDELETED) VALUES (%s, 'CONF_CRR_PLUGIN', 0, %s, '2022-09-22 17:00:00', NULL, NULL, NULL, NULL)"
        cursor.execute(sql, (str(count + 1), veri))
        conn.commit()
    count += 1


# Closing the database connection

conn.close()
