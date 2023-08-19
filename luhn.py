def luhn_checksum(card_number):
    def digits_of_card(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of_card(card_number)

    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    checksum = 0
    checksum += sum(odd_digits)

    for digit in even_digits:
        checksum += sum(digits_of_card(digit*2))
        
    return checksum % 10

userCardNumber = input("Enter a card number:\n")

print('Valid') if luhn_checksum(userCardNumber) == 0 else print('Invalid') # 4532015112830366 is Valid
