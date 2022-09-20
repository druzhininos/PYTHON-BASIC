"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""


def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words

# generate_words()
print("Running generate_words")
lst = generate_words()
print(lst)

# file1.txt
print("Generating file1.txt")
f1 = open('file1.txt', 'w', encoding="utf-8")
for word in lst:
    print(word, file = f1, end = '\n')
f1.close()

# file2.txt
print("Generating file2.txt")

lst.reverse() # reversing list

f2 = open('file2.txt', 'w', encoding="cp1252")
for word in lst:
    print(word, file = f2, end = ',')
if f2.tell():
    f2.seek(f2.tell() - 1, 0) # moving cursor 1byte left in f2
    f2.truncate() # deleting the last comma symbol
f2.close()
