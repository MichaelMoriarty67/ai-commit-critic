# 🤖 AI COMMIT CRITIC 🤖
This project was made for the [Steel Browser](https://steel.dev/) team!

## Setup
1. Clone this repo (duh!)
2. Make sure python is installed (double duh!)
3. Install dependencies in `requirements.txt` using some packing installer (e.g. `pip install -r requirements.txt`)
4. Copy `.env.example` to a `.env` file and add your OpenAI API key.

## Using the package (cmd line flags)
1. `--analyze`: run git commit message analysis for selected repo. Defaults to last 3 commits of git repo in the root of the directory you run the python interpreter from.</br>
<span style="margin-left: 2em; font-style: italic;">Optionally:</span></br>
<span style="margin-left: 2em;">`--n=`: select a number of commits to analyze</span><br>
<span style="margin-left: 2em;"> `--url=`: specify a remote repo to analyze</span><br>
2. `--write`: write a git commit message for the current set of staged changes.