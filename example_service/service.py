from nameko.rpc import rpc


class TestService:
    name = "test_service"

    @rpc
    def ping(self):
        return "pong"

    @rpc
    def printer(self, word: str):
        return f"hello, {word}"

    @rpc
    def multi_params_rpc(self, param_1, param_2, param_3, param_4):
        return f"hi {param_1}, {param_2}, {param_3}, {param_4}!"
