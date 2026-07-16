import subprocess

p = subprocess.Popen("ping 127.0.0.1", stdout=subprocess.PIPE)

p.wait()

print(p)

if p.returncode == 0:
    print("Ping Successful")
else:
    print("Ping Failed")
