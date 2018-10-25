string = "wubbalubbadubdub"
inascii = [ord(c) for c in string]
inascii_bytes = [bytes((n, )) for n in inascii][::-1]
print(inascii_bytes)


