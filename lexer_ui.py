from lexer.polynomial_lexer import PolynomialLexer

def main() -> None:
    lexer = PolynomialLexer.build()

    while True:
        try:
            text = input('lexer > ')
        except EOFError:
            print('EOFError')
            break
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            break

        tokens = lexer.tokenize(text)

        if tokens is not None:
            print(tokens)

if __name__ == '__main__':
    main()
