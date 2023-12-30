def input_checker(text):

    if text == '':
        return [], 'Please insert the 9 numbers'
    
    numbers = [int(x) for x in text.split()]

    if len(numbers) != 9:
        return [], f'I found {len(numbers)} number{"s" * (len(numbers) > 1)}. You need 9!'
    
    for number in numbers:
        if number < 1 or number > 42:
            return [], f'You wrote {number}. The numbers you be in the range 1-42'
        
        if numbers.count(number) > 1:
            return [], f'You wrote {number} more than once!!!'
        
    return numbers, 'Your plate has now been changed!'