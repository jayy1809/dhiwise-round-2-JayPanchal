from groq import Groq

from app.config import GROQ_API_KEY

groq_client = Groq(api_key=GROQ_API_KEY)


def get_chat_completion(
    user_prompt,
    system_prompt,
    model="llama3-8b-8192",
    temperature=0,
    max_tokens=1024,
    stream=False,
):
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
        )

        return chat_completion.choices[0].message.content

    except AttributeError as e:
        error_message = f"Error accessing completion message content: {str(e)}"
        raise AttributeError(error_message) from e

    except Exception as e:
        error_message = (
            f"An error occurred while creating the chat completion: {str(e)}"
        )
        raise RuntimeError(error_message) from e
