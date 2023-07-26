import xml.etree.ElementTree as ET
import pymysql
import os

# Opening the database connection
conn = pymysql.connect(host='X.X.X.X', user='XXXX', password='XXXX', db='XXXX')

if conn.open:
    print("Database connection successful.")
else:
    print("Database connection failed.")

# Dictionary to hold categories
category_dict = {}
print(type(category_dict))
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
                    category_dict[category_id] = category_name

finally:
    # Closing the database connection
    conn.close()

conn = pymysql.connect(host='X.X.X.X', user='XXXX', password='XXXX', db='XXXX')

if conn.open:
    print("Database connection successful.")
else:
    print("Database connection failed.")

root_directory = r"/root/ruletest"
category_files = {}

cursor = conn.cursor()

# Find the highest rule ID
cursor.execute("SELECT * FROM cc_store WHERE STORETYPE = 'CONF_CRR_PLUGIN' ORDER BY id DESC LIMIT 0, 1")
data = cursor.fetchone()
if data is not None:
    count = int(data[1])
else:
    count = 0

for category in os.listdir(root_directory):
    category_directory = os.path.join(root_directory, category)
    if os.path.isdir(category_directory):
        files = os.listdir(category_directory)
        for file in files:
            file_path = os.path.join(category_directory, file)
            if os.path.isfile(file_path):
                data = ""
                with open(file_path, "r") as f:
                    data = f.read()
                    
                # Get the rule name from the file name
                rule_name = file.split(".")[0]

                # Check if a rule with the same name already exists in the database
                cursor.execute("SELECT * FROM cc_store WHERE DATA LIKE '%name=\"{}\"%' AND STORETYPE = 'CONF_CRR_PLUGIN'".format(rule_name))
                data = cursor.fetchone()
                if data is not None:
                    print(f"Rule {rule_name} already exists in the database.")
                else:
                    # Add the new rule to the database
                    cursor.execute("INSERT INTO cc_store (NAME, STORETYPE, ISSYSTEM, DATA, ENTERDATE, DESCRIPTION, VIEWRIGHT, EDITRIGHT, ISDELETED) VALUES (%s, 'CONF_CRR_PLUGIN', 0, %s, '2022-09-22 17:00:00', NULL, NULL, NULL, NULL)", (str(count + 1), data))
                    conn.commit()
                    count += 1
                    if category not in category_files:
                       category_files[category] = [file_path]
                    else:
                       category_files[category].append(file_path)
                    print(f"Rule {rule_name} added.")
                    
# Database categories

# Check database categories for each category in the sample list
for category in category_files.keys():
    for category_id, category_name in category_dict.items():
        if category_name == category:
            for path in category_files[category]:
                # Parsing the XML file
                tree = ET.parse(path)
                root = tree.getroot()
                for plugin in root.iter('rule'):
                    # Process only those with a specific category
                    category_id_element = plugin.find('category_id')
                    # If the category_id tag does not exist, create the tag and set it to 10001
                    if category_id_element is None:
                        category_element = ET.SubElement(plugin, 'category_id')
                        category_element.text = category_id
                        print("category_id:{}".format(str(category_id)))
                    else:
                        category_id_element.text = category_id
                print("------------")
                # Save the XML file
                tree.write(path)
                
directory = r"/root/ruletest"
files = os.listdir(directory)

cursor = conn.cursor()

# Find the highest rule ID
cursor.execute("SELECT * FROM cc_store WHERE STORETYPE = 'CONF_CRR_PLUGIN' ORDER BY id DESC LIMIT 0, 1")
data = cursor.fetchone()

if data is not None:
    print(type(data[1]))
    count = int(data[1])
else:
    count = 0

for file in files:
    file_path = os.path.join(directory, file)
    if os.path.isfile(file_path):
        data = ""
        with open(file_path, "r") as f:
            data = f.read()
               
        print("------------------------------------------")
        sql = "INSERT INTO cc_store (NAME, STORETYPE, ISSYSTEM, DATA, ENTERDATE, DESCRIPTION, VIEWRIGHT, EDITRIGHT, ISDELETED) VALUES (%s, 'CONF_CRR_PLUGIN', 0, %s, '2022-09-22 17:00:00', NULL, NULL, NULL, NULL)"
        cursor.execute(sql, (str(count + 1), data))
        conn.commit()
    count += 1

# Closing the database connection
conn.close()
