from openai import OpenAI

client = OpenAI(api_key=api_key)
import json
import sys
import os

# Replace with your OpenAI API key
api_key = "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"


def create_sales_play(sales_play_name, sales_play_summary,sales_play_sample):
    prompt = (f"""Create a completed Sales Play in bulleted form for each of the sections for the given Sales Play name and Sales Play summary.
                    These are Sales Plays for Hitachi Vantara's Pentaho Data Integration (PDI) product, Pentaho Business Analytics (PBA) product and Lumada Data Catalog product.
                    These sales plays may include a solution focus, where there will be 3rd party partners involved in the solution.
                    Provide detailed and creative ideas and include use cases and examples within each section to illustrate. 
                    Provide 5 unique creative analytical precise bullets in each section. Avoid generic answers. 
                    If an answer varies depending on the customer's specific needs and requirements or  depends on the size of the customer's data environment and the complexity of the solution,
                    provide an estimate based on industry averages and best practices.\n\n"""
              f"Sales Play Name: {sales_play_name}\n"
              f"Sales Play Summary: {sales_play_summary}\n\n"
              f"Please provide the following sections:\n"
              f"1. Description of the addressable and serviceable market by industry, personas (user, buyer)\n"
              f"2. The customer problem being solved?\n"
              f"3. What's business outcome does the customer need to achieve?\n"
              f"4. Why is the customer trying to solve this? What does success look like?\n"
              f"5. How else can the customer solve this problem?\n"
              f"6. How are competitors solving this for their customers?\n"
              f"7. Why are they unable to resolve this with the technology they have today?\n"
              f"8. What is our offering? Is it platform, technology capabilities, product or solution?\n"
              f"9. What is the solution design (or solution blueprint) into which our product fits?\n"
              f"10. What is the sales execution process from first contact to sale 'won' to implementation?\n"
              f"11. What are the expected business benefits?\n"
              f"12. What is our pricing? How does our pricing compare to our competitors?\n"
              f"13. What is our commercial model? XaaS? SaaS? Term based license?\n"
              f"14. What is the expected time to value?\n"
              f"15. What is the TCO for 1, 3, 5 years?\n"
              f"Use the following template as an example to complete the above 15 sections in the sales play:\n{sales_play_sample}\n"
              )

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are a sales play generator to assist sales teams to generate maximum revenue for their deals. You should provide detailed and specific creative ideas based on current market trends and compentitive assessment"},
    {"role": "user", "content": prompt},
    ],
    n=1,
    stop=None,
    temperature=0.7)

    generated_text = response.choices[0].message.content
    return generated_text


# open the sample-sales-play.txt file and read the contents
with open('sample-sales-play.txt', 'r') as myfile:
    sample_sales_play = myfile.read()


# take in a command line parameter named file
if len(sys.argv) == 3 and sys.argv[1] == "--file":
    # Read from file
    with open(sys.argv[2], 'r') as myfile:
        data = myfile.read()
        # check if the file is valid json
        try:
            json.loads(data)
        except ValueError as e:
            print("Invalid JSON file")
            sys.exit(1)

    # print(data)

    output_file_name = sys.argv[2] + ".out"
    # print(output_file_name)

    # try to delete the file if it exists
    if os.path.exists(output_file_name):
        os.remove(output_file_name)
    else:
        print("Creating output file: " + output_file_name )

    # create a file to write the output to
    output_file = open(output_file_name, "w")

    # parse file and loop through json array
    json_data = json.loads(data)

    for play in json_data['plays']:
        result = create_sales_play(play["name"], play["summary"], sample_sales_play)
        print("Generated Sales Play: " + play["name"] + "\n")
        print(result)
        print ("\n\n\n")
        # write to output file
        output_file.write("Generated Sales Play: " + play["name"] +"\n")
        output_file.write("Sales Play Summary Prompt: " + play["summary"] +"\n")
        output_file.write(result)
        output_file.write("\n\n\n")

    output_file.close()
    sys.exit(1)

if len(sys.argv) == 3 and sys.argv[0] != "--file":
    print("Optional Command Usage: python generate_sales_play.py <Sales Play Name> <Sales Play Summary>")
    sales_play_name = input("Enter Sales Play Name: ")
    sales_play_summary = input("Enter Sales Play Summary: ")
    result = create_sales_play(sales_play_name, sales_play_summary, sample_sales_play)
    print ("\n\n\n")
    print("\nGenerated Sales Play: " + sales_play_name)
    print(result)
    sys.exit(1)
else:
    sales_play_name = sys.argv[1]
    sales_play_summary = sys.argv[2]
    result = create_sales_play(sales_play_name, sales_play_summary, sample_sales_play)
    print ("\n\n\n")
    print("\nGenerated Sales Play: " + sales_play_name)
    print(result)
    sys.exit(1)