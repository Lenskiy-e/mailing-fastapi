from tempfile import SpooledTemporaryFile
import re
from schemas.phone import PhoneWithNameCreateRequest


def parse_phones_file(file: SpooledTemporaryFile) -> dict:
    phones_list = file.read().decode().split('\n')
    valid_phones = {}
    invalid_phones = []

    for phone in phones_list:
        phone_number = phone.rstrip()[-10:]

        if valid_phones.get(phone_number):
            invalid_phones.append(phone_number + ' (duplicate)')
            continue

        if re.match(r'^0[0-9]{9}$', phone_number):
            valid_phones[phone_number] = phone_number
        else:
            invalid_phones.append(phone_number + ' (invalid)')

    return {
        'valid': valid_phones.values(),
        'invalid': invalid_phones
    }


async def parse_phones_with_name(file: SpooledTemporaryFile) -> dict:
    file_content = await file.read()
    phones_list = file_content.decode().split('\n')

    valid_phones = {}
    invalid_phones = []
    name_pattern = '^[a-zA-Zа-яА-ЯҐЄІЇґєії\-?\s?\'?]{2,30}$'
    phone_pattern = '^0[0-9]{9}$'

    for item in phones_list:
        parts = item.split(',')

        if len(parts) != 2:
            invalid_phones.append(item)
            continue

        phone = parts[0].rstrip()[-10:]
        name = parts[1].rstrip('\r')

        if valid_phones.get(phone):
            invalid_phones.append(item + ' (duplicate)')
            continue

        if re.match(name_pattern, name) and re.match(phone_pattern, phone):
            valid_phones[phone] = PhoneWithNameCreateRequest(
                name=name,
                phone=phone
            )
        else:
            invalid_phones.append(item + ' (invalid)')

    return {
        'valid': valid_phones.values(),
        'invalid': invalid_phones
    }
