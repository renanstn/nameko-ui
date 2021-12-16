from flask import Flask, render_template


app = Flask(__name__)

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

@app.route("/call_rpc")
def call_rpc():
    pass
