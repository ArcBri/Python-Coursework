import zlib
import sys

file=sys.argv[1]

with open(file, "rb") as f:
 bytes = f.read()
 checksum = zlib.crc32(bytes)
 print(checksum)