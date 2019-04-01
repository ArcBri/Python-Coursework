import sys

file = sys.argv[1]
file2=sys.argv[2]
i= 0
buffer = bytearray(1024) # allocate the buffer
with open(file, "rb") as f:
    with open(file2, "rb")as mask:
      numBytesRead = f.readinto(buffer)
	  for i in range(numBytesRead):
            buffer[i] = (buffer[i] ^ mask)
        sys.stdout.buffer.write(buffer)
      while numBytesRead > 0:
       numBytesRead = f.readinto(buffer)
       for i in range(numBytesRead):
                buffer[i] = (buffer[i] ^ mask)
            
       sys.stdout.buffer.write(buffer[:numBytesRead])

