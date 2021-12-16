from flask import Flask, render_template, request
from nameko.standalone.rpc import ClusterRpcProxy


app = Flask(__name__)

NAMEKO_CONFIG = {"AMQP_URI": "pyamqp://guest:guest@localhost"}

@app.route("/")
def index():
    # Mocked methods just for tests
    service_name = "Service Test"
    methods = [
        {"name": "method01", "params": []},
        {"name": "method02", "params": ["param_a"]},
        {"name": "method03", "params": ["param_a", "param_b"]},
    ]
    return render_template(
        "index.html",
        methods=methods,
        service_name=service_name
    )

@app.route("/call_rpc/<service_name>", methods=["POST"])
def call_rpc(service_name):
    data = request.get_json()
    method_name = data["method"]
    method_params = data["params"]
    with ClusterRpcProxy(NAMEKO_CONFIG) as cluster_rpc:
        method = getattr(cluster_rpc[service_name], method_name)
        response = method(**method_params)
        print(response)
    return "hello"
