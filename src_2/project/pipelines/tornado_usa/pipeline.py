from project.orchestration.runner import run_main_process

from .transform import transform

def start() -> None:
    run_main_process("config/tornado_usa.yaml", transform)