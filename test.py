def multiples_three_five(below):
    yield (['ThreeFive' if n % 3 == 0 and n % 5 == 0 else 'Three' if n % 3 == 0 else
        'Five' if n % 5 == 0 else n for n in range(1, below+1)])

x = next(multiples_three_five(100))


print(x)

