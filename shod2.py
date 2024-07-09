import subprocess
import re
import json
import csv
import subprocess
import sqlite3
import random
ip=[]

script_path = "./cf.sh"


process = subprocess.Popen(script_path, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)

menu_option = "1\n"  
process.stdin.write(menu_option)
process.stdin.flush()


bandwidth_input = "60\n"
process.stdin.write(bandwidth_input)
process.stdin.flush()


rtt_processes_input = "10\n"
process.stdin.write(rtt_processes_input)
process.stdin.flush()

output, _ = process.communicate()
print (output)


preferred_ip_pattern = r'preferred IP (\d+\.\d+\.\d+\.\d+)'

# Search for the IP address using the regular expression
preferred_ip_match = re.search(preferred_ip_pattern, output)
preferred_ip = preferred_ip_match.group(1)
ip.append(preferred_ip)


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

rep_ip=random.choice(ip)
value = json.loads(value)
value["outbounds"][0]["settings"]["vnext"][0]["address"] = rep_ip
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
