import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

openai.api_key = "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"

with open('input.txt', 'r') as myfile:
    data = myfile.read()

data = "You are a expert career advisor for Lee Haas. Give her help with anything related to your career, including job counseling, resume writing, interview preparation, and job search. Keep answers very focused on her experience. This is her resume: " + data

messages = [
    {"role": "system", "content": data},
]

@app.route('/chat', methods=['POST'])
def chatbot():
    input = request.json['input']
    if input:
        messages.append({"role": "user", "content": input})

        if len(messages) > 12:
            messages.pop(1)

        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
