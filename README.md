# Mini Shell com Chamadas ao Sistema

Projeto da II Unidade da disciplina de Sistemas Operacionais. O programa implementa um shell simples em Python para demonstrar chamadas ao sistema como `read`, `write`, `fork`, `execvp` e `wait`.

## O que é um mini shell?

Um shell recebe comandos digitados, interpreta o texto e inicia programas. Neste projeto, comandos como `ls` e `echo` são executados como processos filhos. Alguns comandos, como `cd` e `exit`, são implementados pelo próprio mini shell.

## Requisitos

- Python 3;
- Linux, macOS ou outro sistema POSIX. No Windows, use o Ubuntu pelo WSL.

O mini shell depende de `os.fork()`, que não está disponível no Python nativo do Windows.

## Executar no Ubuntu/WSL

No terminal integrado do VS Code aberto no Ubuntu, entre na pasta do projeto e inicie o programa:

```sh
cd /mnt/c/Sites/Mini-Shell-com-Chamadas-ao-Sistema
python3 main.py
```

Se o projeto estiver dentro do sistema de arquivos do Ubuntu, use o caminho correspondente, por exemplo `cd ~/meu-projeto`.

Quando aparecer `>`, digite um comando. Para encerrar o mini shell, use `exit`.

## Exemplos de uso

```text
> pwd
/mnt/c/Sites/Mini-Shell-com-Chamadas-ao-Sistema
> ls
README.md  main.py  shell.py  shell_builtins.py
> ls -l
> echo "Olá, mundo!"
Olá, mundo!
> cd /tmp
> pwd
/tmp
> cd
> help
> exit
```

`pwd` mostra a pasta atual; `ls` lista seus arquivos; `ls -l` mostra detalhes. O mini shell passa comandos externos e seus argumentos ao sistema. Aspas agrupam palavras com espaços, como em `echo "Olá, mundo!"`.

Se um programa não existir ou não puder ser executado, o mini shell mostra uma mensagem de erro. Ele não implementa recursos de shells completos, como pipes (`|`), redirecionamento (`>`) ou execução de vários comandos em sequência.

## Comandos internos

| Comando | O que faz |
| --- | --- |
| `cd [diretório]` | Muda a pasta atual. Sem argumento, vai para a pasta pessoal do usuário. Exemplo: `cd /tmp` ou `cd "/mnt/c/Users/Usuario/Meus Arquivos"`. |
| `pwd` | Mostra o caminho da pasta atual. |
| `help` | Mostra a lista de comandos internos e uma descrição breve. |
| `exit` | Encerra o mini shell. |

Os comandos internos rodam no processo do mini shell. Em particular, isso permite que a mudança feita por `cd` continue valendo para os próximos comandos.

## Arquivos e funções

### `main.py`

É o ponto de entrada do programa. Quando executado diretamente, importa e chama `mini_shell()`.

### `shell.py`

- `escrever(texto)`: converte o texto para UTF-8 e o escreve na saída padrão usando `os.write()`. Repete a escrita se o sistema gravar apenas parte dos bytes.
- `ler_linha(buffer)`: lê bytes da entrada padrão usando `os.read()` e devolve uma linha de texto. Mantém no buffer os bytes que pertencem às linhas seguintes e devolve `None` quando a entrada termina.
- `interpretar_linha(linha)`: separa a linha em comando e argumentos com `shlex.split()`, respeitando aspas. Linhas vazias produzem uma lista vazia; aspas inválidas geram uma mensagem de erro.
- `executar_comando(comando, argumentos)`: cria um processo filho com `os.fork()`. O filho substitui sua execução pelo programa pedido usando `os.execvp()`; o processo pai aguarda o filho com `os.wait()`.
- `mini_shell()`: controla o ciclo principal: mostra o prompt, lê e interpreta a entrada, executa comandos internos ou inicia programas externos, até receber `exit` ou o fim da entrada.

### `shell_builtins.py`

- `executar_builtin(comando, argumentos)`: verifica se o comando é interno. Implementa `cd`, `pwd`, `help` e `exit`; retorna um valor que informa ao ciclo principal se o comando foi reconhecido ou se o shell deve terminar.

## Chamadas ao sistema demonstradas

- `os.read()`: recebe a entrada digitada pelo usuário;
- `os.write()`: exibe o prompt, mensagens e erros;
- `os.fork()`: cria o processo filho para executar um programa externo;
- `os.execvp()`: executa o programa indicado no processo filho, procurando-o nos diretórios do `PATH`;
- `os.wait()`: faz o processo pai aguardar o término do processo filho.
