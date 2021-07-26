#### Test URLs: (remember to append AUA code and first two digits of Aadhaar number)

>    Auth URL - http://auth.uidai.gov.in/1.6//<1st-digit-of-uid>/<2nd-digit-of-uid>/
>
>    e-KYC URL - http://developer.uidai.gov.in/kyc/1.0//<1st-digit-of-uid>/<2nd-digit-of-uid>/
>
>    OTP URL - http://developer.uidai.gov.in/otp/1.6//<1st-digit-of-uid>/<2nd-digit-of-uid>/
>
>    BFD URL - http://developer.uidai.gov.in/bfd/1.6//<1st-digit-of-uid>/<2nd-digit-of-uid>/

#### Test Codes:

>    AUA Code ("ac" attribute) : "public"
>
>    Sub-AUA Code ("sa" attribute) - "public"
>
>    License Key ("lk" attribute) : You can use any of the following license keys given below. Binary distribution of sample client is shipped with the first one below.
>
>        AUA License Key: MBni88mRNM18dKdiVyDYCuddwXEQpl68dZAGBQ2nsOlGMzC9DkOVL5s - allows usage of PI, PA, PFA, BIO-FMR, BIO-FIR, BIO-IIR, OTP, PIN, Indian Language, e-KYC
>
>        ASA License Key: MMxNu7a6589B5x5RahDW-zNP7rhGbZb5HsTRwbi-VVNxkoFmkHGmYKM
>
>    BFD URL - http://developer.uidai.gov.in/bfd/1.6//<1st-digit-of-uid>/<2nd-digit-of-uid>/
>
>    Public key certificate - See chapter on certificates (remember to use Staging/Test certificate for testing and production certificate for production)
>
>    Keystore for digital signature for "public" AUA - Keystore in p12 file format (keystore Password: "public", Alias: "public")

Following are the test UIDs and their demographic data. All of them have same bio record as given above. If you have your own Aadhaar number (real one) then you can use that to test too.

```
uid=999941057058
name=Shivshankar Choudhury
dob=13-05-1968
dobt=V
gender=M
phone=2810806979
email=sschoudhury@dummyemail.com
street=12 Maulana Azad Marg
vtc=New Delhi
subdist=New Delhi
district=New Delhi
state=New delhi
pincode=110002

uid=999971658847
name=Kumar Agarwal
dob=04-05-1978
dobt=A
gender=M
phone=2314475929
email=kma@mailserver.com
building=IPP, IAP
landmark=Opp RSEB Window
street=5A Madhuban
locality=Veera Desai Road
vtc=Udaipur
district=Udaipur
state=Rajasthan
pincode=313001

uid=999933119405
name=Fatima Bedi
dob=30-07-1943
dobt=A
gender=F
phone=2837032088
email=bedi2020@mailserver.com
building=K-3A Rampur Garden
vtc=Bareilly
district=Bareilly
state=Uttar Pradesh
pincode=243001

uid=999955183433
name=Rohit Pandey
dob=08-07-1985
dobt=A
gender=M
phone=2821096353
email=rpandey@mailserver.com
building=603/4 Vindyachal
street=7TH Road Raja Wadi
locality=Neelkanth Valley
poname=Ghatkopar (EAST)
vtc=Mumbai
district=Mumbai
state=Maharastra
pincode=243001

uid=999990501894
name=Anisha Jay Kapoor
gender=F
dob=01-01-1982
dobt=V
building=2B 203
street=14 Main Road
locality=Jayanagar
district=Bangalore
state=Karnataka
pincode=560036
```
