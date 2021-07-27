import secrets
from datetime import datetime
from typing import TYPE_CHECKING, Dict
from defusedxml import ElementTree as ET
from authaadhaar import __auth_version__

from authaadhaar.encrypt import Certificate

if TYPE_CHECKING:
    # Does not exists at runtime. Only used for type checking.
    from authaadhaar.typing import Element, ElementTree

# from xml.etree.ElementTree import Element, SubElement, tostring
# from abc import ABCMeta, abstractmethod
# from dataclasses import dataclass


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
    production_certificate = "./resources/certs/uidai_auth_prod.cer"
    digital_signature = "./resources/certs/uidai_auth_sign_prod.cer"
    stagging_certificate = "./resources/certs/uidai_auth_stage.cer"

    class License:
        aua = "MBni88mRNM18dKdiVyDYCuddwXEQpl68dZAGBQ2nsOlGMzC9DkOVL5s"
        asa = "MMxNu7a6589B5x5RahDW-zNP7rhGbZb5HsTRwbi-VVNxkoFmkHGmYKM"

    @staticmethod
    def get_auth_url():
        return f"http://auth.uidai.gov.in/{__auth_version__}/public/0/0/{AppData.License.asa}"

    @staticmethod
    def get_otp_url():
        return f"http://developer.uidai.gov.in/otp/{__auth_version__}/public/0/0/{AppData.License.asa}"


class XMLData:
    def __init__(
        self,
        certificate: Certificate = None,
        uid: str = "",
        license: str = "",
        auth_attrs: Dict[str, str] = None,
        uses_attrs: Dict[str, str] = None,
    ) -> None:
        self._pid_tree: ElementTree = ET.parse("./resources/formats/input.pid.xml")
        print(type(self._pid_tree))
        self._auth_tree: ElementTree = ET.parse("./resources/formats/input.xml")
        self._uid = uid or User.uid
        self._license = license or AppData.License.asa
        self._cert = certificate or Certificate(AppData.stagging_certificate)
        self._auth_attrs = auth_attrs or self._get_auth_attrs()
        self._uses_attrs = uses_attrs or {
            "pi": "y",
            "pa": "y",
            "pfa": "n",
            "bio": "n",
            "pin": "n",
            "otp": "n",
        }
        self._ts = self._get_ts()

    def _get_ts(self) -> str:
        now = datetime.now()
        ts = now.strftime("%Y-%m-%dT%H:%M:%S")
        return ts

    def create_pid_block(self) -> str:
        pi_attrs = {
            "ms": "E",
            "mv": "100",
            "name": User.name,
            "gender": User.gender,
            "dob": User.dob,
            "dobt": User.dobt,
            "phone": User.phone,
            "email": User.email,
        }

        pa_attrs = {
            "ms": "E",
            "street": User.street,
            "vtc": User.vtc,
            "subdist": User.subdist,
            "dist": User.district,
            "state": User.state,
            "country": "India",
            "pc": User.pincode,
        }

        tree = self._pid_tree

        root: Element = tree.getroot()
        print(type(root))
        root.attrib["ts"] = self._ts
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

        return ET.tostring(root, encoding="utf8", xml_declaration=True).decode("utf8")

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

    def create_auth_block(self, skey_block: str, pid_block: str, hmac_block: str) -> str:
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
            sig.text = "This is Signature"

        return ET.tostring(root, encoding="utf8", xml_declaration=True).decode("utf8")


"""

class SubNode(metaclass=ABCMeta):
    @abstractmethod
    def xml_link(self, parent: Element) -> Element:
        ...

class RequestData:
    @dataclass
    class Auth:
        uid: str
        consent: str
        licese: str
        transaction_id: str
        tid: str = ""
        aua_code: str = "public"
        sub_aua_code: str = "public"
        version: str = __auth_version__

        def xml_root(self) -> Element:
            element = Element(
                "Auth",
                {
                    "uid": self.uid,
                    "ver": self.version,
                    "lk": self.licese,
                    "tid": self.tid,
                    "ac": self.aua_code,
                    "sa": self.sub_aua_code,
                    "txn": self.transaction_id,
                },
            )
            return element

    @dataclass
    class Data(SubNode):
        content: str

        def xml_link(self, parent: Element) -> Element:
            element = SubElement(parent, "Data")
            element.text = self.content
            return element

    @dataclass
    class Uses(SubNode):
        personal_id: bool = True
        personal_aadress: bool = False
        full_address: bool = False
        otp: bool = False
        pin: bool = False
        biometric: bool = False

        def xml_link(self, parent: Element) -> Element:
            element = SubElement(
                parent,
                "Uses",
                {
                    "pi": "y" if self.personal_id else "n",
                    "pa": "y" if self.personal_aadress else "n",
                    "pfa": "y" if self.full_address else "n",
                    "otp": "y" if self.otp else "n",
                    "pin": "y" if self.pin else "n",
                    "bio": "y" if self.biometric else "n",
                },
            )
            return element

    @dataclass
    class Skey(SubNode):
        certificate_id: str
        content: str

        def xml_link(self, parent: Element) -> Element:
            element = SubElement(parent, "Skey", {"ci": self.certificate_id})
            element.text = self.content
            return element

    @dataclass
    class Hmac(SubNode):
        content: str

        def xml_link(self, parent: Element) -> Element:
            element = SubElement(parent, "Hmac")
            element.text = self.content
            return element

    @staticmethod
    def prettyXML(xml: Element) -> str:
        return tostring(
            xml,
            encoding="UTF-8",
            xml_declaration=True,
        ).decode()
"""
