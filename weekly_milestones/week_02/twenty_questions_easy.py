
import json

def is_answer(node):
    return len(node) == 1


f = open('questions.json')
content = f.read()
node = json.loads(content)
#

finished = False

while not finished:
    print(node['text'])

    if is_answer(node):
        finished = True
    else:
        answer = input()
        if answer.upper() in ['yes', 'y']:
            node = node['no']
        else:
            node = node['yes']
