from pathlib import Path
from quickfix import ConfigError, FileLogFactory, FileStoreFactory, \
    RuntimeError, SessionSettings, SocketAcceptor, SocketInitiator

from src.service.client_fix import ClientFix
from src.service.server_fix import ServerFix


def run_application(config_path: Path, is_server: bool):
    settings = SessionSettings(str(config_path))
    storefactory = FileStoreFactory(settings)
    logfactory = FileLogFactory(settings)

    application = ServerFix() if is_server else ClientFix()

    socket_args = (application, storefactory, settings, logfactory)
    socket = SocketAcceptor(*socket_args) if is_server else SocketInitiator(*socket_args)

    try:
        socket.start()
        application.run()
    except (ConfigError, RuntimeError) as error:
        print(error)
    finally:
        socket.stop()


def run_client(config_path: Path):
    run_application(config_path, False)


def run_server(config_path: Path):
    run_application(config_path, True)
