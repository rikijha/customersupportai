# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token


import requests
import streamlit as st
import warnings
import os
from dotenv import load_dotenv
load_dotenv(".env")


try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "f87dc15b-0a8d-453a-84fc-382f03af289f"
FLOW_ID = "6314e52b-3742-4883-aa4d-476032c19a16"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "customersupportai" # You can set a specific endpoint name in the flow settings


def run_flow(message: str) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def main():
    st.title("Customer Support AI")

    message = st.text_area("Message", placeholder="Ask something...")

    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return

        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)

            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))


if __name__ == "__main__":
    main()