import subprocess
from flask import Flask, render_template, request
from tempfile import SpooledTemporaryFile as tempfile

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/compile", methods=['GET', 'POST'])
def test():
    language = request.form.get("language")
    script = request.form.get("examples")
    inputs = request.form.get("inputs")
    if script == "first":
        script = "dance_with_Lu.lua"
    elif script == "second":
        script = "IIblx.php"
    elif script == "third":
        script = "Flag.py"
    elif script == "fourth":
        script = "funny_ascii.py"
    else:
        return render_template("wtf.html")

    if language.startswith("php"):
        f = tempfile()
        f.write(inputs.encode() + b"\n")
        f.seek(0)
        proc = subprocess.Popen("php static/scripts/" + script, shell=True, stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE, stdin=f)
        script_response = proc.stdout.read().decode() + proc.stderr.read().decode()
        f.close()
    elif language.startswith("lua"):
        proc = subprocess.Popen("lua5.3 static/scripts/" + script, shell=True, stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        script_response = proc.stdout.read().decode() + proc.stderr.read().decode()
    elif language.startswith("python"):
        splited = language.split("n")
        version = splited[1]
        if script == "Flag.py":
            if float(version) < 3:
                return "Intruder!!!"
            else:
                f = tempfile()
                f.write(inputs.encode() + b"\n")
                f.seek(0)
                proc = subprocess.Popen("python{} static/scripts/{}".format(version[0], script), shell=True,
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stdin=f)
                script_response = proc.stdout.read().decode() + proc.stderr.read().decode()
                f.close()
                return str(script_response)

        f = tempfile()
        f.write(inputs.encode() + b"\n")
        f.seek(0)
        proc = subprocess.Popen("python{} static/scripts/{}".format(version[0], script), shell=True,
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE, stdin=f)
        script_response = proc.stdout.read().decode() + proc.stderr.read().decode()
        f.close()
    else:
        return render_template("wtf.html")
    return str(script_response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
