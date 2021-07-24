
from typing import List
from xml.etree.ElementTree import Element
from .data import License, User, API, SubNode, RequestData as RD
from .encrypt import Certificate
from .input import Collector
from .request import Session

class Client:
  def __init__(self) -> None:
    self.cert = Certificate(location=API.stagging_certificate)

  def connect(self):
    _req = Session(certificate=self.cert)
    self._data = Collector()
    self._data.collect()
    self.xml_root = self.load_xml_root()
    self.xml_nodes = self.load_xml_nodes(_req)
    self.compiled_xml()
    print(RD.prettyXML(self.xml_root))
    del _req


  def generate_pid_block(self):
    return f'<Pid ts="{self._data.ts}">This is PID block with user data of {self._data.user.name}</Pid>'

  def load_xml_root(self) -> Element:
    root = RD.Auth(
      uid=User.uid,
      consent=User.auth_consent,
      licese=License.asa,
      transaction_id="testing",
    ).xml_root()

    return root

  def load_xml_nodes(self, req: Session):
    nodes: List[SubNode] = []
    pid_block = self.generate_pid_block()
    _encrypted_pid, _hmac = req.encrypt(pid_block, ts=self._data.ts)
    nodes.append(RD.Skey(
      certificate_id=self.cert.id,
      content=req.encrypted_key,
    ))
    nodes.append(RD.Uses())
    nodes.append(RD.Data(_encrypted_pid))
    nodes.append(RD.Hmac(_hmac))
    return nodes

  def compiled_xml(self):
    for n in self.xml_nodes:
      n.xml_link(self.xml_root)
