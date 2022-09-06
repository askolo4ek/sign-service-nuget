from flask import Flask

from api import create_app

from config import config


def main() -> None:
    app: Flask = create_app()

    app.run(host=config.SERVICE.host,
            port=config.SERVICE.port,
            debug=config.SERVICE.debug,
            threaded=config.SERVICE.threaded)


if __name__ == "__main__":
    main()
