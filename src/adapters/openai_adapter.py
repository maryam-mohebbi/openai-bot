import openai

OPENAI_API_KEY = ''


def setup(api_key):
    global OPENAI_API_KEY
    OPENAI_API_KEY = api_key
    openai.api_key = OPENAI_API_KEY


def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=1024,
        n=1,
        temperature=1,
    )
    content = response.choices[0].message.content
    completion_tokens = response.usage.completion_tokens
    prompt_tokens = response.usage.prompt_tokens

    return {'content': content, 'tokens': {'completion_tokens': completion_tokens, 'prompt_tokens': prompt_tokens}}
