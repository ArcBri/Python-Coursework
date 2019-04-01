def formResponse(header,response): #sends ENCODED response

	method = header.method
	prefix, path = header.path[0:].strip().split("/")
	
	if method == "GET":
	
		if prefix.lower() == "key":
		
			response = getKey(response, path)
			response = resToString(response).encode()
			
		elif prefix.lower() == "file":
		
			response, readFile = getFile(response, path)
			response = resToString(response).encode()
			response = response + readFile + ("  ").encode() # may not be correct
			
	elif method == "POST":
	
		response = postKey(response, header,path)
		response = resToString(response).encode()
		
	elif method == "DELETE":
	
		response = deleteKey(response, path)
		response = resToString(response).encode()
		
	client_socket.send(resToString(response).encode())
	
def getKey(response, path):
	
	if path in store:
	
		value = store[path]
		response["status"] = getStatus(200)
		response["length"] = len(value)
		response["body"] = value
		
	else:
	
		response["status"] = getStatus(404)
	
	return response

def getFile(response, path):

	if os.path.exists(path):
	
		try:
		
			with open(path, "rb") as f: # will read file as bytes. DONT ENCODE
			
				value = f.read()
				response["status"] = getStatus(200)
				response["length"] = len(value)
				
		except OSerror:
		
			response["status"] = getStatus(403)
			value =""
			
	else:
	
		response["status"] = getStatus(404)
		value = ""
		
	return response, value

def postKey(response, header,path):
	
	key = path
	
	length = header.size
	store[key] = header.body
	
	response["status"] = getStatus(200)
	response["length"] = length
	response["body"] = body
	
	return response

def deleteKey(response, path):

	if path in store:
	
		value = path
		response["status"] = getStatus(200)
		response["length"] = len(value)
		response["body"] = value
		
	else:
	
		response["status"] = getStatus(404)
		
	return response

