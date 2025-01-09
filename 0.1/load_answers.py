
def load_answers():
	import os
	import openai

	openai.api_key = os.getenv("OPENAI_API_KEY")

	openai.api_key = "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"

	response = openai.File.create(file=open("answers.jsonl"), purpose='answers')


	return response.id



print(load_answers())
