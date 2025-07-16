import openai
import sys

OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'  # Replace with your OpenAI API key
openai.api_key = OPENAI_API_KEY

def summarize_text(text, max_tokens=128):
    """
    Summarize the given text using OpenAI GPT-3/4 API.
    Args:
        text (str): Text to summarize.
        max_tokens (int): Max tokens for summary.
    Returns:
        str: Summary text or error message.
    """
    try:
        ChatCompletion = getattr(openai, 'ChatCompletion', None)
        if ChatCompletion:
            response = ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Summarize the following financial text for an investor."},
                          {"role": "user", "content": text}],
                max_tokens=max_tokens,
                temperature=0.5
            )
            return response.choices[0].message['content'].strip()
        else:
            Completion = getattr(openai, 'Completion', None)
            if Completion:
                prompt = f"Summarize the following financial text for an investor:\n{text}"
                response = Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=0.5
                )
                return response.choices[0].text.strip()
            else:
                return "OpenAI API does not support completion methods."
    except Exception as e:
        return f"Error: {e}" 