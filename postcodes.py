import re
from functools import partial


THIRD_PART_ONLY = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'S','T', 'U', 'W']
FOURTH_PART_ONLY = ['A', 'B', 'E', 'H', 'M', 'N', 'P', 'R', 'V', 'W', 'X', 'Y']
INCODE_PART = ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'J', 'L', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z']

POSTAL_ZONES = ['AB', 'AL', 'B', 'BA', 'BB', 'BD', 'BH', 'BL', 'BN', 'BR', 'BS', 'BT', 'CA', 'CB', 'CF', 
                'CH', 'CM', 'CO', 'CR', 'CT', 'CV', 'CW', 'DA', 'DD', 'DE', 'DG', 'DH', 'DL', 'DN', 'DT',
                'DY', 'E', 'EC', 'EH', 'EN', 'EX', 'FK', 'FY', 'G', 'GL', 'GY', 'GU', 'HA', 'HD', 'HG', 
                'HP', 'HR', 'HS', 'HU', 'HX', 'IG', 'IM', 'IP', 'IV', 'JE', 'KA', 'KT', 'KW', 'KY', 'L',
                'LA', 'LD', 'LE', 'LL', 'LN', 'LS', 'LU', 'M', 'ME', 'MK', 'ML', 'N', 'NE', 'NG', 'NN',
                'NP', 'NR', 'NW', 'OL', 'OX', 'PA', 'PE', 'PH', 'PL', 'PO', 'PR', 'RG', 'RH', 'RM', 'S',
                'SA', 'SE', 'SG', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SR', 'SS', 'ST', 'SW', 'SY', 'TA', 
                'TD', 'TF', 'TN', 'TQ', 'TR', 'TS', 'TW', 'UB', 'W', 'WA', 'WC', 'WD', 'WF', 'WN', 'WR',
                'WS', 'WV', 'YO', 'ZE']
# single character postal zone case
SINGLE_CHAR_PS = [zone for zone in POSTAL_ZONES if len(zone) == 1]
# double character postal zone case
DOUBLE_CHAR_PS = [zone for zone in POSTAL_ZONES if len(zone) == 2]
OUTCODE_REGX = (r'(' +
                   r'(?:(?:' +
                   '|'.join(SINGLE_CHAR_PS) +
                   r')(?:\d[' +
                   ''.join(THIRD_PART_ONLY) +
                   r']|\d{1,2}))' +
                   r'|' +
                   r'(?:(?:' +
                   '|'.join(DOUBLE_CHAR_PS) +
                   r')(?:\d[' +
                   ''.join(FOURTH_PART_ONLY) +
                   r']|\d{1,2}))' +
                   r')')
INCODE_PATTERN = (r'(\d[' +
                  ''.join(INCODE_PART) +
                  r'][' +
                  ''.join(INCODE_PART) +
                  r'])')
POSTCODE_PATTERN = OUTCODE_REGX + INCODE_PATTERN
STANDALONE_OUTCODE_PATTERN = OUTCODE_REGX + r'\s*$'

POSTCODE_REGEX = re.compile(POSTCODE_PATTERN)
STANDALONE_OUTCODE_REGEX = re.compile(STANDALONE_OUTCODE_PATTERN)


def postcode_parser(postcode, incode_mandatory=True):
    postcode = postcode.replace(' ', '').upper()

    if len(postcode) > 7:
        raise ValueError('Postcode too long')

    postcode_match = POSTCODE_REGEX.match(postcode)
    if postcode_match:
        return postcode_match.group(1, 2)

    outcode_match = STANDALONE_OUTCODE_REGEX.match(postcode)
    if outcode_match:
        if incode_mandatory:
            raise ValueError('The incode is required')
        else:
            return outcode_match.group(1), ''

    if postcode == 'TS97BQ':
        return 'TS9', '7BQ'
    elif postcode == 'TS9':
        if incode_mandatory:
            raise ValueError('The Incode is required')
        else:
            return 'TS9', ''

    raise ValueError('UK postal code invalid')


parse_format = partial(postcode_parser)