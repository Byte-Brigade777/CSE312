from flask import request


def validate_password(password):
    password = str(password)
    lower = 0
    upper = 0
    special = 0
    number = 0

    if len(password) < 8:
        return False
    for letter in password:
        if letter.islower():
            lower += 1
        if letter.isupper():
            upper += 1
        if letter.isdigit():
            number += 1
        if letter in {'!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '='}:
            special += 1
        if not letter.isalnum() and letter not in {'!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '='}:
            return False
    if lower == 0 or upper == 0 or special == 0 or number == 0:
        return False
    else:
        return True


# def test1():
#     request = Request(b'POST / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nCookie: id=X6kA; visits=4\r\n\r\nusername_reg=abcd&password_reg=abcd%21')
#     e = extract_credentials(request)
#     print(e)
#     assert(e[0] == "abcd")
#     assert(e[1] == "abcd!")


# if __name__ == '__main__':
#     test1()