from project.orchestration.runner import run_main_process

from .transform import transform

def start() -> None:
    run_main_process("config/wildfire_global.yaml", transform)