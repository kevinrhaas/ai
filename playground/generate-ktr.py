from openai import OpenAI

client = OpenAI(api_key=api_key)
import json
import sys

# Replace with your OpenAI API key
api_key = "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"


def create_transformation(trans_description):
    prompt = (f"Create a Pentaho Transformation based on the following description.\n\n"
              f"Pentaho Kettle Transformation Description: {trans_description}\n")

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are a Pentaho Data Integration Kettle KTR Transformation Generator. Only respond with valid XML of a KTR file. Include connections, steps and hops connecting the steps. for the Pentaho Data Integration Kettle tool."},
    {"role": "user", "content": prompt},
    ],
    n=1,
    stop=None,
    temperature=0.7)

    generated_text = response.choices[0].message.content
    return generated_text

if len(sys.argv) != 2:
    print("Optional Command Usage: python generate_ktr.py <Transformation Description>")
    trans_description = input("Enter Transformation Description: ")
else:
    trans_description = sys.argv[1]

result = create_transformation(trans_description)
print("\nGenerated Transformation:")
print(result)