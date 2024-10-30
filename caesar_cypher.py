import sys
import re

def main(args):

    if ( len(sys.argv) < 3 ):
        print("Usage: CaesarCypher.py <Text> <Key>")
        sys.exit(1)

    text = args[1]
    key =  eval(str(args[2]))
    
    #hint: I tried to remove spaces, but a spce leads to another entry in the args list
    if key == 0: 
        print("Key must not be 0. This does not make sense.")
        sys.exit(1)

    caesar_cypher = CaesarCypher()
    encoded_text = caesar_cypher.encode_text(text, key)
    print("Encoded Text: " + encoded_text)
    print(''*20)    
    print("Histogramm" + str(caesar_cypher.string_histogram(text)))
    print(''*20)
    print("Frequency" + str(caesar_cypher.frequencies(text)))




class CaesarCypher:
    #ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    CHR_OFF_SET_UPPER = 65
    CHR_OFF_SET_LOWER = 97
    LENGH_ALPHABET = 26
    
    #def __init__(self):

    def __encode_char(self, char, key) :
        
        char_ord = ord(char)
        offset = 0
        
        if char.isupper():
            offset = CaesarCypher.CHR_OFF_SET_UPPER
        else:
            offset = CaesarCypher.CHR_OFF_SET_LOWER
        
        return chr((((char_ord + key)-offset) % CaesarCypher.LENGH_ALPHABET) + offset)
         

    def encode_text(self, text, key) :
        
        encoded_text = ""
        
        for char in text:
            if char.isalpha():
                encoded_text += self.__encode_char(char, key)
            else:
                encoded_text += char
        
        return encoded_text
    
    def string_histogram(self, text) :
        
        hist = {}
        for char in text:
            if char.isalpha():
                lower_char = char.lower()
                if lower_char in hist:
                    hist[lower_char] += 1
                else:
                    hist[lower_char] = 1

        return dict(sorted(hist.items()))
    
    def crack_caesar(self, text) :
        
        hist = self.string_histogram(text)
        n = len(text)
        chi = 0

        for char in hist:
            expected = CaesarCypher.ALPHABET.count(char) / len(CaesarCypher.ALPHABET) * n
            chi += (hist[char] - expected) ** 2 / expected
        return chi

    def frequencies(self, text) :
        hist = self.string_histogram(text)
        n = len(text.replace(" ", ""))
        
        freq = [0] * 26
        idx = 0

        for char in range(CaesarCypher.CHR_OFF_SET_LOWER, CaesarCypher.CHR_OFF_SET_LOWER + CaesarCypher.LENGH_ALPHABET):
            if (chr(char) in hist):
                freq[idx] = hist[chr(char)] / n
            idx += 1

        return freq
    


if __name__ == "__main__":
    main(sys.argv)
