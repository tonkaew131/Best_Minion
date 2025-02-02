import json


def openJSONFile(fileName):
    with open(fileName) as jsonFile:
        data = json.load(jsonFile)
        return(data)


def openTextFile(fileName):
    with open(fileName) as textFile:
        return(textFile.read())


def jsonToArray(json):
    array = []
    for key in json:
        array.append(json[key])
    return(array)

def numberToRoman(number):
    num_map = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
    (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]

    roman = ''
    while number > 0:
        for i, r in num_map:
            while number >= i:
                roman += r
                number -= i

    return roman