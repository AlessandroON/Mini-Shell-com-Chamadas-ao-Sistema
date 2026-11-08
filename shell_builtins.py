"""Comandos internos executados no próprio processo do mini shell."""

import os


def executar_builtin(comando, argumentos):
    """Executa um comando interno; retorna True se ele foi reconhecido."""
    if comando == "exit":
        return "exit"

    if comando == "cd":
        destino = argumentos[0] if argumentos else os.path.expanduser("~")
        try:
            os.chdir(destino)
        except FileNotFoundError:
            print(f"cd: diretório não encontrado: {destino}")
        except NotADirectoryError:
            print(f"cd: não é um diretório: {destino}")
        except PermissionError:
            print(f"cd: permissão negada: {destino}")
        return True

    if comando == "pwd":
        print(os.getcwd())
        return True

    if comando == "help":
        print("Comandos internos: cd [diretório], pwd, help, exit")
        print("Outros comandos são executados como programas do sistema.")
        return True

    return False
