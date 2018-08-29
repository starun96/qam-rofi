import os, json

with open('./config.json', 'r') as read_file:
    data = json.load(read_file)

for major_options in data:
    print(major_options)