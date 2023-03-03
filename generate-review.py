# Automated Code Review using the ChatGPT language model

# Import statements
import openai
import os
import requests
import glob
import os
from github import Github

# Authenticating with the OpenAI API
openai.api_key = os.getenv('OPENAPI_KEY')
openai_engine = 'text-davinci-003'
openai_temperature = 0.5
openai_max_tokens = 2048

g = Github(os.getenv('GIT_TOKEN'))

def generate_review():
    try:
        repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
        pull_request = repo.get_pull(int(os.getenv('GIT_PR_ID')))
        
        ## Loop through the commits in the pull request
        commits = pull_request.get_commits()
        
        seen_files = set()
        for commit in commits:
            files = commit.files
            
            print('file list ', files)
            for file in files:
                filename = file.filename
                
                if filename in seen_files:
                    print(f'Review already generated for file {filename}')
                    continue

                if 'src' not in filename:
                    print(f'{filename} Skipping')
                    continue

                seen_files.add(filename)
                content = repo.get_contents(filename, ref=commit.sha).decoded_content
 
                # Sending the code to ChatGPT from here
                response = openai.Completion.create(
                    engine=openai_engine,
                    prompt=(
                        f"Review the following code in terms of best practices:\n```{content}```"),
                    temperature=openai_temperature,
                    max_tokens=openai_max_tokens
                )
    
                # Adding a comment to the pull request with ChatGPT's response
                print(response['choices'])
                review_comment = '\n\n'.join( [ x['text'] for x in response['choices'] ] )

                pull_request.create_issue_comment(f'<img src="https://raw.githubusercontent.com/allabakashb/SampleJSON/main/logo.png" width="100px"><div>You can improve the code quality by following suggestions for <b>{file.filename}</b>:{review_comment}</div>')

    except Exception as ex:
        print('exception generated', ex.args)

generate_review()
