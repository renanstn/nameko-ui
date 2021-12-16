from nameko.rpc import rpc


class Test:
    name = "test"


class TestService:
    name = "test_service"

    @rpc
    def ping(self):
        return "pong"

    @rpc
    def printer(self, word: str):
        return f"hello, {word}"
