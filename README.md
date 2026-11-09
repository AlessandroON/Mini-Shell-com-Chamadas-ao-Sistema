# Mini Shell com Chamadas ao Sistema

Projeto da II Unidade da disciplina de Sistemas Operacionais. O mini shell lê
comandos da entrada padrão com `os.read()`, mostra o prompt e mensagens com
`os.write()`, cria um processo filho com `os.fork()`, executa programas com
`os.execvp()` e aguarda o processo filho com `os.wait()`.

## Executar

Use Python 3 em um sistema POSIX, como Linux ou macOS:

```sh
python3 main.py
```

`os.fork()` não está disponível no Windows.

## Exemplos

```text
> ls -l
> cat README.md
> echo Olá, mundo!
> comando-inexistente
Comando não encontrado: comando-inexistente
> exit
```

O parser separa argumentos e aceita aspas, por exemplo `echo "Olá, mundo!"`.
Comandos internos: `cd [diretório]`, `pwd`, `help` e `exit`.

## Organização

- `ler_linha()` e `interpretar_linha()`: leitura e parsing da entrada.
- `executar_comando()`: criação, execução e espera do processo filho.
- `mini_shell()`: prompt e controle do loop principal.
- `shell_builtins.py`: implementação dos comandos internos.
