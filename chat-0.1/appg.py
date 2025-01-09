import openai
import gradio as gr

openai.api_key = "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"

# read text from file and assign to variable
with open('input.txt', 'r') as myfile:
    data=myfile.read()

# add text to the beginning of the data variable
data = "You are a expert career advisor for Lee Haas. Give her help with anything related to your career, including job counseling, resume writing, interview preparation, and job search. Keep answers very focused on her experience. This is her resume: " + data


messages = [
    {"role": "system", "content": data},
]

def chatbot(input):
    if input:
        messages.append({"role": "user", "content": input})
        #debug print the length of the messages array
        print(len(messages))

        #if the messages array is greater than 12, remove the second message (keep the first message with resume)
        if len(messages) > 12:
            messages.pop(1)

        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply

inputs = gr.inputs.Textbox(lines=7, label="What would you like help with?")
outputs = gr.outputs.Textbox(label="Reply")

gr.Interface(fn=chatbot, inputs=inputs, outputs=outputs, title="Lee Haas's Career Advisor",
             description="I am a expert career advisor for Lee Haas, trained on her Linked In Resume. I can help her with anything related to her career, including job counseling, resume writing, interview preparation, and job search. Try things like:\n > Give me some fun job ideas based on my experience.\n > What Chicago companies should I look for jobs at?\n > What are jobs can I make the most money with my skills?",
             theme="compact").launch(share=True)

