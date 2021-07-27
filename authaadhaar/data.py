import secrets
from datetime import datetime
from typing import TYPE_CHECKING, Dict, Optional

from defusedxml import ElementTree as ET

from authaadhaar import __auth_version__
from authaadhaar.encrypt import Certificate

if TYPE_CHECKING:
    # Does not exists at runtime. Only used for type checking.
    from .typing import Element, ElementTree

UserDataError = ValueError("User data is not fetched")


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


class AppData:
    class Certificate:
        production = "./resources/certs/uidai_auth_prod.cer"
        signature = "./resources/certs/uidai_auth_sign_prod.cer"
        stagging = "./resources/certs/uidai_auth_stage.cer"

    class License:
        aua = "MBni88mRNM18dKdiVyDYCuddwXEQpl68dZAGBQ2nsOlGMzC9DkOVL5s"
        asa = "MMxNu7a6589B5x5RahDW-zNP7rhGbZb5HsTRwbi-VVNxkoFmkHGmYKM"

    class Input:
        auth = "./resources/formats/input.xml"
        pid = "./resources/formats/input.pid.xml"

    auth_url = f"http://auth.uidai.gov.in/{__auth_version__}/public/0/0/{License.asa}"
    otp_url = f"http://developer.uidai.gov.in/otp/{__auth_version__}/public/0/0/{License.asa}"


class DataBuilder:
    def __init__(
        self,
        uid: str,
        certificate: Optional[Certificate] = None,
        license: Optional[str] = None,
        auth_attrs: Optional[Dict[str, str]] = None,
        uses_attrs: Optional[Dict[str, str]] = None,
    ) -> None:
        self._pid_tree: ElementTree = ET.parse(AppData.Input.pid)
        self._auth_tree: ElementTree = ET.parse(AppData.Input.auth)
        self._uid: str = uid
        self._license = license or AppData.License.asa
        self._cert = certificate or Certificate(AppData.Certificate.stagging)
        self._auth_attrs: Dict[str, str] = auth_attrs or self._get_auth_attrs()
        self._uses_attrs: Dict[str, str] = uses_attrs or {
            "pi": "y",
            "pa": "y",
            "pfa": "n",
            "bio": "n",
            "pin": "n",
            "otp": "n",
        }
        self.__user_data: Optional[Dict[str, str]] = None

    def __get_ts(self) -> str:
        now = datetime.now()
        ts = now.strftime("%Y-%m-%dT%H:%M:%S")
        return ts

    def get_user_data(
        self,
        uid: str,
        name: str = "",
        dob: str = "",
        gender: str = "",
        phone: str = "",
        email: str = "",
        street: str = "",
        village: str = "",
        subdist: str = "",
        district: str = "",
        state: str = "",
        country: str = "India",
        pincode: str = "",
    ) -> str:
        self.__user_data = {
            "uid": uid.strip(),
            "name": name.strip(),
            "dob": dob.strip(),
            "gender": gender.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
            "street": street.strip(),
            "vtc": village.strip(),
            "subdist": subdist.strip(),
            "district": district.strip(),
            "state": state.strip(),
            "country": country.strip(),
            "pincode": pincode.strip(),
        }
        return self.__get_ts()

    def build_pid_block(self, ts: str) -> str:
        if self.__user_data is None:
            raise UserDataError

        pi_attrs = {
            "ms": "E",
            "mv": "100",
            "name": self.__user_data["name"],
            "gender": self.__user_data["gender"],
            "dob": self.__user_data["dob"],
            "phone": self.__user_data["phone"],
            "email": self.__user_data["email"],
        }

        pa_attrs = {
            "ms": "E",
            "street": self.__user_data["street"],
            "vtc": self.__user_data["vtc"],
            "subdist": self.__user_data["subdist"],
            "dist": self.__user_data["district"],
            "state": self.__user_data["state"],
            "country": self.__user_data["country"],
            "pc": self.__user_data["pincode"],
        }

        tree = self._pid_tree

        root: Element = tree.getroot()
        root.attrib["ts"] = ts
        root.attrib["ver"] = "2.0"
        del root.attrib["wadh"]

        demo = root.find("Demo")
        if demo is not None:
            del demo.attrib["lang"]

            pi = demo.find("Pi")
            if pi is not None:
                pi.attrib = pi_attrs

            pa = demo.find("Pa")
            if pa is not None:
                pa.attrib = pa_attrs

            pfa = demo.find("Pfa")
            if pfa is not None:
                demo.remove(pfa)

        del pi_attrs
        del pa_attrs

        bios = root.find("Bios")
        if bios is not None:
            root.remove(bios)

        pv = root.find("Pv")
        if pv is not None:
            root.remove(pv)

        return ET.tostring(root, encoding="unicode", xml_declaration=True)

    def _get_auth_attrs(self) -> Dict[str, str]:
        txn_id = "public:auth:" + secrets.token_urlsafe(28)
        attrs = {
            "uid": self._uid,
            "rc": "Y",
            "ac": "public",
            "sa": "public",
            "ver": __auth_version__,
            "txn": txn_id,
            "lk": self._license,
        }
        return attrs

    def build_auth_block(self, skey_block: str, pid_block: str, hmac_block: str) -> str:

        if self.__user_data is None:
            raise UserDataError

        tree = self._auth_tree

        root: Element = tree.getroot()
        root.attrib.update(self._auth_attrs)

        uses = root.find("Uses")
        if uses is not None:
            uses.attrib.update(self._uses_attrs)

        device = root.find("Device")
        if device is not None:
            root.remove(device)

        skey = root.find("Skey")
        if skey is not None:
            skey.attrib["ci"] = self._cert.id
            skey.text = skey_block

        data = root.find("Data")
        if data is not None:
            data.attrib["type"] = "X"
            data.text = pid_block

        hmac = root.find("Hmac")
        if hmac is not None:
            hmac.text = hmac_block

        sig = root.find("Signature")
        if sig is not None:
            sig.text = "TODO: Signature Block"

        return ET.tostring(root, encoding="unicode", xml_declaration=True)
