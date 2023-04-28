from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_folder="build/static", template_folder="build")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results/<job_id>")
def results(job_id):
    return render_template("index.html")


@app.route("/predict")
def predict():
    return redirect("/results/" + str(hash(request.args["q"])))


if __name__ == "__main__":
    app.run(port=5000)
