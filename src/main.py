from decouple import config
from flask import Flask, render_template, request, redirect, url_for
from nameko.standalone.rpc import ClusterRpcProxy
import service_inspector


app = Flask(__name__)

AMQP_URI = config("AMQP_URI", default="pyamqp://guest:guest@broker")
NAMEKO_CONFIG = {"AMQP_URI": AMQP_URI}

nameko_service_data = service_inspector.inspect_file("./service.py")


@app.route("/")
def index():
    service_name = nameko_service_data['service_name']
    methods = nameko_service_data['methods']
    return render_template(
        "index.html",
        methods=methods,
        service_name=service_name
    )

@app.route("/call_rpc/<service_name>", methods=["POST"])
def call_rpc(service_name):
    data = request.form.copy()
    method_name = data.pop("method")
    method_params = {}
    for i in data:
        # Remove prefix from param name
        prefix = f"{method_name}_"
        param_name = i.replace(prefix, '')
        method_params.update({param_name: data[i]})

    with ClusterRpcProxy(NAMEKO_CONFIG) as cluster_rpc:
        method = getattr(cluster_rpc[service_name], method_name)
        response = method(**method_params)
        print(response)

    return redirect(url_for("index"))
