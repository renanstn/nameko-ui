from decouple import config
from flask import Flask, render_template, request, redirect, url_for, session
from nameko.standalone.rpc import ClusterRpcProxy
import service_inspector


app = Flask(__name__)
app.secret_key = config("SECRET_KEY", default="secret")

AMQP_URI = config("AMQP_URI", default="pyamqp://guest:guest@broker")
NAMEKO_CONFIG = {"AMQP_URI": AMQP_URI}


@app.route("/")
def select_service():
    return render_template(
        "select_service.html",
        service_name="Upload service file",
    )

@app.route("/file_upload/", methods=["POST"])
def file_upload():
    file = request.files["service_file"]
    file_in_bytes = file.read()
    file_content = file_in_bytes.decode("UTF-8")
    nameko_service_data = service_inspector.inspect_content(file_content)

    session["service_name"] = request.form["service-name"]
    session["methods"] = nameko_service_data['methods']

    return redirect(url_for("rpcs"))

@app.route("/rpcs")
def rpcs():
    methods = session["methods"]
    service_name = session["service_name"]

    return render_template(
        "rpcs.html",
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

    return redirect(url_for("rpcs"))
