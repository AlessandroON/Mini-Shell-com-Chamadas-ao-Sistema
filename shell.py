"""Leitura, interpretação e execução dos comandos do mini shell."""

import os
import shlex

from shell_builtins import executar_builtin


def escrever(texto):
    """Escreve texto no terminal usando a chamada write()."""
    dados = texto.encode("utf-8", errors="replace")
    while dados:
        escritos = os.write(1, dados)
        dados = dados[escritos:]


def ler_linha(buffer):
    """Lê a entrada padrão com read() e devolve uma linha ou None no EOF."""
    while b"\n" not in buffer[0]:
        trecho = os.read(0, 4096)
        if not trecho:
            if not buffer[0]:
                return None
            linha = bytes(buffer[0])
            buffer[0].clear()
            return linha.decode("utf-8", errors="replace")
        buffer[0].extend(trecho)

    fim = buffer[0].index(b"\n")
    linha = bytes(buffer[0][:fim])
    del buffer[0][:fim + 1]
    return linha.decode("utf-8", errors="replace")


def interpretar_linha(linha):
    """Converte uma linha em comando e argumentos; retorna lista vazia se inválida/vazia."""
    try:
        return shlex.split(linha)
    except ValueError as erro:
        escrever(f"Erro ao interpretar comando: {erro}\n")
        return []


def executar_comando(comando, argumentos):
    """Executa programa externo com fork/execvp e aguarda o processo filho."""
    try:
        pid_filho = os.fork()
    except OSError as erro:
        escrever(f"Erro ao criar processo filho: {erro}\n")
        return

    if pid_filho == 0:
        try:
            os.execvp(comando, [comando, *argumentos])
        except FileNotFoundError:
            mensagem = f"Comando não encontrado: {comando}\n"
        except PermissionError:
            mensagem = f"Permissão negada ao executar: {comando}\n"
        except OSError as erro:
            mensagem = f"Erro ao executar {comando}: {erro}\n"
        os.write(2, mensagem.encode("utf-8", errors="replace"))
        os._exit(127)

    while True:
        try:
            os.wait()
            break
        except InterruptedError:
            continue
        except ChildProcessError as erro:
            escrever(f"Erro ao aguardar processo filho: {erro}\n")
            break


def mini_shell():
    """Controla o prompt e o ciclo principal do mini shell."""
    buffer = bytearray()
    while True:
        escrever("> ")
        try:
            linha = ler_linha([buffer])
        except KeyboardInterrupt:
            escrever("\nUse 'exit' para sair.\n")
            continue
        if linha is None:
            escrever("\n")
            break
        linha = linha.strip()
        if not linha:
            continue

        partes = interpretar_linha(linha)
        if not partes:
            continue

        comando, *argumentos = partes
        resultado = executar_builtin(comando, argumentos)
        if resultado == "exit":
            escrever("Isso é tudo pessoal!!\n")
            break
        if resultado:
            continue
        executar_comando(comando, argumentos)
