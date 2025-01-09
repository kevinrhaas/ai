import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = "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"

restart_sequence = "\n"

response = openai.Completion.create(
#  engine="curie",
  model="davinci:ft-personal-2022-07-30-00-21-05", #$12.07 LDC 7.1
  # model="curie:ft-personal-2022-07-29-19-31-09", #$1.27 LDC 7.1
  #model="curie:ft-personal-2022-08-01-17-56-33", #$9.53 Pentaho 9.3 #variable batch
  prompt="How do you start installing LDC? ",
  temperature=0.77,
  max_tokens=140,
  top_p=0.9,
  frequency_penalty=.95,
  presence_penalty=.95,
  stop=["\n"]
)
print(response)
