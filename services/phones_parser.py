from tempfile import SpooledTemporaryFile
import re
from typing import List

from api.schemas.phone import PhonesWithName

COUNTRY_PHONE_CODE = '38'


def parse_phones(phones: List[str]) -> dict:
    valid_phones = {}
    invalid_phones = []

    for phone in phones:
        phone_number = phone.rstrip()[-10:]

        if valid_phones.get(phone_number):
            invalid_phones.append(phone_number + ' (duplicate)')
            continue

        if phone_is_valid(phone_number):
            valid_phones[phone_number] = COUNTRY_PHONE_CODE + phone_number
        else:
            invalid_phones.append(phone_number + ' (invalid)')

    return {
        'valid': list(valid_phones.values()),
        'invalid': list(invalid_phones)
    }


def parse_phones_with_names(phones: List[PhonesWithName]) -> dict:
    valid_phones = {}
    invalid_phones = []

    for phone in phones:
        phone_number = phone.phone.rstrip()[-10:]
        name = phone.name.rstrip('\r')

        if valid_phones.get(phone_number):
            invalid_phones.append(f'{phone_number},{name} (duplicate)')
            continue

        if name_is_valid(name) and phone_is_valid(phone_number):
            valid_phones[phone_number] = PhonesWithName(
                name=name,
                phone=COUNTRY_PHONE_CODE + phone_number
            )
        else:
            invalid_phones.append(f'{phone_number},{name} (invalid)')

    return {
        'valid': valid_phones.values(),
        'invalid': invalid_phones
    }


def parse_phones_file(file: SpooledTemporaryFile) -> dict:
    phones_list = file.read().decode().split('\n')

    return parse_phones(phones_list)


def parse_phones_with_name_file(file: SpooledTemporaryFile) -> dict:
    phones_list = file.read().decode().split('\n')

    valid_phones = {}
    invalid_phones = []

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

        if name_is_valid(name) and phone_is_valid(phone):
            valid_phones[phone] = PhonesWithName(
                name=name,
                phone=COUNTRY_PHONE_CODE + phone
            )
        else:
            invalid_phones.append(item + ' (invalid)')

    return {
        'valid': list(valid_phones.values()),
        'invalid': list(invalid_phones)
    }


def phone_is_valid(phone: str) -> bool:
    if re.fullmatch(r'^0[0-9]{9}$', phone):
        return True
    return False


def name_is_valid(name: str) -> bool:
    if re.match('^[a-zA-Zа-яА-ЯҐЄІЇґєії\-?\s?\'?]{2,30}$', name):
        return True
    return False
