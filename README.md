# compiladorPly
Compilador léxico e sintático utilizando a biblioteca Ply

## Execução com make:

``
make run ARGS=""
``

ARGS deve conter o caminho para o arquivo, por exemplo:

``
make run ARGS="test_files/test1.lcc"
``

Como parâmetro opcional, é possível colocar:
- -t ou --table, para a tabela de atributos também aparecer na saída;
- -s ou --save para a saída da análise sintática ser mostrada na tela;
- -d ou --debug para rodar o programa com logs de debug.

Recomenda-se rodar o programa com as duas primeira opções para melhor legibilidade:

``
make run ARGS="test_files/test1.lcc -s -t"
``

## Execução com python:

No caso de python, os parâmetros não devem ficar dentro da variável ARGS:

``
python main.py -t -s"
``

