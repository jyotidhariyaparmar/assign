from collections import Counter

def build_encoding(text):
    counter = Counter(text)
    characters = [char for char, _ in counter.most_common()]
    
    codes = []
    charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
    
    for c in charset:
        codes.append(c)
   
    if len(characters) > len(codes):
        for c1 in charset:
            for c2 in charset:
                codes.append(c1 + c2)
                if len(codes) >= len(characters):
                    break
            if len(codes) >= len(characters):
                break

    encoding = {char: code for char, code in zip(characters, codes)}
    return encoding

def compress(text, encoding):
    return ''.join(encoding[c] for c in text)

# Reverse the encoding
def build_decoding(encoding):
    return {v: k for k, v in encoding.items()}

def decompress(encoded, decoding):
    result = []
    buffer = ''
    max_code_len = max(len(code) for code in decoding)

    i = 0
    while i < len(encoded):
        buffer += encoded[i]
        if buffer in decoding:
            result.append(decoding[buffer])
            buffer = ''
        i += 1
    return ''.join(result)

if __name__ == '__main__':
    text = ("Marley was dead: to begin with. There is no doubt whatever about that. The register of his burial was signed by the clergyman, the clerk, "
            "the undertaker, and the chief mourner. Scrooge signed it: and Scrooge’s name was good upon ’Change, for anything he chose to put his hand to. "
            "Old Marley was as dead as a door-nail. Mind! I don’t mean to say that I know, of my own knowledge, what there is particularly dead about a "
            "door-nail. I might have been inclined, myself, to regard a coffin-nail as the deadest piece of ironmongery in the trade. But the wisdom of our "
            "ancestors is in the simile; and my unhallowed hands shall not disturb it, or the Country’s done for. You will therefore permit me to repeat, "
            "emphatically, that Marley was as dead as a door-nail.")

    encoding = build_encoding(text)
    encoded = compress(text, encoding)
    decoding = build_decoding(encoding)
    decoded = decompress(encoded, decoding)
    # print("Original:", text[:100], "...\n")
    # print("Encoded:", encoded[:100], "...\n")
    # print("Decoded:", decoded[:100], "...\n")
    print("Original:", text, "\n")
    print("Encoded:", encoded, "\n")
    print("Decoded:", decoded, "\n")
    print("Match:", decoded == text)
