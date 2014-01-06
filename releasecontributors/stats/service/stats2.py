import json
import time
import datetime
import calendar

from functools import wraps
from flask import request, current_app
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.code import Code
from collections import defaultdict
from flask import Flask, jsonify
from flask import request

HOST = "" #TODO insert mongo address here
client = MongoClient(HOST)

app = Flask(__name__)


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function


@app.route('/getActivityForProduct')
@jsonp
def get_dates_for_product():

    data = request.args["product"] if "product" in request.args\
        else json.loads(request.data)["product"]

    map_str = Code(
        """
        function() {
            var id = this.extra.values.target_milestone;
            emit(id, {assignee: this.extra.assignee});
        }
        """
    )
    reduce_str = Code(
        """
        function (key, values) {
            var ret = {mails:[]};
            values.forEach(function (value) {
                if (value.assignee && ret.mails.indexOf(value.assignee) < 0)
                    ret.mails.push(value.assignee);
            });
            return ret;
        }
        """
    )
    query ={"source": "bugzilla", "extra.product": data,
            "extra.values.target_milestone": {"$exists": True},
            "extra.assignee": {"$exists": True}}
    collection = client.blackhole.contributions
    collection.ensure_index([("datetime", ASCENDING),
                             ("source", ASCENDING),
                             ("extra.product", ASCENDING)])
    result = []
    for d in sorted(collection.map_reduce(map_str, reduce_str,
                                          {'inline': 0},
                                          query=query)["results"]):
        if "mails" in d["value"]:
            print d
            d["value"] = len(d["value"]["mails"])
            result.append(d)
    return jsonify({"result": result})


@app.route('/getSources',  methods = ['GET'])
@jsonp
def get_sources():
    sources =\
        sorted([p for p in client.blackhole.contributions.find().\
                distinct("source")])
    return jsonify({"sources": sources})


@app.route('/getProducts',  methods = ['GET'])
@jsonp
def get_prodcuts():
    query_dict ={"source": "bugzilla"}
    products =\
        sorted([p for p in client.blackhole.contributions.find(query_dict).\
                distinct("extra.product")])
    return jsonify({"products": products})


if __name__ == '__main__':
    app.run(debug=True)
