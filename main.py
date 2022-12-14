import argparse
import json
import os

from lang_yacc import parser, symbol_table, errors
from lang_lex import lexer
from symbol_table.scope.out_of_scope_exception import OutOfScopeException

CLI = argparse.ArgumentParser()
CLI.add_argument("filename")
CLI.add_argument("-t", "--table", action='store_true')
CLI.add_argument("-d", "--debug", action='store_true')
CLI.add_argument("-r", "--raw", action='store_true')


# Comverte tupla para dicionário
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


# Printa a tupla em formato JSON
def pretty_print_tuples(t: tuple, raw, filename: str):
    print("Arquivo passou na análise sintática")
    result = convert_to_dict(t)
    production = result[0]
    value = result[1]
    t_dict = {production: value}

    jstr = json.dumps(t_dict, indent=2)
    if not raw:
        filename = os.path.basename(filename) + ".json"
        with open(filename, "w+") as outfile:
            outfile.write(jstr)
        print("Resultado salvo em", filename)
    else:
        print("Árvore do arquivo", filename)
        print(jstr)


# Análise léxica
def lex(data: str):
    symbol_table.program = data
    lexer.input(data)
    print("Tokens")
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)
    try:
        symbol_table.end()
    except OutOfScopeException as e:
        errors.append(str(e))
    if args.table:
        print()
        print("Tabela de símbolos")
        symbol_table.pretty_print()

    for error in errors:
        print(error)

    if len(errors) > 0:
        exit(1)

    print("Arquivo passou na análise léxica")


# Análise sintática
def parse(data: str):
    symbol_table.program = data
    result = parser.parse(data, debug=args.debug)
    if result is not None and len(errors) == 0:
        pretty_print_tuples(result, args.raw, args.filename)


if __name__ == '__main__':
    args = CLI.parse_args()
    with open(args.filename, 'r') as file:
        file_str = file.read()
        lex(file_str)
        print()
        symbol_table.clear()
        print()
        parse(file_str)


