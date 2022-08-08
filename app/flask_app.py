from flask import Flask, request
import git

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        info=request.get_json()
        repo = git.Repo("./lfyawebsite")
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated successfull', 200
    else:
        return '', 400
