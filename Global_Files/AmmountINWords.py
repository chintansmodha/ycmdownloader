from num2words import num2words


def inwords(a):
    result = ''
    result1 = ''
    stringofa = str("%.2f" % float(a))
    indexofdot = stringofa.index('.')
    beforedot = stringofa[:indexofdot]
    afterdot = stringofa[indexofdot + 1:]

    result = num2words(beforedot, lang='en_IN')
    result = result.replace(',', '')
    result = result.replace('-', ' ')
    result = result.title()
    result = result.replace('And', '')

    if afterdot[0] == '0':
        if afterdot[1] == "0":
            result = result + " Only"
        elif afterdot[1] != "0":
            result1 = num2words(afterdot[1], lang='en_IN')
            result1 = result1.replace('-', ' ')
            result1 = result1.title()
            result = result + " Rupees And " + result1 + " Paisa"

    elif afterdot[0] != '0':
        if afterdot[1] == "0":
            result1 = num2words(afterdot, lang='en_IN')
            result1 = result1.replace('-', ' ')
            result1 = result1.title()
            result = result + " Rupees And " + result1 + " Paisa"
        elif afterdot[1] != "0":
            result1 = num2words(afterdot, lang='en_IN')
            result1 = result1.replace('-', ' ')
            result1 = result1.title()
            result = result + " Rupees And " + result1 + " Paisa"

    result = "Rupees " + result
    return result