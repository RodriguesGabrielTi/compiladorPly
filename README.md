# compiladorPly
Compilador léxico e sintático utilizando a biblioteca Ply

### Requisitos

 - Python 3.10.5
 - pyenv e pyenv-virtualenv

Instalação do pyenv e pyenv-virtualenv:

```bash
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv

$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc

$ exec "$SHELL"

$ git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
$ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
$ exec "$SHELL"
```

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
- -r ou --raw para a saída da ser mostrada no terminal no lugar de salva em um arquivo;
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

