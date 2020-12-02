from decimal import Decimal
import random
import string


def convert_weight_unit(from_, to, weight):
    """单位转换"""
    units = ['lb', 'oz', 'kg', 'g']
    kg_2_dict = {
        'oz': Decimal('35.2739619'),
        'lb': Decimal('2.2046226'),
        'g': Decimal(1000),
        'kg': Decimal(1),
    }

    if from_ not in units or to not in units:
        raise Exception('Invalid Unit')
    if from_ == to:
        return weight
    return kg_2_dict.get(to) / kg_2_dict.get(from_) * weight


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(string_length))
