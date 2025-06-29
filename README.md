# Context-Restricted Chatbot

A sophisticated Python-based chatbot application developed using the Streamlit framework. This project showcases a context-restricted conversational agent that responds exclusively based on user-provided training data, integrated with email registration and simulation features. The application is designed to be user-friendly, deployable, and extensible for real-world use cases.

## Project Overview

This chatbot is a custom-built solution that empowers users to train it with specific reference materials such as FAQs, product descriptions, or any textual content. The core functionality restricts the chatbot's responses to the trained context, ensuring accuracy and relevance. Additionally, it includes a robust email registration system that simulates email notifications and a dynamic sidebar profile for managing user emails. The project leverages the OpenAI API for advanced natural language processing, making it a powerful tool for interactive applications.

The development process focused on creating a clean, maintainable codebase with a responsive user interface, styled using custom CSS. This README provides a detailed guide to set up, use, and deploy the application, ensuring it can be easily adopted by other developers or integrated into larger systems.

## Setup Instructions

### Prerequisites
Before proceeding, ensure you have the following installed on your system:
- **Python 3.8 or Higher**: Required to run the application and its dependencies.
- **Git**: Necessary for cloning the repository (download from [git-scm.com](https://git-scm.com) if not installed).
- **An OpenAI API Key**: Obtain one by signing up at [OpenAI](https://platform.openai.com/) and generating an API key from your account dashboard.
- **Text Editor or IDE**: Recommended tools include Visual Studio Code, PyCharm, or Notepad++ for code editing.

### Installation Steps
Follow these detailed steps to set up the project on your local machine:

1. **Clone the Repository**
   - Open a terminal or command prompt.
   - Navigate to your desired directory (e.g., `C:\Users\username`) and clone the repository:
     ```bash
     git clone https://github.com/your-username/project_name.git
     cd project_name
2. Create a Virtual Environment

    Isolate project dependencies by creating a virtual environment:
    bash

       python -m venv venv
   
    Activate the virtual environment:
   
        On Windows: venv\Scripts\activate
   
        On macOS/Linux: source venv/bin/activate
   
    You should see (venv) in your terminal prompt, indicating the environment is active.
   
4. Install Dependencies

    Install the required Python packages listed in requirements.txt:
    bash

       pip install -r requirements.txt

If requirements.txt is missing, manually install the dependencies:
bash

    pip install streamlit openai python-dotenv
   Verify installation by checking versions (e.g., pip show streamlit).

4. Configure the OpenAI API Key

    Create a .env file in the project root directory:

    OPENAI_API_KEY=your-api-key-here
   
    Replace your-api-key-here with your actual OpenAI API key. Keep this file secure and exclude it from version control by adding it to .gitignore.
    For deployment on Streamlit Community Cloud, configure the API key in the Secrets section instead (see Deployment).

6. Run the Application

    Launch the Streamlit app from the terminal:
    bash

        streamlit run main.py
   
    Open your web browser and navigate to http://localhost:8501 to interact with the app.
   If the app doesn’t load, ensure all dependencies are installed and the API key is valid.

**Usage**
Training the Chatbot

   Step 1: Access the Training Section
        Locate the "Training input" header on the main page.
        
   Step 2: Enter Reference Data
        Use the text area to paste reference information such as FAQs, product manuals, or any text you want the bot to learn from.
        The text area supports multi-line input with a height of 200 pixels for convenience.
        
   Step 3: Save the Context
        Click the "Save Context" button to train the bot.
        A success message will appear if the training is successful; an error will display if the input is empty or the API fails.

**Chatting with the Bot**

   Step 1: Verify Training
        Ensure the bot is trained (check for the absence of the "Train the bot first" warning).
        
   Step 2: Ask Questions
        Type your question in the "Ask the Bot" chat input field and press Enter.
        The bot will respond based on the trained context. If the question is out of scope, it will reply: "I'm sorry, I can only answer questions based on the provided training content."
        
   Step 3: Review Chat History
        The chat interface displays a history of user questions and bot responses in a conversational format.

**Registering an Email**

   Step 1: Navigate to Email Registration
        Find the "Register Your Email" section below the chat area.
        
   Step 2: Enter Email
        Input a valid email address (must contain @) in the text field.
        
   Step 3: Submit Email
        Click "Submit Email" to register the address.
        The app simulates sending a welcome email ("Welcome" subject, "Thanks for signing up!" body) and displays a success message.
        An error will appear if the email is invalid.

**Profile Management**

   Step 1: View Profile
        Check the sidebar on the left for the "Profile" section.
        
   Step 2: Manage Emails
        If an email is registered, it will be displayed.
        Click "Add another email" to clear the current email and chat history, allowing a new email to be registered.
        
   Step 3: Reset and Continue
        After clicking "Add another email," return to the email registration section to enter a new address.

## Deployment
**Local Deployment**

   Follow the setup instructions above.
   
    Run the app locally with  streamlit run main.py.
    Test all features (training, chatting, email) in your browser.

**Streamlit Community Cloud Deployment**

  Step 1: Push to GitHub
        Commit and push your changes:
        bash

    git add .
    git commit -m "Ready for deployment"
    git push origin master

Step 2: Deploy on Streamlit

   Visit Streamlit Community Cloud.
   Connect your GitHub account and select the Chatbot-project repository.
   Set main.py as the entry point in the deployment settings.

Step 3: Configure Secrets

   Add your OpenAI API key in the Secrets section:
    toml

    [secrets]
    OPENAI_API_KEY = "your-api-key-here"
   Save and deploy the app.

Step 4: Share the App

   Once deployed, copy the generated URL (e.g., https://your-username-chatbot-project.streamlit.app) and share it.

## Features

 - Custom Training: Train the chatbot with any textual reference data.
 - Context Restriction: Limits responses to trained content with an out-of-scope message.
 - Email Simulation: Registers emails and simulates welcome notifications.
 - Dynamic Profile: Displays and manages registered emails in the sidebar.
 - Chat History Management: Clears chat history when adding a new email.
 - Responsive UI: Custom-styled interface with a clean layout.
   
## Future Improvements

  - Add support for file uploads as an alternative training method.
  - Implement real email sending using an SMTP service.
  - Enhance UI with additional styling options or themes.
  - Integrate a database to persist chat and email data.
