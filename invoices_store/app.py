from flask import Flask
from flask import request, abort, jsonify, make_response
import json

from main.controller import InvoicesStore
from main.utils import get_mongodb_collection

app = Flask(__name__)
invoices_store = InvoicesStore(get_mongodb_collection())


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({"message": "api not found"}), 404)


@app.route("/")
def list_routes():
    """
    List available API endpoints.
    """
    import urllib

    output = []
    for rule in app.url_map.iter_rules():
        output.append({"rule": str(rule), "methods": str(rule.methods)})

    return make_response(jsonify(output), 200)


@app.route("/invoices", methods=["GET"])
def list_invoices():
    res = invoices_store.list_invoices()
    ret_code = res["ret_code"]
    del res["ret_code"]
    return make_response(jsonify(res["docs"]), ret_code)


@app.route("/invoice", methods=["POST"])
def create_invoices():
    docs = request.get_json()
    res = invoices_store.create_invoice(docs)
    return make_response(jsonify(res), res["ret_code"])


@app.route("/contact", methods=["UPDATE", "PATCH"])
def update_contact():
    doc = request.get_json()
    res = invoices_store.update_contact(doc)
    return make_response(jsonify(res), res["ret_code"])


@app.route("/search_contact", methods=["GET"])
def search_contact():
    request_dict = request.args.to_dict()
    print(request_dict)
    res = invoices_store.search_contact(request_dict)
    ret_code = res["ret_code"]
    del res["ret_code"]
    return make_response(jsonify(res["doc"]), ret_code)


if __name__ == "__main__":
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
    app.run(host="0.0.0.0", port=8080)
