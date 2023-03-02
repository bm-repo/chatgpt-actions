#!/bin/sh -l
python -m venv venv & venv/bin/activate & python -m pip install --upgrade pip & pip install -r requirements.txt

python /main.py --openai_api_key "$1" --github_token "$2" --github_pr_id "$3" --openai_engine "$4" --openai_temperature "$5" --openai_max_tokens "$6" --mode "$7"
