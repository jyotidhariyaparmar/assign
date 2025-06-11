from collections import Counter

def build_encoding(text):
    counter = Counter(text)
    most_common = [char for char, _ in counter.most_common()]

    encoding = {}
    index = 0

    def next_code():
        nonlocal index
        if index < 15:
            code = hex(index)[2:]
        else:
            chain = []
            temp = index - 15
            while True:
                nibble = temp & 0xF
                temp >>= 4
                chain.append(hex(nibble)[2:])
                if temp == 0:
                    break
            # Build code: 'f' repeated len(chain) times + chain nibbles reversed
            code = 'f' * len(chain) + chain[-1]
            for c in reversed(chain[:-1]):
                code += c
        index += 1
        return code

    for char in most_common:
        encoding[char] = next_code()

    return encoding

def compress(text, encoding):
    return ''.join(encoding[c] for c in text if c in encoding)

def build_decoding(encoding):
    decoding = {}
    for k, v in encoding.items():
        decoding[v] = k
    return decoding

def decompress(encoded, decoding):
    result = []
    i = 0
    while i < len(encoded):
        if encoded[i] != 'f':
            key = encoded[i]
            if key not in decoding:
                raise ValueError(f"Invalid encoding key: {key}")
            result.append(decoding[key])
            i += 1
        else:
            start = i
            # Count how many f's
            while i < len(encoded) and encoded[i] == 'f':
                i += 1
            num_fs = i - start  # number of f's
            
            # After 'f's expect exactly num_fs hex digits
            if i + num_fs > len(encoded):
                raise ValueError("Invalid encoding: incomplete multi-nibble code")
            
            key = encoded[start:i + num_fs]
            if key not in decoding:
                raise ValueError(f"Invalid encoding key: {key}")
            result.append(decoding[key])
            i = i + num_fs
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
    print("Original:", text, "\n")
    print("Encoded:", encoded, "\n")
    print("Decoded:", decoded, "\n")

    # print("Original:", text[:100], "...\n")
    # print("Encoded:", encoded[:100], "...\n")
    # print("Decoded:", decoded[:100], "...\n")
    print("Match:", decoded == text)
