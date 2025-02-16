import google.generativeai as genai
import google.api_core.exceptions  # ✅ Import this for proper exception handling
import time

# List of API keys
API_KEYS = [
    'AIzaSyDvpbV34TFp2hGXWF5Hl9zONjlKeKoAuv8',
    'AIzaSyDhJfidnxBuUbHRo9suvX_nQUCHrqwqzAI',
    'AIzaSyB3Giz0lqT72uwivTH2ee5e6obNEZMpQd4',
    'AIzaSyCAhUtQo8_SoeDuwRuUpgIaIapBxK8uTIc',
    'AIzaSyATs_JN_vRbeWI0P2TGCaTCon5AWRAY_ys',
    'AIzaSyAOUt8Yirbs6BfOTxYDlf4TkKfdWAPovpw'
]

# Current API key index
current_key_index = 0
total_attempts = 0  # Track how many times we've looped through all API keys


def configure_gemini():
    """Configure the Gemini API with the current API key."""
    global current_key_index
    genai.configure(api_key=API_KEYS[current_key_index])

# Initialize with the first API key
configure_gemini()
model = genai.GenerativeModel('gemini-1.5-flash')

def switch_api_key():
    """Switch to the next available API key when the limit is reached."""
    global current_key_index, total_attempts

    if current_key_index < len(API_KEYS) - 1:
        current_key_index += 1
    else:
        total_attempts += 1  # Track full cycles
        if total_attempts >= 2:  # If we've tried all APIs twice, raise an error
            raise Exception("All API keys have reached their limits. Please wait or add more keys.")
        current_key_index = 0  # Restart from the first API key

    configure_gemini()  # Reconfigure with the new API key
    print(f"Switched to API Key {current_key_index + 1}")


def assign():
    """Generate content using the Gemini model, switching API keys if needed."""
    global model
    prompt = "Hello"

    while True:  # Keep retrying until a valid response is received
        try:
            response = model.generate_content([prompt])
            return response.text  # Return response if successful

        except google.api_core.exceptions.ResourceExhausted as e:
            print("⚠️ Rate limit exceeded. Trying next API key...")
            switch_api_key()  # Move to next API key
            model = genai.GenerativeModel("gemini-1.5-flash")  # Reset model
            time.sleep(2)  # Small delay before retrying

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise e  # Raise other errors

# Loop to generate responses and store them in a list
responses = []
for i in range(150):
    print(f"Generating response {i+1}...")
    responses.append(assign())

# Print all responses
for idx, response in enumerate(responses, start=1):
    print(f"Response {idx}:\n{response}\n")
