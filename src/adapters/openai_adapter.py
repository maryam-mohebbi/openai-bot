import openai

OPENAI_API_KEY = ''


def setup(api_key):
    global OPENAI_API_KEY
    OPENAI_API_KEY = api_key
    openai.api_key = OPENAI_API_KEY


def generate_response(prompt, last_5_conversations):
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': 'I need your help. I want to ask from you. Your answer should be simple but complete'},
                {'role': 'assistant', 'content': 'Sure, I will help you in my best'},
                ]

    for convo in last_5_conversations:
        # Use 'TEXT' instead of 'U_MESSAGES.TEXT'
        user_message = {'role': 'user', 'content': convo['TEXT']}
        # Use 'ASSISTANT_TEXT' instead of 'A_MESSAGES.TEXT'
        assistant_message = {'role': 'assistant',
                             'content': convo['ASSISTANT_TEXT']}
        messages.extend([user_message, assistant_message])

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
