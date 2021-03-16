
"""A very basic implementation of IEEE 754 in python 3 for learning purposes.

Date: March 16, 2021.
Author: Jose Noriega<josenoriega723@gmail.com>
"""

def int_to_binary(int_number, available_places):
    """Converts an integer number into its binary representation."""
    bits = ''

    while int_number > 0 and len(bits) < available_places:
        quotient = int_number / 2;
        has_decimal = quotient % 1 != 0

        if has_decimal:
            bits = '1' + bits
        else:
            bits = '0' + bits
        
        int_number = int(quotient)

    if not bits:
        bits = '0'

    return bits

def get_number_as_ieee754(number):
    """Given a floating point number, it returns its binary representation based on IEEE 754.
    
    Returns:
        str: Binary representation of the given floating point number.
    """
    number_str = str(number).replace('-', '')
    decimal_part = number_str.split('.')[0]
    fraction_part = number_str.split('.')[1]

    signal_bit = (1 if number < 0 else 0)

    decimal_bits = ''
    fraction_bits = ''

    mantissa_available_bits = 23

    if decimal_part:
        decimal_part = int(decimal_part)
        decimal_bits = int_to_binary(decimal_part, mantissa_available_bits)

    if fraction_part:
        fraction_part = float('0.' + fraction_part)
        extra_bits = 0
        count_zeros_to_the_left = True

        while len(fraction_bits) < (mantissa_available_bits + extra_bits) :
            product = fraction_part * 2

            bit = '1' if product >= 1 else '0'

            fraction_bits += bit

            fraction_part = str(product).split('.')[1]

            if fraction_part == '0':
                fraction_part = 0
                break

            fraction_part = float('0.' + fraction_part)

            if count_zeros_to_the_left:
                extra_bits = 0
                for fraction_bit in fraction_bits:
                    if fraction_bit == '0':
                        extra_bits += 1
                    else:
                        count_zeros_to_the_left = False
                        break
        
        if not fraction_bits:
            fraction_bits = '0'

        # round binary
        if fraction_part != 0:
            fraction_bits += '1'

    mantissa = decimal_bits + fraction_bits
    exponent = 0
    zeros_shifted = mantissa.find('1')

    exponent = len(decimal_bits) - 1

    if decimal_bits == '0':
        exponent -= 1

    if zeros_shifted > 0:
        exponent -= zeros_shifted - 1

    mantissa = mantissa[zeros_shifted + 1:mantissa_available_bits].ljust(mantissa_available_bits, '0')

    exponent += 127

    exponent_bits = int_to_binary(exponent, mantissa_available_bits).rjust(8, '0')

    return f'{signal_bit}{exponent_bits}{mantissa}'


def binary_to_int(binary):
    """Converts a binary representation of an integer number into its decimal value."""
    output = 0
    for idx, bit in enumerate(reversed(binary)):
        if bit == '1':
            output += 2 ** idx

    return output

def get_float_from_ieee754(binary):
    """Converts a IEEE 754 binary representation into its decimal value."""

    # chunks
    signal_bit = binary[0]
    exponent_binary = binary[1:9]
    mantissa = binary[9:]

    decimal_bits = '0'
    fraction_bits = '0'

    exponent = binary_to_int(exponent_binary) - 127

    if exponent >= 0:
        decimal_bits = '1' + mantissa[: exponent]
        fraction_bits = mantissa[exponent:]
    else:
        fraction_bits = '0' * (abs(exponent) - 1) + '1' + mantissa

    decimal_number = binary_to_int(decimal_bits)

    fraction_number = 0
    for idx, char in enumerate(fraction_bits):
        if char == '1':
            fraction_number += 2 ** -(idx + 1)

    return (-1)**int(signal_bit) * float(decimal_number + fraction_number)

# Testing
l = [
    4.18,
    -0.86,
    3.95,
    5.96,
    -3.75,
    -6.04,
    7.38,
    0.32,
    4.64,
    3.74,
    4.2,
    -5.5,
    0.93,
    9.85,
    2.09,
    4.33,
    -3.72,
    2.72,
    6.09,
    2.04,
    -6.35,
    6.12,
    299.59,
    7.21,
    5.82,
]
for n in l:
    ieee754_binary = get_number_as_ieee754(n)
    float_from_ieee754 = get_float_from_ieee754(ieee754_binary)
    print(ieee754_binary)
    print(f'{n}: {float_from_ieee754}')
