from polynomial_interpreter import PolynomialInterpreter

def main() -> None:
    p = PolynomialInterpreter('3.58*x**5')
    result = p.evaulate(x=2, y=1, z=0.5)

    print(f'Expression: {p.get_text()}')
    print(f'Result: {result}')

    p = PolynomialInterpreter('6.28*x**2*y*z')
    result = p.evaulate(x=2, y=1, z=0.5)

    print(f'Expression: {p.get_text()}')
    print(f'Result: {result}')

    p = PolynomialInterpreter('x*y*z**3')
    result = p.evaulate(x=2, y=1, z=0.5)

    print(f'Expression: {p.get_text()}')
    print(f'Result: {result}')

    p = PolynomialInterpreter('3.58*x**5 + 6.28*x**2*y*z + x*y*z**3 + 3')
    result = p.evaulate(x=2, y=1, z=0.5)

    print(f'Expression: {p.get_text()}')
    print(f'Result: {result}')

if __name__ == '__main__':
    main()
