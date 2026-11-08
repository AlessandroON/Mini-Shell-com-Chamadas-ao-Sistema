"""Leitura e execuÃ§Ã£o dos comandos do mini shell."""

import os
import shlex

from shell_builtins import executar_builtin


def executar_comando(comando, argumentos):
    """Executa programa externo com fork/execvp e espera seu terrmino."""
    try:
        pid_filho = os.fork()
    except OSError as erro:
        print(f"Erro ao criar processo filho: {erro}")
        return

    if pid_filho == 0:
        try:
            os.execvp(comando, [comando, *argumentos])
        except FileNotFoundError:
            print(f"Comando não encontrado: {comando}", flush=True)
        except PermissionError:
            print(f"Permissão negada ao executar: {comando}", flush=True)
        except OSError as erro:
            print(f"Erro ao executar {comando}: {erro}", flush=True)
        os._exit(127)

    try:
        os.wait()
    except InterruptedError:
        # Se a espera for interrompida, continua aguardando o filho.
        while True:
            try:
                os.waitpid(pid_filho, 0)
                break
            except InterruptedError:
                continue
    except ChildProcessError as erro:
        print(f"Erro ao aguardar processo filho: {erro}")


def mini_shell():
    while True:
        try:
            linha = input("> ").strip()
        except KeyboardInterrupt:
            print("\nUse 'exit' para sair.")
            continue
        except EOFError:
            print()
            break

        if not linha:
            continue

        try:
            partes = shlex.split(linha)
        except ValueError as erro:
            print(f"Erro ao interpretar comando: {erro}")
            continue

        if not partes:
            continue

        comando, *argumentos = partes
        resultado = executar_builtin(comando, argumentos)
        if resultado == "exit":
            print("Até mais!")
            break
        if resultado:
            continue

        executar_comando(comando, argumentos)

