from abc import abstractmethod
import base64

from .utils import krunner_response


class KRunnerHandler:
    @classmethod
    @abstractmethod
    def match(cls, query: str):
        ...

    # @classmethod
    # @abstractmethod
    # def run(cls, query: str):
    #     ...

    @staticmethod
    def forward(query: str):
        response = []
        for handler in KRunnerHandler.__subclasses__():
            # res -> bool, func
            if (res := handler.match(query)) is not False:
                response.append(res)
        return response


class Base64(KRunnerHandler):
    @classmethod
    def match(cls, query: str):
        if query.startswith("b64d "):
            return cls.base64decode(query[5:])

        elif query.startswith("b64e "):
            return cls.base64encode(query[5:])

        return False

    @classmethod
    def base64decode(cls, data: str):
        res = base64.b64decode(data).decode()
        return krunner_response(res, f'"{res}"')

    @classmethod
    def base64encode(cls, data: str):
        res = base64.b64encode(data.encode()).decode()
        return krunner_response(res, f'"{res}"')
