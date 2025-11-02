from parser.polynomial_parser import PolynomialParser

def main() -> None:
    parser = PolynomialParser.build()

    while True:
        try:
            text = input('poly_calc > ')
        except EOFError:
            print('EOFError')
            break
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            break

        result = parser.parse(text)

        if result is not None:
            print(result)

if __name__ == '__main__':
    main()
