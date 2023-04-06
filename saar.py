import xml.etree.ElementTree as ET
import pymysql
import os


# Enter the host address, username, password and database name for database connection
conn = pymysql.connect(host='X.X.X.X', user='XXXX', password='XXXX', db='XXXX')

if conn.open:
    print("Database connection successful.")
else:
    print("Database connection failed.")


category_dictionary = {}

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
                   category_dictionary[category_id] = category_name

finally:
    # Closing the database connection
    conn.close()


# Enter the host address, username, password and database name for database connection
conn = pymysql.connect(host='X.X.X.X', user='XXXX', password='XXXX', db='XXXX')

if conn.open:
    print("Database connection successful.")
else:
    print("Database connection failed.")

# Give the path of the category files you have added
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
        folders = os.listdir(category_directory)
        for file in folders:
            file_path = os.path.join(category_directory, file)
            if os.path.isfile(file_path):
                data = ""
                with open(file_path, "r") as f:
                    data = f.read()
                            
                # Get rule name from filename
                rule_name = file.split(".")[0]

                # Check if there is a rule with the same name in the database
                cursor.execute("SELECT * FROM cc_store WHERE NAME = %s AND STORETYPE = 'CONF_CRR_PLUGIN'", (rule_name,))
                data = cursor.fetchone()
                if data is not None:
                    print(f"Rule {rule_name} already exists in database.")

                if category not in category_files:
                   category_files[category] = [file_path]
                else:
                   category_files[category].append(file_path)

for category in category_files.keys():
    for category_id, category1 in category_dictionary.items():
        if category1 == category:
            for path in category_files[category]:
                # Reading the XML file
                tree = ET.parse(path)
                root = tree.getroot()

                for plugin in root.iter('rule'):
                    # Process only those with a specific category
                    categoryid = plugin.find('category_id')
                    # Adding the category_id tag just below the timeout tag
                    timeout = plugin.find('timeout')
                    if timeout is not None:
                        category_id_element = ET.Element('category_id')
                        category_id_element.text = category_id      
                        timeout_index = list(plugin).index(timeout)
                        plugin.insert(timeout_index + 1, category_id_element)
                    else:
                        # If there is no timeout tag, add it to the end
                        category_id_element = ET.SubElement(plugin, 'category_id')
                        category_id_element.text = category_id
                        plugin.append(category_id_element)

                    # Update or add <CodeStr> tag
                    code_str_element = plugin.find('CodeStr')
                    if code_str_element is not None:
                        code_str_element.text = '<![CDATA[]]>'
                    else:
                        code_str_element = ET.Element('CodeStr')
                        code_str_element.text = '<![CDATA[]]>'
                        plugin.append(code_str_element)

                    # Saving the XML file
                    if os.path.exists(path):
                        os.remove(path)
                    with open(path, 'w', encoding='utf-8') as f:
                       f.write('<?xml version="1.0" encoding="utf-8"?>\n')
                       tree.write(f, encoding="unicode")

for category in os.listdir(root_directory):
    category_directory = os.path.join(root_directory, category)
    if os.path.isdir(category_directory):
        folders = os.listdir(category_directory)
        for file in folders:
            file_path = os.path.join(category_directory, file)
            if os.path.isfile(file_path):
                data = ""
                with open(file_path, "r") as f:
                    data = f.read()
                    # You can use the data here
                    cursor.execute("INSERT INTO cc_store (NAME, STORETYPE, ISSYSTEM, DATA, ENTERDATE, DESCRIPTION, VIEWRIGHT, EDITRIGHT, ISDELETED) VALUES (%s, 'CONF_CRR_PLUGIN', 0, %s, '2022-09-22 17:00:00', NULL, NULL, NULL, NULL)", (str(count + 1), data.replace("&lt;","<").replace("&gt;",">")))
                    conn.commit()
                    count += 1
                    print("{} to the category {} rule file successfully added.".format(category,file))

conn.close()					   
