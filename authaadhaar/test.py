from .data import Files
from .encrypt import Certificate
from .input import Collector
from .request import Session

data = Collector()
data.collect()
cert = Certificate(location=Files.stagging_certificate)
req = Session(certificate=cert)

pid_block = f'<Pid ts="{data.ts}">This is PID block with user data of {data.user.name}</Pid>'
encrypted_pid_block = req.encrypt(pid_block, ts=data.ts)
auth_block = f"<Auth>{encrypted_pid_block}</Auth>"

req.post()

print("Session Key")
print(req.key)
print("Encrypted Session Key")
print(req.encrypted_key)
print("Auth Block")
print(auth_block)

dec = req.decrypt(encrypted_pid_block)

print(dec)
