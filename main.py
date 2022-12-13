import argparse
from lang_yacc import parser, symbol_table, errors
from symbol_table.scope.out_of_scope_exception import OutOfScopeException

CLI = argparse.ArgumentParser()
CLI.add_argument("filename")
CLI.add_argument("-t", "--table", action='store_true')
CLI.add_argument("-d", "--debug", action='store_true')


if __name__ == '__main__':
    args = CLI.parse_args()
    with open(args.filename, 'r') as file:
        data = file.read()
        symbol_table.program = data
        result = parser.parse(data, debug=args.debug)
        try:
            symbol_table.end()
        except OutOfScopeException as e:
            errors.append(str(e))

        if args.table:
            print("TABELA DE SÍMBOLOS")
            symbol_table.pretty_print()

        print("Árvore")
        print(result)


