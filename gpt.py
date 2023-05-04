import openai

history = [{"role": "system", "content": "You are a helpful assistant that gives concise answers."}]
max_history = 10

def append_history(message):
    if len(history) >= max_history:
        del history[1:3]

    history.append(message)


def conversate(prompt):
    message = {"role": "user", "content": prompt}
    append_history(message)
    r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=history)

    reply = r['choices'][0]['message']['content']
    tokens_used = r['usage']['total_tokens']

    return reply, tokens_used
