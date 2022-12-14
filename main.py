import argparse
import json
import os

from lang_yacc import parser, symbol_table, errors
from symbol_table.scope.out_of_scope_exception import OutOfScopeException

CLI = argparse.ArgumentParser()
CLI.add_argument("filename")
CLI.add_argument("-t", "--table", action='store_true')
CLI.add_argument("-d", "--debug", action='store_true')
CLI.add_argument("-s", "--save", action='store_true')


def convert_to_dict(t: tuple):
    t_final = []
    for i, item in enumerate(t):
        if i == 0:
            continue
        if type(item) is tuple:
            result = convert_to_dict(item)
            production = result[0]
            value = result[1]
            t_final.append({production: value})
        else:
            t_final.append(item)
    return t[0], t_final


def pretty_print_tuples(t: tuple, save, filename: str):
    result = convert_to_dict(t)
    production = result[0]
    value = result[1]
    t_dict = {production: value}

    jstr = json.dumps(t_dict, indent=2)
    if save:
        filename = os.path.basename(filename) + ".json"
        with open(filename, "w+") as outfile:
            outfile.write(jstr)
        print("Resultado salvo em", filename)
    else:
        print("Árvore do arquivo", filename)
        print(jstr)


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

        if result is not None:
            pretty_print_tuples(result, args.save, args.filename)


