# Auth Aadhaar
AuthAadhaar - Aadhaar Authentication/Verification using Python

## Installation

### Linux (Debian)
```bash
sudo apt install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl pkg-config
```

### Linux (CentOS)
```bash
sudo yum install libxml2-devel xmlsec1-devel xmlsec1-openssl-devel libtool-ltdl-devel pkgconfig
```

### Linux (Fedora)
```bash
sudo dnf install libxml2-devel xmlsec1-devel xmlsec1-openssl-devel libtool-ltdl-devel pkgconfig
```

### MacOS
```bash
brew install libxml2 libxmlsec1 pkg-config
```

### Alpine
```bash
apk add build-base libressl libffi-dev libressl-dev libxslt-dev libxml2-dev pkgconfig xmlsec-dev xmlsec
```

### Poetry
```bash
pip3 install --user poetry
```


## Getting started
```bash
poetry update
poetry run task test
```

## References
[Tutorials](https://uidai.gov.in/ecosystem/authentication-devices-documents/developer-section/915-developer-section/tutorial-section.html)

[Sample Data](https://uidai.gov.in/ecosystem/authentication-devices-documents/developer-section/916-developer-section/data-and-downloads-section.html)

[Authentication Documents](https://www.uidai.gov.in/ecosystem/authentication-devices-documents/authentication-documents.html)

[pingali/pyAadhaarAuth](https://github.com/pingali/pyAadhaarAuth)
