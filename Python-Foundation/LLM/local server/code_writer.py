import requests

# 1. Point to your active local high-level code endpoint
GENERATOR_URL = "http://localhost:8000/v1/generate_code"


def request_code(requirement, language="python"):
    payload = {"prompt": requirement, "language": language}

    print(f"⚡ Local 7B AI Architect is structuring your {language} script...")
    response = requests.post(GENERATOR_URL, json=payload)
    return response.text


if __name__ == "__main__":
    # The programmatic prompt for the local 7B engine to build
    user_requirement = (
        "Create a robust file archiving function that accepts a directory path, "
        "compresses all files inside it into a clean zip format using standard modules, "
        "and implements comprehensive try/except error logging blocks."
    )

    # Execute the API hit
    source_code = request_code(user_requirement, language="python")

    # 2. Save the output string directly into a new script file!
    output_filename = "auto_generated_archive_tool.py"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(source_code)

    print(f"\n📦 Success! High-level code written and saved to -> {output_filename}")
