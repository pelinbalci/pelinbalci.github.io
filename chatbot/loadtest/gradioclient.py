from gradio_client import Client

print("One request")

client = Client("pelinbalci/pelin-notes-chat")
print(client.view_api())

result = client.predict(
    "Explain neural networks",
    api_name="/chat"
)
print(result)
