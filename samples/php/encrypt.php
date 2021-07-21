<? php

function encryptMcrypt($data){
  $fp             = fopen(UIDAI_PUBLIC_CERTIFICATE, "r");
  $pub_key_string = fread($fp, 8192);
  openssl_public_encrypt($data, $encrypted_data, $pub_key_string, OPENSSL_PKCS1_PADDING);
  return $encrypted_data;
}

function generateRandomString($length           = 32) {
  $characters       = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  $charactersLength = strlen($characters);
  $randomString     = '';
  for ($i                = 0;$i < $length;$i++) {
          $randomString .= $characters[rand(0, $charactersLength - 1) ];
  }
  return $randomString;
}

function encryptPID($data, $skey) {
  $result = openssl_encrypt($data, 'AES-256-ECB', $skey);
  return ($result);
}

function getExpiryDate($_CERTIFICATE) {
  $_CERT_DATA = openssl_x509_parse(file_get_contents($_CERTIFICATE));
  return date('Ymd', $_CERT_DATA['validTo_time_t']);
}

$path=$_SERVER['DOCUMENT_ROOT'];
$certpath=$path."/your .pfx file";
$publickeypath=$path."/your .cer file";
$certpassword="your cert password";

require_once('xmlsecurity.php'); // for creating this file use link : https://github.com/robrichards/xmlseclibs
$trn_id = "AuthDemoClient:public:". date('YmdHisU');
if (!$cert_store = file_get_contents($certpath)) {
  echo "Error: Unable to read the cert file\n";
  exit;
}

if (openssl_pkcs12_read($cert_store, $cert_info, $certpassword)) {
  //print_r($cert_info["cert"]);
  //print_r($cert_info["pkey"]);
} else {
  echo "Error: Unable to read the cert store.\n";
  exit;
}

define("UIDAI_PUBLIC_CERTIFICATE" , $publickeypath);
define("AUA_PRIVATE_CERTIFICATE" , $cert_info["pkey"]);
date_default_timezone_set("Asia/Calcutta");

$date2= gmdate("Y-m-d\TH:i:s");
$date1 = date('Y-m-d\TH:i:s', time());
$ts='"'.$date1.'"';
//date('Y-m-d\TH:i:s');

$pid_1='<Pid ts='.$ts.' ver="1.0"><Pv otp="'.$otp.'"/></Pid>';
$randkey = generateRandomString();
$SESSION_ID = $randkey;
$skey1=encryptMcrypt($SESSION_ID); $skey=base64_encode($skey1); // generate ci code start
$ci=getExpiryDate(UIDAI_PUBLIC_CERTIFICATE); // generate pid block code start

$pid=encryptPID($pid_1,$randkey); //hmac creation code start
$hash=hash("SHA256",$pid_1,true);
$hmac=encryptPID($hash,$randkey);
$load_xml="
<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>
<Auth xmlns=\"http://www.uidai.gov.in/authentication/uid-auth-request/1.0\" sa=\"public\" lk=\"your license key\" txn=\"$trn_id\" ver=\"1.6\" tid=\"public\" ac=\"your code from aadhaar\" uid=\"$aadhaarno\"><Uses pi=\"n\" pa=\"n\" pfa=\"n\" bio=\"n\" bt=\"\" pin=\"n\" otp=\"y\"/>
  <Meta udc=\"UDC:001\" fdc=\"NC\" idc=\"NA\" pip=\"NA\" lot=\"P\" lov=\"$pincode\"/>
  <Skey ci=\"$ci\">$skey</Skey>
  <Data type=\"X\">$pid</Data>
  <Hmac>$hmac</Hmac>
</Auth>";

$dom = new DOMDocument();
$dom->loadXML($load_xml); // the XML you specified above.
$objDSig = new XMLSecurityDSig();
$objDSig->setCanonicalMethod(XMLSecurityDSig::C14N_COMMENTS);
$objDSig->addReference($dom, XMLSecurityDSig::SHA1, array('http://www.w3.org/2000/09/xmldsig#enveloped-signature'),array('force_uri' =>'true'));
$objKey = new XMLSecurityKey(XMLSecurityKey::RSA_SHA1, array('type'=>'private'));
$objKey->loadKey($cert_info["pkey"], False);
$objKey->passphrase = 'your certificate password';
$objDSig->sign($objKey, $dom->documentElement); $objDSig->add509Cert($cert_info["cert"]);
$objDSig->appendSignature($dom->documentElement);
$xml_string = $dom->saveXML();
$xml_string1 = urlencode($xml_string);

$curl = curl_init(); $url=""; //aadhar service url
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_POSTFIELDS,"eXml=A28".$xml_string1);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true); /* complete within 20 seconds */
curl_setopt($curl, CURLOPT_TIMEOUT, 20);
$result = curl_exec($curl);
curl_close($curl);

$xml = @simplexml_load_string($result);
$return_status=$xml['ret'];

if($return_status=="y"){
  $res=1;
}
if($return_status!="y"){
  $res=0;
} else {
  $res='Aadhaar no not exist';
}

?>
