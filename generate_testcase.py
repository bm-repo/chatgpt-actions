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

def generate_testcases():
    try:
        repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
        pull_request = repo.get_pull(int(os.getenv('GIT_PR_ID')))
        
        if not os.path.exists('test-genie'):
            os.makedirs('test-genie')
 
        ## Loop through the commits in the pull request
        commits = pull_request.get_commits()
        
        seen_files = set()
        for commit in commits:
            files = commit.files
            
            print('file list ', files)
            for file in files:
                filename = file.filename
                
                if filename in seen_files:
                    print(f'Unit tests already generated for file {filename}')
                    continue

                if 'src' not in filename:
                    print(f'{filename } Skipping ')
                    continue

                seen_files.add(filename)
                content = repo.get_contents(filename, ref=commit.sha).decoded_content
 
                # Sending the code to ChatGPT from here
                response = openai.Completion.create(
                    engine=openai_engine,
                    prompt=(
                        f"Generate unit tests for following code:\n```{content}```"),
                    temperature=openai_temperature,
                    max_tokens=openai_max_tokens
                )
                
                print(f'test cases generated for "{filename}": \n',  {
                    response['choices'][0]['text']})
                
                test_file_name = 'test_' + filename.split('/')[-1]
                with open(f"test-genie/{test_file_name}", "w") as ws:
                    ws.write(response['choices'][0]['text'])

                with open(f"test-genie/{test_file_name}") as rs:
                    content = rs.read()
                    print(f"test cases read from the files \n, {content}")
    except Exception as ex:
        print('exception generated', ex.args)


generate_testcases()
