from .data import Files
from .encrypt import Certificate
from .input import Collector
from .request import Session

data = Collector()
data.collect()
cert = Certificate(location=Files.stagging_certificate)
req = Session(certificate=cert)

pid_block = f'<Pid ts="{data.ts}">This is PID block with user data of {data.user.name}</Pid>'

encrypted_pid, hmac = req.encrypt(pid_block, ts=data.ts)

skey = f'<Skey ci="{cert.id}">{req.encrypted_key}</Skey>'
data_block = f"<Data>{encrypted_pid}</Data>"
hmac_block = f"<Hmac>{hmac}</Hmac>"

# req.post()

print("Encrypted Session Key")
print(skey)
print("Data Block")
print(data_block)
print("HMAC Block")
print(hmac_block)

dec, deh = req.decrypt(encrypted_pid, hmac)

print(dec)
print(deh)
