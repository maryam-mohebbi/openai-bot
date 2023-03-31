import openai

OPENAI_API_KEY = ''


def setup(api_key):
    global OPENAI_API_KEY
    OPENAI_API_KEY = api_key
    openai.api_key = OPENAI_API_KEY


def generate_response(prompt, previous_messages):
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': 'I need your help. I want to ask from you. Your answer should be simple but complete'},
                {'role': 'assistant', 'content': 'Sure, I will help you in my best'},
                ]
    for i, convo in enumerate(previous_messages):
        role = 'user' if i % 2 == 0 else 'assistant'
        message = {'role': role, 'content': convo['TEXT']}
        messages.append(message)

    messages.append({'role': 'user', 'content': prompt})

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        max_tokens=1024,
        n=1,
        temperature=1,
    )

    content = response.choices[0].message.content
    completion_tokens = response.usage.completion_tokens
    prompt_tokens = response.usage.prompt_tokens

    return {'content': content, 'tokens': {'completion_tokens': completion_tokens, 'prompt_tokens': prompt_tokens}}
