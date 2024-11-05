import sys

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
    print(f"Encoded Text: {encoded_text}")
    print(''*20)    
    print(f"Histogramm {str(caesar_cypher.string_histogram(text))}") #+ str(caesar_cypher.string_histogram(text)))
    print(''*20)
    print(f"Frequency {str(caesar_cypher.frequencies(text))}")
    print(''*20)
    print(''*20)
    decoded_text = caesar_cypher.crack_caesar("I know that virtue to be in you, Brutus, As well as I do know your outward favour. Well, honour" +
    "is the subject of my story. I cannot tell what you and other men Think of this life; but," +
    "for my single self, I had as lief not be as live to be In awe of such a thing as I myself. I was " +
    "born free as Caesar; so were you: We both have fed as well, and we can both Endure the " +
    "winter's cold as well as he: For once, upon a raw and gusty day, The troubled Tiber chafing " +
    "with her shores, Caesar said to me 'Darest thou, Cassius, now Leap in with me into this angry " +
    "flood, And swim to yonder point?' Upon the word, Accoutred as I was, I plunged in And " +
    "bade him follow; so indeed he did. The torrent roar'd, and we did buffet it With lusty sinews, " +
    "throwing it aside And stemming it with hearts of controversy; But ere we could arrive the " +
    "point proposed, Caesar cried 'Help me, Cassius, or I sink!' I, as Aeneas, our great ancestor," +
    "Did from the flames of Troy upon his shoulder The old Anchises bear, so from the waves of " +
    "Tiber Did I the tired Caesar. And this man Is now become a god, and Cassius is A wretched " +
    "creature and must bend his body, If Caesar carelessly but nod on him. He had a fever when " +
    "he was in Spain, And when the fit was on him, I did mark How he did shake: 'tis true, this " +
    "god did shake; His coward lips did from their colour fly, And that same eye whose bend doth " +
    "awe the world Did lose his lustre: I did hear him groan: Ay, and that tongue of his that bade " +
    "the Romans Mark him and write his speeches in their books, Alas, it cried 'Give me some " +
    "drink, Titinius,' As a sick girl. Ye gods, it doth amaze me A man of such a feeble temper " +
    "should So get the start of the majestic world And bear the palm alone.", 
    "Reu jf zk zj. Wfi kyzj kzdv Z nzcc cvrmv pfl: Kf-dfiifn, zw pfl gcvrjv kf jgvrb nzky dv, Z nzcc tfdv yfdv kf pfl; fi, zw pfl nzcc, Tfdv yfdv kf dv, reu Z nzcc nrzk wfi pfl.")
    print(decoded_text)


class CaesarCypher:

    CHR_OFF_SET_UPPER = 65
    CHR_OFF_SET_LOWER = 97
    LENGH_ALPHABET = 26
    
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
    
    def decode_text(self, text, key):
        return self.encode_text(text, -key)
    
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
    
    def calculate_chi_square(self, observed, expected):

        chi_square = 0
        for charInt in range(CaesarCypher.CHR_OFF_SET_LOWER, CaesarCypher.CHR_OFF_SET_LOWER + CaesarCypher.LENGH_ALPHABET):
            char = chr(charInt)
            #get the counted values for each character
            observed_count = observed.get(char, 0)
            expected_count = expected.get(char, 0)
            #avoid division by zero
            chi_square += (observed_count - expected_count) ** 2 / expected_count if expected_count != 0 else 0
        return chi_square

    #try to encode the decoded text using chi-square algorithm
    def crack_caesar(self, example_text, encrypted_text):

        example_histogram = self.string_histogram(example_text)
        example_length = len(example_text)
        #put expcted frequencies in a dictionary
        expected_frequencies = {char: count / example_length for char, count in example_histogram.items()}

        closest_shift = 0
        #set the chi square to positive infinity, to have the highest value
        minimum_chi_square = float('inf')

        for shift in range(CaesarCypher.LENGH_ALPHABET):

            shifted_text = self.decode_text(encrypted_text, shift)
            evaluated_histogram = self.string_histogram(shifted_text)

            calculated_chi_square = self.calculate_chi_square(evaluated_histogram, expected_frequencies)

            if calculated_chi_square < minimum_chi_square:
                minimum_chi_square = calculated_chi_square
                closest_shift = shift

        return self.decode_text(encrypted_text, closest_shift)


    def frequencies(self, text) :
        
        hist = self.string_histogram(text)
        text_length = len(text.replace(" ", ""))
        
        freq = [0] * CaesarCypher.LENGH_ALPHABET
        idx = 0

        for char in range(CaesarCypher.CHR_OFF_SET_LOWER, CaesarCypher.CHR_OFF_SET_LOWER + CaesarCypher.LENGH_ALPHABET):
            if (chr(char) in hist):
                freq[idx] = hist[chr(char)] / text_length
            idx += 1

        return freq
    


if __name__ == "__main__":
    main(sys.argv)
