import os
import sys
import xmlrpc.client

#Put your server IP here
IP='127.0.0.1'
PORT=65432

url = 'http://{}:{}'.format(IP, PORT)
client_server_proxy = xmlrpc.client.ServerProxy(url)

directory = os.path.dirname(os.path.realpath(__file__))
if sys.argv[1]=='UPLOAD':
    filename = sys.argv[2]
    file_path = directory + '/'+'Client_Folder'+'/' + filename
    if not os.path.exists(file_path):
        print('Missing file -> ({})'.format(file_path))
        sys.exit(1)
    with open(file_path, "rb") as handle:
        binary_data = xmlrpc.client.Binary(handle.read())
        client_server_proxy.server_receive_file(binary_data, filename)
    print(' file ({}) Uploaded Sucessfully'.format(filename))

elif sys.argv[1]=='DOWNLOAD':
    filename = sys.argv[2]
    file_path = directory + '/'+'Client_Folder'+'/' + filename
    with open(file_path, "wb") as handle:
        handle.write(client_server_proxy.client_recieve_file(filename).data)

elif sys.argv[1]=='DELETE':
    filename = sys.argv[2]
    print(client_server_proxy.delete(filename))

elif sys.argv[1]=='RENAME':
    oldfile = sys.argv[2]
    newfile = sys.argv[3]
    print(client_server_proxy.rename(oldfile,newfile))

elif sys.argv[1] == 'ADD':
    x=input('Enter 1st number: ')
    y=input('Enter 2nd number: ')
    print('Result: {}'.format(client_server_proxy.add(x,y)))

elif sys.argv[1] == 'SORT':
    n = int(input("Enter the Total number to sort : "))
    li=[]
    for i in range(n):
        value = int(input("Please enter the %d Item : " %i))
        li.append(value)
    print('Sorted items : '+client_server_proxy.sort(li))

elif sys.argv[1]=='STOP':
    client_server_proxy.stop()