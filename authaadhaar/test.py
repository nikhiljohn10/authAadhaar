from .data import Files
from .encrypt import Certificate
from .input import Collector
from .request import Session

data = Collector()
data.collect()
cert = Certificate(location=Files.stagging_certificate)
req = Session(data=data, certificate=cert)

pid_block = f'<Pid ts="{data.ts}">This is PID block with user data of {data.user.name}</Pid>'
encrypted_pid_block = req.encrypt(pid_block)
auth_block = f"<Auth>{encrypted_pid_block}</Auth>"

print("session key")
print(req.key)
print("encrypted session key")
print(req.encrypted_key)
print("auth_block")
print(auth_block)
