from authaadhaar.client import AuthClient
from authaadhaar.data import AppData as AD
from authaadhaar.encrypt import Certificate


class User:

    uid = "999941057058"
    auth_consent = "Y"

    name = "Shivshankar Choudhury"
    dob = "13-05-1968"
    dobt = "V"
    gender = "M"
    phone = "2810806979"
    email = "sschoudhury@dummyemail.com"

    street = "12 Maulana Azad Marg"
    vtc = "New Delhi"
    subdist = "New Delhi"
    district = "New Delhi"
    state = "New delhi"
    pincode = "110002"


cert = Certificate(location=AD.Certificate.stagging)
license = AD.License.asa

client = AuthClient(license=license, certificate=cert)

auth1 = client.authenticate(uid=User.uid)
auth1.load_data({"name": User.name})
out = auth1.auth()
print(out)
