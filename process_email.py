
class InvalidEmail(Exception):
    """The provided value is not a valid email address"""
    pass

def extract_domain(email):
    if "@" not in email:
        raise InvalidEmail("An email address must have an @ sign")
    if email.count("@") > 1:
        raise InvalidEmail(f"Expected a single @ sign, but '{email}' has {email.count('@')} ")

    local_part, domain_part = email.split("@")

    if not local_part:
        raise InvalidEmail("An email address cannot have an empty local part")
    if not domain_part:
        raise InvalidEmail("An email address cannot have an empty domain part")
    
    return local_part

