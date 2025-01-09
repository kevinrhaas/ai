import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = "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"

response = openai.Answer.create(
    search_model="ada", 
    model="curie", 
    question="which puppy is happy?", 
    file="file-09CdGPgSgyPisTfdx1f7Qmx7", 
    examples_context="In 2017, U.S. life expectancy was 78.6 years.", 
    examples=[["What is human life expectancy in the United States?", "78 years."]], 
    max_rerank=5,
    max_tokens=10,
    stop=["\n", "<|endoftext|>"]
)

print(response)
