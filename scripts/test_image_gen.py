from openai import OpenAI

client = OpenAI(
    api_key="sk-litellm-master-key-12345",
    base_url="http://localhost:4000/v1"
)

try:
    print("🎨 Testing Image Generation (DALL-E 3 via Proxy)...")
    response = client.images.generate(
        model="openrouter-gpt4o", # OpenRouter often routes 'dall-e-3' requests if model supports it
        prompt="A cute cartoon rabbit",
        n=1,
        size="256x256"
    )
    print(f"✅ Success! URL: {response.data[0].url}")
except Exception as e:
    print(f"❌ DALL-E Failed: {e}")

try:
    print("🎨 Testing Image Generation (Gemini via Proxy)...")
    # Some proxies map 'dall-e-3' to Imagen if configured
    response = client.images.generate(
        model="gemini-3-flash-preview", 
        prompt="A cute cartoon rabbit",
        n=1,
        size="256x256"
    )
    print(f"✅ Success! URL: {response.data[0].url}")
except Exception as e:
    print(f"❌ Gemini Failed: {e}")
