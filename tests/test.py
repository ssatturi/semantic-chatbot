import openai

# Paste your real key here or use environment variable
openai.api_key = "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"
def test_embedding():
    try:
        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=["Test OpenAI key"]
        )
        embedding = response.data[0].embedding
        print("✅ Success! Received embedding of length:", len(embedding))
    except openai.APIError as e:
        print("❌ API error:", e)
    except openai.AuthenticationError as e:
        print("❌ Authentication error: Invalid API key")
    except Exception as e:
        print("❌ General error:", e)

if __name__ == "__main__":
    test_embedding()
