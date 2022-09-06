from __future__ import annotations

from http import HTTPStatus
from os import remove
from os.path import basename, abspath
from threading import Thread
from typing import Any

from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser

from common import console
from client import SignServiceClient

from config import config


def thread_signing(task: dict) -> None:
    filename: str = basename(task["filepath"])
    url: str = "/".join([config.SIGN_SERVICE.url, "static", "nuget", filename])

    downloaded_path: str = SignServiceClient.download_file(url)

    cmd: str = " ".join(["nuget sign",
                         abspath(downloaded_path),
                         "-ForceEnglishOutput",
                         "-CertificateFingerprint",
                         config.NUGET.certificate,
                         "-Timestamper",
                         config.NUGET.timestamp_url])

    std_err, exit_code = console(cmd, shell=True)

    if exit_code == 0:
        task["message"] = "Signed!"
        task["status"] = "Done"
    else:
        task["message"] = std_err
        task["status"] = "Failed"

    SignServiceClient.update_task_status(task)

    remove(downloaded_path)


def get_post_parser() -> RequestParser:
    post_parser: RequestParser = RequestParser()

    post_parser.add_argument("uuid", required=True, type=str, location="json")
    post_parser.add_argument("filepath", required=True, type=str, location="json")
    post_parser.add_argument("production", required=True, type=inputs.boolean, location="json")
    post_parser.add_argument("status", required=True, type=str, location="json")
    post_parser.add_argument("message", required=True, type=str, location="json")
    post_parser.add_argument("last_update", required=True, type=str, location="json")

    return post_parser


class SignNugetResource(Resource):
    post_parser: RequestParser = get_post_parser()

    @classmethod
    def post(cls):
        sign_service_task: dict[str, Any] = cls.post_parser.parse_args()

        thread: Thread = Thread(target=thread_signing, args=(sign_service_task,))
        thread.start()

        return sign_service_task, HTTPStatus.OK
