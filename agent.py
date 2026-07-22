import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": "Décris une sqli"
            }]
        )

print(message.content[0].text)
