# prompt_masker_indian_context

A simple Python script designed to mask confidential details and personal identifiers in text prompts. This script identifies and replaces sensitive information with appropriate placeholders.

## Features
The script masks the following types of information:
- **PAN Number**: Replaced with `[PAN_NUMBER]`
- **Aadhar Number**: Replaced with `[AADHAR_NUMBER]`
- **Indian Passport Number**: Replaced with `[PASSPORT_NUMBER]`
- **Driving License Number**: Replaced with `[DL_NUMBER]`
- **UPI ID**: Replaced with `[UPI_ID]`
- **Indian Bank Account Number**: Replaced with `[BANK_ACCOUNT]`
- **IFSC Code**: Replaced with `[IFSC_CODE]`
- **Indian Phone Number**: Replaced with `[PHONE_NUMBER]`
- **Email Address**: Replaced with `[EMAIL_ADDRESS]`
- **Person Name**: Replaced with `[PERSON_NAME]`
- **Organization Name**: Replaced with `[ORGANIZATION]`
- **Location (GPE)**: Replaced with `[LOCATION]`

## Additional Information
- A Gradio interface has been provided for a simple and user-friendly way to test and use the script.

## Getting Started
1. Clone the repository.
2. Ensure you have Python installed.
3. Install required dependencies.
4. Run the script and/or Gradio interface to mask input data.

Feel free to modify or expand based on specific requirements or additional features.
