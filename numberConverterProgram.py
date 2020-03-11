# numberConvertProgram.py - converts 16-bit unsigned binary
# to/from decimal and hexadecimal, and converts decimal to/from
# 16-bit 2's complement signed

# dict used for converting to/from bin and hex
binToHexValues = {
    "0000": "0",
    "0001": "1",
    "0010": "2",
    "0011": "3",
    "0100": "4",
    "0101": "5",
    "0110": "6",
    "0111": "7",
    "1000": "8",
    "1001": "9",
    "1010": "A",
    "1011": "B",
    "1100": "C",
    "1101": "D",
    "1110": "E",
    "1111": "F",
}

###### USER INPUT FUNCTIONS ######
def selectConversionMode():
    print("Input number of desired conversion:")
    print("1 - 16 bit binary to decimal\n"
          + "2 - decimal to 16 bit binary\n"
          + "3 - 16 bit binary to hex\n"
          + "4 - hex to 16 bit binary\n"
          + "5 - 16 bit binary 2's to decimal\n"
          + "6 - decimal to 16 bit binary 2's")
    # Get user selection and return if compatable
    while True:
        selection = input()
        try:
            if(1 <= int(selection) <=6):
                return selection
            else:
                print("Invalid selection, please select 1-6")
        except ValueError:
            print("Invalid selection, please select 1-6")

def getNumberToConvert():
    print("Please input number to convert:")
    # upper is used here for hex values
    return input().upper()

###### NUMBER CHECKING FUNCTIONS ######
def checkBinary(numberToConvert):
    try:
        int(numberToConvert, 2)
        if len(numberToConvert) == 16:
            return True
        else:
            print("16 bit binary number required")
            return False
    except ValueError:
        print("16 bit binary number required")
        return False

def checkDecimal(numberToConvert):
    try:
        int(numberToConvert, 10)
        if 0 <= int(numberToConvert) <= 2 ** 16:
            return True
        else:
            print("number between 0 and 65535 required")
            return False
    except ValueError:
        print("number between 0 and 65535 required")
        return False

def checkSignedDecimal(numberToConvert):
    try:
        int(numberToConvert, 10)
        if -2 ** 15 <= int(numberToConvert) <= (2 ** 15)-1:
            return True
        else:
            print("number between -32768 and 32767 required")
            return False
    except ValueError:
        print("number between -32768 and 32767 required")
        return False

def checkHex(numberToConvert):
    try:
      int(numberToConvert, 16)
      if len(numberToConvert) == 4:
          return True
      else:
          print("4 digit hex value required")
          return False
    except ValueError:
      print("4 digit hex value required")
      return False

# acts as a switch to check number based on conversion type
def checkNumberByType(conversionType, numberToConvert):
    if conversionType == '1' or conversionType == '3' or conversionType == '5':
        return checkBinary(numberToConvert)
    elif conversionType == '2':
        return checkDecimal(numberToConvert)
    elif conversionType == '6':
        return checkSignedDecimal(numberToConvert)
    elif conversionType == '4':
        return checkHex(numberToConvert)

###### CONVERSION FUNCTIONS ######
def conv16BToHex(numberToConvert):
    # perfom a key/value lookup for every 4 places of binary
    return binToHexValues.get(numberToConvert[:4])  \
        + binToHexValues.get(numberToConvert[4:8])  \
        + binToHexValues.get(numberToConvert[8:12]) \
        + binToHexValues.get(numberToConvert[12:16])

def convHexTo16B(numberToConvert):
    # invert binToHexValues to convert hex to bin
    hexToBinValues = {v: k for k, v in binToHexValues.items()}
    # for each digit of hex perform a key/value lookup
    converted = ""
    for i in range(len(numberToConvert)):
        converted += hexToBinValues.get(numberToConvert[i])
    return converted

def conv16BToDec(numberToConvert):
    converted = 0
    place = 0
    for i in reversed(range(16)):
        if numberToConvert[place] == '1':
            converted = converted + 2 ** i
        place+= 1
    return str(converted)

def convDecTo16B(numberToConvert):
    numberToConvert = int(numberToConvert)
    converted = ""
    for i in reversed(range(16)):
        if numberToConvert / 2 ** i >= 1:
            numberToConvert = numberToConvert - 2 ** i
            converted += '1'
        else:
            converted += '0'
    return converted

# used as a logical NOT for 16B 2's to decimal and vice versa
def reverseBitsIn16B(numberToConvert):
    for i in reversed(range(16)):
        if numberToConvert[i] == '1':
            numberToConvert = numberToConvert[:i] + '0' + numberToConvert[i+1:]
        else:
            numberToConvert = numberToConvert[:i] + '1' + numberToConvert[i+1:]
    return numberToConvert

def conv16B2ToDec(numberToConvert):
    converted = 0

    # if positive, simply convert as a normal binary number
    if numberToConvert[0] == '0':
        return conv16BToDec(numberToConvert)

    # subtract 1 from number
    for i in reversed(range(16)):
        if numberToConvert[i] == '0':
            numberToConvert = numberToConvert[:i] + '1' + numberToConvert[i+1:]
        else:
            numberToConvert = numberToConvert[:i] + '0' + numberToConvert[i+1:]
            break

    # reverse 1s and 0s
    numberToConvert = reverseBitsIn16B(numberToConvert)

    # convert to decimal format
    converted = int(conv16BToDec(numberToConvert))

    return str(converted * -1)

def convDecTo16B2(numberToConvert):
    # check if number is negative and reverse sign if so
    negative = int(numberToConvert) < 0
    if negative:
        numberToConvert = numberToConvert[1:]

    # convert decimal to standard binary
    converted = convDecTo16B(numberToConvert)

    # if negative, reverse each bit (1's complement)
    if negative:
        converted = reverseBitsIn16B(converted)
        # after reversing the bits we add one (2's complement)
        for i in reversed(range(16)):
            if converted[i] == '1':
                converted = converted[:i] + '0' + converted[i+1:]
            else:
                converted = converted[:i] + '1' + converted[i+1:]
                break

    return converted


###### PROGRAM LOOP ######
while __name__ == '__main__':
    conversionType = selectConversionMode()
    # loop until user inputs a correctly formatted number
    while True:
        numberToConvert = getNumberToConvert()
        if(checkNumberByType(conversionType, numberToConvert) == True):
            break
    # perform and print conversion based on selected conversion
    if (conversionType == '1'):
        print(conv16BToDec(numberToConvert))
    elif (conversionType == '2'):
        print(convDecTo16B(numberToConvert))
    elif (conversionType == '3'):
        print(conv16BToHex(numberToConvert))
    elif (conversionType == '4'):
        print(convHexTo16B(numberToConvert))
    elif (conversionType == '5'):
        print(conv16B2ToDec(numberToConvert))
    elif (conversionType == '6'):
        print(convDecTo16B2(numberToConvert))
    else:
        print("conversion mode unknown. try again.")
