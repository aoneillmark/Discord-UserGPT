import json
import os

def smart_concatenate(existing_text, new_text):
    if not new_text:
        return existing_text
    if not existing_text:
        return new_text
    if existing_text[-1] not in ".!?":
        if new_text[0] not in ".!?,;: ":
            return existing_text + ". " + new_text
    return existing_text + " " + new_text


def create_prompt_response_pairs(messages, user1_id, user2_id):
    pairs = []
    current_prompt = ""
    current_response = ""
    awaiting_response = False

    for message in messages:
        author_id = message['author']['id']
        text = message['content'].strip()

        if author_id == user1_id:
            if awaiting_response and current_response:
                pairs.append((current_prompt, current_response))
                current_prompt = text
                current_response = ""
                awaiting_response = False
            else:
                current_prompt = smart_concatenate(current_prompt, text)
            awaiting_response = True
        elif author_id == user2_id and awaiting_response:
            current_response = smart_concatenate(current_response, text)

    if current_prompt and current_response:
        pairs.append((current_prompt, current_response))

    return pairs


def write_data(output_file_path, data_directory, user1_id, user2_id):
    # Open the output file once and write all prompt-response pairs
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Iterate over every file in the data directory
        for filename in os.listdir(data_directory):
            if filename.endswith('.json'):
                file_path = os.path.join(data_directory, filename)
                # Load and process each JSON file
                with open(file_path, 'r', encoding='utf-8') as file:
                    messages = json.load(file)
                    prompt_response_pairs = create_prompt_response_pairs(messages, user1_id, user2_id)
                    # Write the pairs to the output file
                    for prompt, response in prompt_response_pairs:
                        output_file.write("[PROMPT] " + prompt + " [RESPONSE] " + response + "\n")

    print(f"All files processed. Output saved to {output_file_path}")

####################################################


# Path to the directory containing JSON files
data_directory = 'Data/'
output_file_path = 'Results/processed_data/combined_output.txt'

# Enter the user IDs of the two users whose messages you want to process
user1_id = '123456789123456789'
user2_id = '987654321987654321'


write_data(output_file_path, data_directory, user1_id, user2_id)





