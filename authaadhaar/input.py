import uuid

from .data import PublicAPI, User
from .encrypt import Certificate
from .session import Session


def get_transaction_id(uid):
    return uuid.uuid5(uuid.uuid4(), str(uid))


class Config:
    class Uses:
        pi = "y"
        pa = "y"
        pfa = "y"
        pin = "n"
        otp = "y"


# <Pi ms="E" mv="" name="" lname="" lmv="" gender="M|F|T" dob="" dobt="V|D|A" age="" phone="" email=""/>
# <Pa ms="E" co="" house="" street="" lm="" loc="" vtc="" subdist="" dist="" state="" country="" pc="" po=""/>
# <Pfa ms="E" mv="" av="" lav="" lmv=""/>

pid_data = f'<Pid ts="" ver="" wadh=""><Demo lang=""><Pi ms="E" mv="" name="" lname="" lmv="" gender="M|F|T" dob="" dobt="V|D|A" age="" phone="" email=""/><Pa ms="E" co="" house="" street="" lm="" loc="" vtc="" subdist="" dist="" state="" country="" pc="" po=""/><Pfa ms="E" mv="" av="" lav="" lmv=""/></Demo><Bios dih=""><Bio type="FMR|FIR|IIR|FID" posh="" bs="">encoded biometric</Bio></Bios><Pv otp="" pin=""/></Pid>'

cert = Certificate()
encrypted_pid_block = cert.encrypt("Testing")
print(encrypted_pid_block)
txn_id = get_transaction_id(User.uid)
session = Session()

auth_data = f"""<Auth uid="{User.uid}" rc="{User.auth_consent}" tid="" ac="{PublicAPI.aua_code}" sa="{PublicAPI.sub_aua_code}" ver="" txn="{txn_id}" lk="{PublicAPI.aualk}">
<Uses pi="{Config.Uses.pi}" pa="{Config.Uses.pa}" pfa="{Config.Uses.pfa}" bio="n" pin="{Config.Uses.pin}" otp="{Config.Uses.otp}"/>
<Device rdsId="" rdsVer="" dpId="" dc="" mi="" mc="" />
<Skey ci="{cert.cert_id}">{session.key}</Skey>
<Hmac>SHA-256 Hash of Pid block, encrypted and then encoded</Hmac>
<Data type="X|P">{encrypted_pid_block}</Data>
<Signature>Digital signature of AUA</Signature>
</Auth>"""

# print(auth_data)
