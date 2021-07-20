from authaadhaar import __version__


def test_version():
    if not __version__ == "0.1.0":
        raise AssertionError
