from typing import List
from sqlalchemy.orm import Session
from app.commands.base import Command
from app.commands.fiado_command import FiadoCommand
from app.commands.pago_command import PagoCommand
from app.commands.consulta_command import ResumenCommand, HistorialClienteCommand


class CommandRegistry:
    """
    Registro central de comandos. Para agregar un nuevo comando,
    simplemente creá la clase e incorporala en _build_commands().
    """

    def __init__(self):
        self._commands: List[Command] = self._build_commands()

    def _build_commands(self) -> List[Command]:
        return [
            FiadoCommand(),
            PagoCommand(),
            ResumenCommand(),
            HistorialClienteCommand(),
        ]

    def dispatch(self, text: str, db: Session) -> str | None:
        for command in self._commands:
            if command.can_handle(text):
                return command.execute(text, db)
        return None
