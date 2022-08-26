"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""

contents = []

def read_file(filename):
    f = open(filename, 'r')
    contents.append(f.read())
    f.close()
    return contents

import os
path = './files'
files = os.listdir(path)

for file in files:
    if os.path.isfile(os.path.join(path, file)):
        read_file(os.path.join(path, file))

print(contents)

def write_file(filename, data):
    f = open(filename, 'w')
    for word in data:
        print(word, file = f, end = ',')
    if f.tell():
        f.seek(f.tell() - 1, 0)
        f.truncate()
    f.close()

write_file('result.txt', contents)

print("Task finished.")
