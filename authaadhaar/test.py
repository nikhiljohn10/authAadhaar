# Testing API

class User:
    uid = "999941057058"
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


class PublicAPI:

    version = "2.5"
    aualk = "MBni88mRNM18dKdiVyDYCuddwXEQpl68dZAGBQ2nsOlGMzC9DkOVL5s"
    asalk = "MMxNu7a6589B5x5RahDW-zNP7rhGbZb5HsTRwbi-VVNxkoFmkHGmYKM"

    class Auth:
        url = f"http://auth.uidai.gov.in/{PublicAPI.version}/public/0/0/{PublicAPI.asalk}"

    class OTP:
        url = f"http://developer.uidai.gov.in/otp/{PublicAPI.version}/public/0/0/{PublicAPI.asalk}"
