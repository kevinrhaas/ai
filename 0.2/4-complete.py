import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = "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"

restart_sequence = "\n"

import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument('--prompt', help='Prompt to start with')
parser.add_argument('--model', help='Name of the model to use, default is curie')

args=parser.parse_args()

if not args.prompt:
    print("Please provide a prompt with --prompt")
    sys.exit(1)   

prompt_input = args.prompt

model_name = "curie:ft-personal-2023-01-13-20-57-00"

if not args.model:
    print("Using default model: " + model_name)
else:
    if args.model == "curie":
        model_name = "curie:ft-personal-2023-01-13-20-57-00"
    elif args.model == "davinci":
        model_name = "davinci:ft-personal-2023-01-14-16-54-48"    
    print("Using model: " + model_name)


response = openai.Completion.create(
#  engine="curie",
  # model="davinci:ft-personal-2022-07-30-00-21-05", #$12.07 LDC 7.1
  # model="curie:ft-personal-2022-07-29-19-31-09", #$1.27 LDC 7.1
  # model="curie:ft-personal-2022-08-01-17-56-33", #$9.53 Pentaho 9.3 #variable batch
  # model="curie:ft-personal-2023-01-13-20-57-00", # Fine-tune costs $1.08 LDC 73 Doc
  model=model_name, # Fine-tune costs $10.82 LDC 73 Doc
  prompt=prompt_input,
  temperature=0,
  max_tokens=140,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(response)