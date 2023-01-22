TOKEN = "Your Token" # https://dashboard.ngrok.com/get-started/your-authtoken
PORT = "Your Port"
REGION = "Your Region" # United States, Europe, Asia Pacific, Australia, South America, Japan, India

import socket, inspect, shutil, os
try:
    from pyngrok import conf, ngrok
except:
    os.system("pip install pyngrok")
    from pyngrok import conf, ngrok

region_index = {"United States":"us", "Europe":"eu", "Asia Pacific":"ap", "Australia":"au", "South America":"sa", "Japan":"jp", "India":"in"}
ip_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_s.connect(("8.8.8.8", 80))
ip = ip_s.getsockname()[0]
ip_s.close()
path = os.path.dirname(__file__)
ngrok_path = str(inspect.getfile(conf)).replace("conf.py", "")+"bin"

try:
    os.makedirs(ngrok_path)
except:
    pass
shutil.copy(path+'\\ngrok.exe', ngrok_path+'\\ngrok.exe')

# ngrok.set_auth_token(TOKEN)
# conf.get_default().ngrok_version = "v3"
# conf.get_default().region = region_index[REGION]

pyngrok_config = conf.PyngrokConfig(auth_token=TOKEN, region=region_index[REGION], ngrok_version="v3")
conf.set_default(pyngrok_config)

connection_string = ngrok.connect(PORT, "tcp", pyngrok_config=pyngrok_config).public_url
ssh_url, port = connection_string.strip("tcp://").split(":")
ngrok_process = str(ngrok.get_ngrok_process()).split('"')

os.system("cls")

print(f"Region          {REGION} ({region_index[REGION]})")
print(f"Web Interface   {ngrok_process[1]}")
print(f"Local           {ip}:{PORT}")
print(f"Public          {socket.gethostbyname(ssh_url)}:{port} or {ssh_url}:{port}")
print("\nCtrl+C to quit")
# print()

try:
    ngrok.get_ngrok_process().proc.wait()
except KeyboardInterrupt:
    os.system("cls")
    print("Shutting down server.")

    ngrok.kill()