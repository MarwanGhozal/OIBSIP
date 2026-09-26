## Privacy Considerations

Ghozal Assistant is designed to process user input locally where possible.

### Data Processing

- **Voice input:** Speech is captured through the user's microphone and converted to text using the speech recognition service used by the application.
- **Text commands:** Recognized text is processed locally by the assistant to determine the user's intent and perform the requested action.
- **Intent classification:** The intent classifier runs locally using a TF-IDF vectorizer and Logistic Regression model.
- **Knowledge questions:** General knowledge questions supported by the local knowledge base are answered locally without sending the question to an external AI service.
- **Custom commands:** Custom commands are loaded from the local `commands.json` configuration file.
- **Weather:** Weather requests use an external weather API. The selected city is sent to the weather service to retrieve current weather information.
- **Web searches:** Search requests open a Google search in the user's web browser. The search query is therefore sent to Google.
- **Email:** When the email feature is used, the recipient, subject, and message are sent through the configured email service.
- **Reminders:** Reminder information is kept in the running application while the assistant is active.

### Credentials

Email credentials and API keys are stored in environment variables rather than directly in the source code.

The `.env` file should **never be committed to the repository**. It should be included in `.gitignore`.

Example:

```text
GHOZAL_EMAIL_ADDRESS=your_email@example.com
GHOZAL_EMAIL_APP_PASSWORD=your_app_password
GHOZAL_WEATHER_API_KEY=your_api_key