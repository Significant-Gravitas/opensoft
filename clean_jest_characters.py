import json
import re

def strip_ansi_escape_sequences(input_string):
    # Match the string's representation of the escape sequence
    return re.sub(r'\\u001b\[[0-9;]*[a-zA-Z]', '', input_string)

report_path = 'report.json'
with open(report_path, 'r', encoding='utf-8') as file:
    content = file.read()

cleaned_content = strip_ansi_escape_sequences(content)

with open(report_path, 'w', encoding='utf-8') as file:
    file.write(cleaned_content)
# Load JSON data
parsed_data = json.loads(cleaned_content)

# Extract details of the first failed test
first_failed_test = None
for test_result in parsed_data["testResults"]:
    if test_result["status"] == "failed":
        for assertion in test_result["assertionResults"]:
            if assertion["status"] == "failed":
                first_failed_test = {
                    "Component": assertion["ancestorTitles"][0] if assertion["ancestorTitles"] else "",
                    "Test Title": assertion["title"],
                    "Failure Reason": "\n".join(assertion["failureMessages"])
                }
                break
        if first_failed_test:
            break

# Display the details of the first failed test
if first_failed_test:
    result_string = f"Component: {first_failed_test['Component']}\n" \
                    f"Test Title: {first_failed_test['Test Title']}\n" \
                    f"Failure Reason: {first_failed_test['Failure Reason']}"
    print(result_string)
