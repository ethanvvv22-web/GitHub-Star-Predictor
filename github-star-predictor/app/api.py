from flask import Flask, Blueprint, request, jsonify, render_template_string
from .rank import rank_repositories
import json
from .model.load_model import predict_stars
import os

app = Flask(__name__)

with open(os.path.join(os.path.dirname(__file__),'model/best_model_metadata.json'),'r') as f:
	metadata = json.load(f)

## UI
# HTML_TEMPLATE = f"""
# <!doctype html>
# <title>GitHub Star Predictor</title>
# <h1>GitHub Star Predictor</h1>
# <h2>Model: {metadata["model_name"]}<h2>
# <h2>R2 value: {metadata["r2_val"]}</h2>
# <form action="/predict" method="post">
# 	<h2>Predict Stars</h2>
# 	<label for="features">Features (JSON format):</label><br>
# 	<textarea name="features" rows="5" cols="50"></textarea><br>
# 	<input type="submit" value="Predict">
# </form>
#
# <form action="/rank" method="post">
# 	<h2>Rank Repositories</h2>
# 	<label for="repos">Repositories (JSON array format):</label><br>
# 	<textarea name="repos" rows="5" cols="50"></textarea><br>
# 	<input type="submit" value="Rank">
# </form>
# """
HTML_TEMPLATE =f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>GitHub Star Predictor</title>

<style>
body {{
    font-family: Arial;
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white;
}}

.container {{
    max-width: 700px;
    margin: 50px auto;
    padding: 30px;
    background: #ffffff10;
    border-radius: 12px;
}}

h1 {{
    text-align: center;
}}

.buttons {{
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}}

button {{
    flex: 1;
    padding: 10px;
    border: none;
    border-radius: 8px;
    background: #00c6ff;
    cursor: pointer;
}}

button.active {{
    background: #ffcc00;
}}

textarea {{
    width: 100%;
    padding: 10px;
    border-radius: 8px;
    border: none;
    margin-top: 10px;
}}

.result {{
    margin-top: 10px;
    padding: 10px;
    background: #00000030;
    border-radius: 8px;
}}
</style>

<script>
function showSection(section) {{
    document.getElementById("predict_section").style.display = "none";
    document.getElementById("rank_section").style.display = "none";

    document.getElementById(section).style.display = "block";
}}

async function predictStars() {{
    const input = document.getElementById("features").value;

    const res = await fetch("/predict", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: input
    }});

    const data = await res.json();
    document.getElementById("predict_result").innerText =
        "Predicted Stars: " + data.predicted_stars;
}}

async function rankRepos() {{
    const input = document.getElementById("repos").value;

    const res = await fetch("/rank", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: input
    }});

    const data = await res.json();
    document.getElementById("rank_result").innerText =
        JSON.stringify(data.ranked_repositories, null, 2);
}}
</script>

</head>

<body>

<div class="container">

<h1>GitHub Star Predictor</h1>
<p><b>Model:</b> {metadata["model_name"]}</p>
<p><b>R²:</b> {metadata["r2_val"]}</p>

<div class="buttons">
    <button onclick="showSection('predict_section')">Predict Stars</button>
    <button onclick="showSection('rank_section')">Rank Repositories</button>
</div>

<!-- Predict -->
<div id="predict_section">
    <h2>Predict Stars</h2>
    <textarea id="features" rows="6"></textarea>
    <button onclick="predictStars()">Predict</button>
    <div id="predict_result" class="result"></div>
</div>

<!-- Rank -->
<div id="rank_section" style="display:none;">
    <h2>Rank Repositories</h2>
    <textarea id="repos" rows="6"></textarea>
    <button onclick="rankRepos()">Rank</button>
    <div id="rank_result" class="result"></div>
</div>

</div>

</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
	return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
	try:
		import json
		if 'features' in request.form:
			data_str = request.form.get('features')
			data = json.loads(data_str)
		else:
			data = request.get_json(force=True)

		prediction = predict_stars(data)
		return jsonify({'predicted_stars': prediction})
	except Exception as e:
		return jsonify({'error': str(e)}),400

@app.route('/rank', methods=['POST'])
def rank():
	try:
		import json
		if 'repos' in request.form:
			data_str = request.form.get('repos')
			data = json.loads(data_str)
		else:
			data = request.get_json(force=True)

		ranked = rank_repositories(data)
		return jsonify({'ranked_repositories': ranked})
	except Exception as e:
		return jsonify({'error': str(e)}),400
