from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from helper import Dashboard

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template("index.html")


@app.route("/dashboard")
def get_dashboard_data():
    search_string = request.args.get('q')

    if search_string is None:
        return jsonify({"status": 400, "message": "Search string is not given or empty"})
    
    dash = Dashboard(search_string)
    dash.get_dataset_from_moj()

    return render_template("dashboard.html", data= {
        "search_string": search_string,
        "total_posts": dash.dashboard_data["total_posts"],
        "top_accounts": dash.get_top_accounts_by_interactions(),
        "latest_posts": dash.get_latest_posts(),
        "top_tags": dash.get_top_tags_by_interactions(),
        "total_interactions": dash.dashboard_data["total_interactions"],
        "languages": {
            "labels": list(dash.dashboard_data["languages"].keys()),
            "datasets": [{
                "label": "Language used in Videos",
                "data": list(dash.dashboard_data["languages"].values()),
                "backgroundColor": dash.graph_colors,
            }]
        },
        "categories": {
            "labels": list(dash.dashboard_data["categories"].keys()),
            "datasets": [{
                "label": "Categories of Content",
                "data": list(dash.dashboard_data["categories"].values()),
                "backgroundColor": dash.graph_colors,
                "hoverOffset": 4
            }]
        }
    })