import requests
OLLAMA_URL = "http://localhost:11434/api/generate"
def call(prompt, model="mistral", temperature=0.2, timeout=60):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            },
            timeout=timeout
        )

        response.raise_for_status()

        data = response.json()

        if "response" not in data:
            return "Error: Invalid response from LLM"

        return data["response"].strip()

    except requests.exceptions.Timeout:
        return "Error: Request timed out"

    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama. Is it running?"

    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP {e.response.status_code if e.response else 'Unknown'}"

    except Exception as e:
        return f"Error: {str(e)}"