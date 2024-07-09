import subprocess
import re
import json
import csv
import subprocess
import sqlite3
import random
import sys
ip=[]

user_id = sys.argv[1]
user_server_name = sys.argv[2]
user_host = sys.argv[3]


command = "x-ui stop"
process = subprocess.Popen(
    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print("Error executing command:", command)
else:
    print(stdout.decode('utf-8'))
# Open the database file
conn = sqlite3.connect('/etc/x-ui/x-ui.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Construct the SQL query to retrieve the value of xrayTemplateConfig
query = "SELECT value FROM settings WHERE key = 'xrayTemplateConfig'"

# Execute the query and fetch the result 
cursor.execute(query)
result = cursor.fetchone()

# Close the database connection


# Extract the value from the result tuple
if result is not None:
    value = result[0]
    print("The current value of xrayTemplateConfig is:", value)
else:
    print("xrayTemplateConfig not found in the database.")


value = json.loads(value)
value["outbounds"][0]["streamSettings"]["wsSettings"]["headers"]["Host"] =  user_host
value["outbounds"][0]["streamSettings"]["tlsSettings"]["serverName"] = user_server_name
value["outbounds"][0]["settings"]["vnext"][0]["users"][0]["id"] = user_id
value = json.dumps(value,indent=4)
print(value)

query = "UPDATE settings SET value = ? WHERE key = 'xrayTemplateConfig'"

# Execute the query with the new value
cursor.execute(query, (value,))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

command = "x-ui start"
process = subprocess.Popen(
    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print("Error executing command:", command)
else:
    print(stdout.decode('utf-8'))
