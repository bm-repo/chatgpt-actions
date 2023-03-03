# Automated Code Review using the ChatGPT language model

# Import statements
import openai
import os
import requests
import glob
import os

# Authenticating with the OpenAI API
openai.api_key = os.getenv('OPENAPI_KEY')
openai_engine = 'text-davinci-003'
openai_temperature = 1
openai_max_tokens = 4000


def generate_testcases():
    try:
        fl_list = glob.glob('python-files/*.py')
        print('file list ', fl_list)

        if not os.path.exists('test-genie'):
            os.makedirs('test-genie')

        for file in fl_list:
            with open(file) as f:
                content = f.read()
        		# Sending the code to ChatGPT
                response = openai.Completion.create(
                    engine=openai_engine,
                    prompt=(
                        f"Generate unit tests for following code:\n```{content}```"),
                    temperature=openai_temperature,
                    max_tokens=openai_max_tokens
                )
                filename = f.name.split("/")[1]
                
                print(f'test cases generated for "{filename}": \n',  {
                    response['choices'][0]['text']})
                    
                with open(f"test-genie/{filename}", "w") as ws:
                    ws.write(response['choices'][0]['text'])

                with open(f"test-genie/{filename}") as rs:
                    content = rs.read()
                    print(f"test cases read from the files \n, {content}")
    except Exception as ex:
        print('exception generated', ex.args)


generate_testcases()
