import argparse


def sumar(a: float, b: float) -> float:
    return a + b


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Suma dos números.")
    parser.add_argument("a", type=float, help="Primer número")
    parser.add_argument("b", type=float, help="Segundo número")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    resultado = sumar(args.a, args.b)
    print(resultado)


if __name__ == "__main__":
    main()
