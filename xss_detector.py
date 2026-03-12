# xss_detector.py

def check_reflection(payload, response_text):

    if payload in response_text:
        return True

    return False
