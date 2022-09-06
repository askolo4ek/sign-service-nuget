from __future__ import annotations

from subprocess import Popen, PIPE, STDOUT


def console(command: str, shell: bool = False) -> tuple[str, int] | None:
    proc: Popen[bytes] | Popen = Popen(command, shell=shell, stdout=PIPE, stderr=STDOUT)

    std_err, _ = proc.communicate()
    exit_code: int = proc.returncode

    return std_err.decode("utf-8"), exit_code
