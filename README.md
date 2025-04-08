# Lexic_Analyzer 
by Eduardo Carvalho, Guilherme Bragaia e Nicolas Flores

## Descrição
Este é um analisador léxico desenvolvido em Python, projetado para processar e identificar tokens em um texto de entrada com base em uma gramática definida. O projeto utiliza a biblioteca `PLY` (Python Lex-Yacc) para definição das regras léxicas e sintáticas. Este projeto faz parte do conteúdo prográmatico do componente curricular de Compiladores 2025 do curso de Ciência da Computação da Universidade Federal do Pampa (UNIPAMPA). Orientações pelo docente Claudio Schepke. 

## Estrutura do Projeto
O projeto está organizado nos seguintes arquivos:

- `__main__.py` - Arquivo principal para execução do analisador.
- `tokens.py` - Definição dos tokens usados no analisador.
- `grammar.py` - Regras gramaticais para análise sintática.
- `ex1.por` - Arquivo de exemplo de entrada.
- `Readme.txt` - Documentação auxiliar.
- `.gitignore` - Lista de arquivos e diretórios ignorados pelo Git.
- `pyproject.toml` - Configuração do projeto.

## Requisitos
Para executar o analisador, é necessário ter instalado:
- Python 3.10+
- Biblioteca `PLY`

Instalação das dependências:
```bash
poetry install
```
Acessar o ambiente virtual:
```bash
poetry shell
```

## Como Usar
Para executar o analisador léxico:
```bash
python __main__.py ex1.por
```
Isso processará o arquivo de exemplo `ex1.por`, identificando e classificando os tokens.

## Contribuição
Sinta-se à vontade para contribuir com melhorias no projeto. Para isso:
1. Faça um fork do repositório.
2. Crie uma branch para suas modificações: `git checkout -b minha-feature`.
3. Submeta um pull request.

## Licença
Este projeto está licenciado sob a Licença MIT.

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


