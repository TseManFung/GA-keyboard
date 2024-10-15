import json

jsonData = {}
tempData = {}

def read_file(fileName):
    with open(fileName, 'r') as file:
        content = file.read()
    return content

def input_CNS2UNICODE(content):
    lines = content.split('\n')
    for line in lines:
        if line == '':
            continue
        line = line.split('\t')
        cns = line[0]
        unicode = line[1]
        tempData[cns] = {'unicode': unicode.lower()}

def input_CNS2cangjie(content):
    lines = list(content.split('\n'))
    for line in lines:
        if line == '':
            continue
        line = line.split('\t')
        cangjie = line[1]
        cns = line[0]
        if cns in tempData:
            if 'cangjie' not in tempData[cns]:
                tempData[cns]['cangjie'] = []
            tempData[cns]['cangjie'].append(cangjie)
            jsonData[tempData[cns]['unicode']] = tempData[cns]['cangjie']
        else:
            print(f'Error: {cns} not found in tempData')

def read_json(fileName):
    with open(rf"dataset\cangjie\{fileName}", 'r', encoding='utf-8-sig') as file:
        return json.load(file)

def write_json(fileName):
    with open(fileName, 'w') as file:
        json.dump(jsonData, file, separators=(',', ':'))

def json_process(fileName):
    read_json(fileName)
    data = read_json(fileName)
    for entry in data:
        char = entry['char']
        cangjies = entry['cangjie'].split(', ')
        unicode_val = char.encode('unicode_escape').decode('utf-8').replace('\\u', '')
        for cangjie in cangjies:
            if unicode_val in jsonData:
                if cangjie not in jsonData[unicode_val]:
                    jsonData[unicode_val].append(cangjie)
            else:
                jsonData[unicode_val] = [cangjie]

if __name__ == "__main__":
    input_CNS2UNICODE(read_file('CNS2UNICODE_Unicode BMP.txt'))
    input_CNS2UNICODE(read_file('CNS2UNICODE_Unicode 15.txt'))
    input_CNS2UNICODE(read_file('CNS2UNICODE_Unicode 2.txt'))
    input_CNS2cangjie(read_file('CNS_cangjie.txt'))
    json_process('HKSCS2016.json')
    write_json("dataset\cangjie\unicode2cangjie.json")
    