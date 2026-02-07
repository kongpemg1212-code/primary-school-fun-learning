from openai import OpenAI

client = OpenAI(
    api_key="sk-litellm-master-key-12345",
    base_url="http://localhost:4000/v1"
)

print("🔍 Connecting to Local LiteLLM Proxy...")
try:
    models = client.models.list()
    print(f"✅ Connection Success! Found {len(models.data)} models.")
    for m in models.data:
        print(f"   - {m.id}")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
