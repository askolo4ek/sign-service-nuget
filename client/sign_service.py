from os.path import basename

from requests import get, post

from config import config


class SignServiceClient:
    @staticmethod
    def update_task_status(task: dict) -> None:
        post(f"{config.SIGN_SERVICE.url}/windows/nuget", json=task)

    @staticmethod
    def download_file(url: str) -> str:
        filename: str = basename(url)

        with get(url, stream=True) as response:
            response.raise_for_status()
            filepath: str = "/".join(["static", filename])

            with open(filepath, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        return filepath
