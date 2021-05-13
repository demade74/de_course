import re

EMAIL_PATTERN = r'^([\w\-\.]+)@([\w\-]+\.[\w]{2,4})$'

def email_parse(email):
    email = email.lower()
    valid_email = re.fullmatch(EMAIL_PATTERN, email)
    if valid_email is None:
        raise ValueError(f'wrong email {email}')

    return {'username': valid_email.group(1), 'domain': valid_email.group(2)}

print(email_parse('demade74@gmail.com')) # valid result
print(email_parse('de made74@gmail.com')) # invalid result
