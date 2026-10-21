from flask import Flask, render_template_string
app = Flask(__name__)
PAGE = '''
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Student Task Tracker</title><style>
body{font-family:Arial;max-width:760px;margin:40px auto;padding:0 18px;background:#f4f6fb;color:#202638}
header,.task{background:white;padding:22px;border-radius:14px;margin-bottom:14px;box-shadow:0 4px 16px #17255412}
h1{color:#2546a8}.tag{display:inline-block;padding:5px 10px;border-radius:20px;background:#e5edff}
.done{background:#e3f8e9}footer{color:#5c6478;font-size:14px;margin-top:24px}</style></head><body>
<header><h1>Student Task Tracker</h1><p>A demo app for the CCA 2 CI/CD pipeline.</p><p><strong>Release:</strong> {{ release }}</p></header>
{% for task in tasks %}<section class="task"><h3>{{ task.title }}</h3><p>{{ task.description }}</p>
<span class="tag {{ 'done' if task.status == 'Completed' else '' }}">{{ task.status }}</span></section>{% endfor %}
<footer>Deployed with Jenkins, Docker and Kubernetes.</footer></body></html>'''
@app.get("/")
def home():
    tasks = [
        {"title":"Complete CCA 2","description":"Build and verify the CI/CD pipeline.","status":"In progress"},
        {"title":"Prepare viva notes","description":"Understand each pipeline stage.","status":"Pending"},
        {"title":"Push a new release","description":"Change the release label and run Jenkins again.","status":"Completed"},
    ]
    return render_template_string(PAGE, tasks=tasks, release="v2")
@app.get("/health")
def health():
    return {"status":"ok"}, 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
