
import json
import requests


MISTRAL_API_KEY = "yTtuo7hslGaUFBgRljI5w9LqiGi32Kb1"  # Secure with env variable in production
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-medium"  # or mistral-small, mistral-tiny

def generate_script_from_mistral(prompt):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt_str = (
    f"You are simulating a podcast between two fictional hosts: Alex (analytical) and Sam (humorous and curious). "
    f"The topic of the podcast is: {prompt}. "
    "Alex is referred to as 'Host' and Sam is referred to as 'Guest'. "
    "Begin with a brief introduction of the podcast, including short backgrounds of both hosts. "
    "Then have them engage in a natural, insightful back-and-forth conversation about the topic. "
    "End with a brief outro.\n\n"

    "Output must be in this exact JSON format:\n"
    '[{"speaker": "Host", "text": "..."}, {"speaker": "Guest", "text": "..."}, ...]\n\n'

    "Rules:\n"
    "- Use only the speaker labels 'Host' and 'Guest'.\n"
    "- Each message must be a single paragraph (no line breaks, no markdown, no special characters).\n"
    "- Do not add explanations, comments, or formatting outside the JSON array.\n"
    "- Do not include markdown, newlines (\\n), or a preamble.\n\n"

    "Return only the JSON array as plain text."
)


    data = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "user", "content": prompt_str}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }

    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    content = result["choices"][0]["message"]["content"]

    # Example assumption: response is a JSON-like script (you can adapt parsing)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # fallback: simple line split, assuming format: "Speaker: text"
        lines = content.strip().split("\n")
        return [
            {"speaker": line.split(":")[0].strip(), "text": ":".join(line.split(":")[1:]).strip()}
            for line in lines if ":" in line
        ]
