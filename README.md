# Mini Shell com Chamadas ao Sistema

Projeto da II Unidade da disciplina de Sistemas Operacionais.

O mini shell exibe o prompt `>`, lê comandos com argumentos, cria um processo
filho com `os.fork()`, executa programas com `os.execvp()` e aguarda o filho
com `os.wait()`. Digite `exit` para encerrar.

Comandos internos: `cd [diretório]`, `pwd`, `help` e `exit`.

Execute em um sistema POSIX (como Linux ou macOS) com:

```sh
python3 main.py
```

`os.fork()` não está disponível no Windows.
