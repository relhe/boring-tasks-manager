########################################################################################################################
# Document Processing Class                                                                                            #
#                                                                                                                      #
# This class processes a Word document specified in the `file_path` and extracts categorized activities into a JSON    #
# file.                                                                                                                #
#                                                                                                                      #
# Author: Renel Lherisson                                                                                              #
# Date: 2024-12-27                                                                                                     #
# Purpose: Automate the extraction and categorization of activities from a Word document into JSON format.             #
# Dependencies:                                                                                                        #
#    - python-docx: `pip install python-docx`                                                                          #
########################################################################################################################

from docx import Document
import json


class DocumentProcessor:
    def __init__(self, file_path, output_file_path):
        self.file_path = file_path
        self.output_file_path = output_file_path
        self.activities = {
            "Learning": [],
            "Reading": [],
            "Writing": [],
            "Job Applications": [],
            "Interview Prep": [],
            "Travel/Visit": []
        }

    def process_document(self):
        # Load the Word document
        document = Document(self.file_path)

        # Extract text and categorize into the dictionary
        for paragraph in document.paragraphs:
            text = paragraph.text.strip()
            if text.startswith("Learning:"):
                self.activities["Learning"].append(
                    text.replace("Learning:", "").strip())
            elif text.startswith("Reading:"):
                self.activities["Reading"].append(
                    text.replace("Reading:", "").strip())
            elif text.startswith("Writing:"):
                self.activities["Writing"].append(
                    text.replace("Writing:", "").strip())
            elif text.startswith("Job Applications:"):
                self.activities["Job Applications"].append(
                    text.replace("Job Applications:", "").strip())
            elif text.startswith("Interview Prep:"):
                self.activities["Interview Prep"].append(
                    text.replace("Interview Prep:", "").strip())
            elif text.startswith("Travel/Visit:"):
                self.activities["Travel/Visit"].append(
                    text.replace("Travel/Visit:", "").strip())

    def save_to_json(self):
        # Convert the dictionary to JSON
        output_json = json.dumps(self.activities, indent=4)

        # Save JSON to a file
        with open(self.output_file_path, 'w') as json_file:
            json_file.write(output_json)

    def run(self):
        self.process_document()
        self.save_to_json()
        return self.output_file_path


# Example usage
if __name__ == "__main__":
    file_path = './data/52.docx'
    output_file_path = './data/activities.json'

    processor = DocumentProcessor(file_path, output_file_path)
    result_path = processor.run()
    print(f"Activities JSON saved to: {result_path}")
