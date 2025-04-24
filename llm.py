from openai import OpenAI
from mistralai import Mistral
from typing import Dict
import dotenv
import os

dotenv.load_dotenv()


def llm_call_deepseek(prompt):
    print("backend used deepseek")
    client = OpenAI(
        api_key=os.environ["DEEP_SEEK"], base_url="https://api.deepseek.com"
    )
    response = client.chat.completions.create(
        model='deepseek-reasoner',#"deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "You are an expert tutor specialized in Math and Science evaluating tutoring interactions.",
            },
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )
    return response.choices[0].message.content


def llm_call_openai(prompt, model="gpt-4o"):
    print(f"backend used openai - {model}")
    client = OpenAI()

    completion = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You are an expert tutor specialized in Math, and you are evaluating tutoring interactions.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content


def llm_call_mistral(prompt, model='ministral-8b-latest'):

    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    print(f"backend used mistral - {model}")
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "system",
                "content": "You are an expert tutor specialized in Math and Science evaluating tutoring interactions.",
            },
            {"role": "user", "content": prompt},
        ]
    )
    print('--> returning response')
    return chat_response.choices[0].message.content

def llm_call_llama(prompt, model="meta-llama/Meta-Llama-3.1-70B-Instruct"):
    openai = OpenAI(
    api_key=os.environ["DEEP_INFRA"],
    base_url="https://api.deepinfra.com/v1/openai",
    )
    print(f"backend used llama - {model}")
    chat_completion = openai.chat.completions.create(
        model='meta-llama/Meta-Llama-3.1-70B-Instruct',#"meta-llama/Meta-Llama-3.1-8B-Instruct",#
        messages=[
            {
                "role": "system",
                "content": "You are an expert tutor specialized in Math and Science evaluating tutoring interactions.",
            },
            {"role": "user", "content": prompt},
        ],
    stream=False,
    )
    return chat_completion.choices[0].message.content




def llm_call(prompt, backend="openai", model="gpt-4o-mini"):
    if backend == "openai":
        return llm_call_openai(prompt, "gpt-4o")
    elif backend == "deepseek":
        return llm_call_deepseek(prompt)
    elif backend == "mistral":
        return llm_call_mistral(prompt)
    elif backend == "llama":
        return llm_call_llama(prompt)
    else:
        raise ValueError(f"Invalid backend - {backend}. Supported backends are: openai, deepseek, mistral, llama.")
