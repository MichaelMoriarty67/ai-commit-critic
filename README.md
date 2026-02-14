<div style="display: flex; justify-content: center; gap: 20px">
    <svg style="margin-top: 10px" width="55px" height="50px" viewBox="0 0 32 23" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7.57889 0C3.39319 0 0 3.30987 0 7.3928C0 11.4757 3.39319 14.7856 7.57889 14.7856H15.9999C16.465 14.7856 16.842 15.1534 16.842 15.607C16.842 16.0607 16.465 16.4284 15.9999 16.4284H0.58947C0.263915 16.4284 0 16.6859 0 17.0034V22.4248C0 22.7424 0.263915 22.9998 0.58947 22.9998H15.9999C20.1856 22.9998 23.5788 19.6899 23.5788 15.607C23.5788 11.5241 20.1856 8.21422 15.9999 8.21422H7.57889C7.11382 8.21422 6.73679 7.84646 6.73679 7.3928C6.73679 6.93914 7.11382 6.57138 7.57889 6.57138H21.8588C21.8708 6.5715 21.8828 6.57156 21.8948 6.57156H24.4211C24.8862 6.57156 25.2632 6.93932 25.2632 7.39298V22.425C25.2632 22.7426 25.5271 23 25.8527 23H31.4105C31.7361 23 32 22.7426 32 22.425V7.39298C32 3.31005 28.6068 0.000184234 24.4211 0.000184234H23.5788L7.57889 0Z" fill="white"/>
    </svg>
    <span style="font-size: 45px; font-weight: 800; font-style: italic; color: white">AI COMMIT CRITIC.<span>
</div> 
<div style="display: flex; justify-content: center; gap: 4px">This project was made for the <a href="https://steel.dev/">Steel Browser</a> team!</div>

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