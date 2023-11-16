charDict = {}

def loadKey():
    if len(list(charDict.keys())) > 0: ##Don't ask comparing it to an empty dic didn't work
        return
    
    keyFileName = 'utils/strlength.txt'
    
    with open(keyFileName, encoding="utf8") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    
    for line in lines:
        i = 0
        total = ""
        key = ""
        for char in line:
            if line[0] + line[1] == "//":
                break
            elif i == 0:
                key = char
            elif i != 1:
                total += char
            try:
                charDict[key] = float(total)
            except:
                1 + 1
            i += 1

def calculate(inputString):
    total = 0.0
    for char in inputString:
        if char == "'":
            char = "’"
        try:
            total += charDict[char]
        except:
            total += charDict[" "]
    return total