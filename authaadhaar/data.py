from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from xml.etree.ElementTree import Element, SubElement, tostring

from authaadhaar import __auth_version__


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


class License:
    aua = "MBni88mRNM18dKdiVyDYCuddwXEQpl68dZAGBQ2nsOlGMzC9DkOVL5s"
    asa = "MMxNu7a6589B5x5RahDW-zNP7rhGbZb5HsTRwbi-VVNxkoFmkHGmYKM"


class API:
    production_certificate = "./resources/certs/uidai_auth_prod.cer"
    digital_signature = "./resources/certs/uidai_auth_sign_prod.cer"
    stagging_certificate = "./resources/certs/uidai_auth_stage.cer"

    @staticmethod
    def get_auth_url():
        return f"http://auth.uidai.gov.in/{__auth_version__}/public/0/0/{License.asa}"

    @staticmethod
    def get_otp_url():
        return f"http://developer.uidai.gov.in/otp/{__auth_version__}/public/0/0/{License.asa}"


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
