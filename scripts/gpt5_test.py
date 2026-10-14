from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-6-astra",
    input="How much gold would it take to coat the Statue of Liberty in a 1mm layer?",
    reasoning={
        "effort": "low"
    }
)

print(response)
