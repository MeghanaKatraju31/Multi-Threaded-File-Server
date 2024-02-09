from xmlrpc.server import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
import xmlrpc.client
import os
import sys
import threading
import time
# Put in your server IP here
directory = os.path.dirname(os.path.realpath(__file__))
IP='127.0.0.1'
PORT=65432
class AsyncRequest(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

if len(sys.argv)>1 and sys.argv[1]=="ASYNC":
    server = SimpleXMLRPCServer((IP, PORT), requestHandler=AsyncRequest)
    
server = SimpleXMLRPCServer((IP, PORT))
def synchronize_folder():
    synchronize_folder_path= directory+'/Sync_Folder/'
    while True:
        for root, dirs, files in os.walk(synchronize_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                last_modified_syncfolder = os.path.getmtime(file_path)
                last_modified_server=os.path.getmtime(directory + '/' +'Server_Folder'+'/'+ file)
                if last_modified_syncfolder > last_modified_server:
                    with open(file_path, "rb") as handle:
                        with open(directory + '/Server_Folder/'+ file, "wb") as handel1:
                            handel1.write(handle.read())
        time.sleep(300)

syncthread = threading.Thread(target=synchronize_folder)
syncthread.start()
print("Server is running....")

def server_receive_file(arg, filename):
    output_file_path = directory + '/' +'Server_Folder'+'/'+ filename
    with open(output_file_path, "wb") as handle:
        handle.write(arg.data)
        return True
quit = 0
def stop():
    global quit
    quit = 1
    return True

def client_recieve_file(filename):
    output_file_path = directory + '/' +'Server_Folder'+'/'+ filename
    if not os.path.exists(output_file_path):
        print('Missing file -> ({})'.format(output_file_path))
        sys.exit(1)
    with open(output_file_path, "rb") as handle:
        return xmlrpc.client.Binary(handle.read())

def delete(filename):
    try:
        output_file_path = directory + '/' +'Server_Folder'+'/'+ filename
        os.remove(output_file_path)
        return '{} Sucessfully deleted'.format(filename)
    except:
        return 'Missing file -> ({})'.format(filename)

def rename(oldfile,newfile):
    try:
        old_file_path = directory + '/' +'Server_Folder'+'/'+ oldfile
        new_file_path = directory + '/' +'Server_Folder'+'/'+ newfile
        os.rename(old_file_path,new_file_path)
        return '{} Sucessfully renamed'.format(newfile)
    except:
        return 'Missing file -> ({})'.format(oldfile)

def add(x,y):
    return float(x)+float(y)

def sort(li):
    n = len(li)
    for i in range(n -1):
        for j in range(n - i - 1):
            if(li[j] > li[j + 1]):
                temp = li[j]
                li[j] = li[j + 1]
                li[j + 1] = temp

    return ' '.join([str(i) for i in li])

server.register_function(server_receive_file, 'server_receive_file')
server.register_function(client_recieve_file, 'client_recieve_file')
server.register_function(delete,'delete')
server.register_function(rename,'rename')
server.register_function(add,'add')
server.register_function(sort,'sort')
server.register_function(stop,'stop')
while not quit:
    server.handle_request()