import re
from functools import partial


INWARD_ELEM = ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'J', 'L', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z']

POSTAL_ZONES = ['AB', 'AL', 'B', 'BA', 'BB', 'BD', 'BH', 'BL', 'BN', 'BR', 'BS', 'BT', 'CA', 'CB', 'CF',
                'CH', 'CM', 'CO', 'CR', 'CT', 'CV', 'CW', 'DA', 'DD', 'DE', 'DG', 'DH', 'DL', 'DN', 'DT',
                'DY', 'E', 'EC', 'EH', 'EN', 'EX', 'FK', 'FY', 'G', 'GL', 'GY', 'GU', 'HA', 'HD', 'HG',
                'HP', 'HR', 'HS', 'HU', 'HX', 'IG', 'IM', 'IP', 'IV', 'JE', 'KA', 'KT', 'KW', 'KY', 'L',
                'LA', 'LD', 'LE', 'LL', 'LN', 'LS', 'LU', 'M', 'ME', 'MK', 'ML', 'N', 'NE', 'NG', 'NN',
                'NP', 'NR', 'NW', 'OL', 'OX', 'PA', 'PE', 'PH', 'PL', 'PO', 'PR', 'RG', 'RH', 'RM', 'S',
                'SA', 'SE', 'SG', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SR', 'SS', 'ST', 'SW', 'SY', 'TA',
                'TD', 'TF', 'TN', 'TQ', 'TR', 'TS', 'TW', 'UB', 'W', 'WA', 'WC', 'WD', 'WF', 'WN', 'WR',
                'WS', 'WV', 'YO', 'ZE']

# Areas with only single-digit districts
SINGLE_DIGIT_AREAS = ['BR', 'FY', 'HA', 'HD', 'HG', 'HR', 'HS', 'HX', 'JE', 'LD', 'SM', 'SR', 'WC', 'WN', 'ZE']

# Areas with only double-digit districts
DOUBLE_DIGIT_AREAS = ['AB', 'LL', 'SO']

# letters to exclude in first position
FIRST_POSITION_EXCLUDED = ['Q', 'V', 'X']

# letters to be excluded in second position
SECOND_POSITION_EXCLUDED = ['I', 'J', 'Z']

# The only letters to appear in the third position
THIRD_PART_ONLY = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'S', 'T', 'U', 'W']

# The only letters to appear in the fourth position
FOURTH_PART_ONLY = ['A', 'B', 'E', 'H', 'M', 'N', 'P', 'R', 'V', 'W', 'X', 'Y']

# Areas with a district '0' (zero). We exclude BS as this is the only one which accepts 10 and goes up-to 99
DISTRICT_ZERO_AREAS = ['BL', 'CM', 'CR', 'FY', 'HA', 'PR', 'SL', 'SS']

SPECIAL_AREA_WITH_TEN = ['BS']

# single character postal zone cases
SINGLE_CHAR_PC = [zone for zone in POSTAL_ZONES if len(zone) == 1]
# double character postal zone cases
DOUBLE_CHAR_PC = [zone for zone in POSTAL_ZONES if len(zone) == 2
                  and zone not in (SINGLE_DIGIT_AREAS + DOUBLE_DIGIT_AREAS + DISTRICT_ZERO_AREAS + SPECIAL_AREA_WITH_TEN)]
# outcode
OUTWARD_PATTERN = (r'(' +
                   r'(?:(?:' +
                   '|'.join(SINGLE_CHAR_PC) +
                   r')(?:\d[' +
                   ''.join(THIRD_PART_ONLY) +
                   r']|\d{1,2}))' +
                   r'|' +
                   r'(?:(?:' +
                   '|'.join(DOUBLE_CHAR_PC) +
                   r')(?:\d[' +
                   ''.join(FOURTH_PART_ONLY) +
                   r']|[1-9]{1,2}))' +
                   r'|(?:(?:' + '|'.join(SINGLE_DIGIT_AREAS) + ')\d{1})'
                   r'|(?:(?:' + '|'.join(DOUBLE_DIGIT_AREAS) + ')(?:[1-9][1-9]{1,2}))'
                   r'|(?:(?:' + '|'.join(DISTRICT_ZERO_AREAS) + ')[0-9])'
                   r'|(?:BS(?:[1-9][0-9]))'
                   r')')
# incode
INWARD_PATTERN = (r'(\d[' +
                  ''.join(INWARD_ELEM) +
                  r'][' +
                  ''.join(INWARD_ELEM) +
                  r'])')
POSTCODE_PATTERN = OUTWARD_PATTERN + INWARD_PATTERN
STANDALONE_OUTWARD_PATTERN = OUTWARD_PATTERN + r'\s*$'

POSTCODE_REGEX = re.compile(POSTCODE_PATTERN)
STANDALONE_OUTWARD_REGEX = re.compile(STANDALONE_OUTWARD_PATTERN)

print(POSTCODE_PATTERN)
def postcode_parser(postcode, inward_mandatory=True):
    postcode = postcode.replace(' ', '').upper()

    if len(postcode) > 7:
        raise ValueError('Postcode too long')

    postcode_match = POSTCODE_REGEX.match(postcode)
    if postcode_match:
        return postcode_match.group(1, 2)

    outcode_match = STANDALONE_OUTWARD_REGEX.match(postcode)
    if outcode_match:
        if inward_mandatory:
            raise ValueError('The incode is required')
        else:
            return outcode_match.group(1), ''

    if postcode == 'GIR0AA':
        return 'GIR', '0AA'
    elif postcode == '0AA':
        if inward_mandatory:
            raise ValueError('The Incode is required')
        else:
            return '0AA', ''

    raise ValueError('UK postal code invalid')


parse_format = partial(postcode_parser)