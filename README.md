# 🤖 AI Code Explainer

An interactive web application that leverages Generative AI to demystify Python code. Paste any code snippet and receive an instant, clear, and educational explanation, making it an invaluable tool for students and developers learning to code.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Gemini-API](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

- **AI-Powered Explanations**: Utilizes Google's powerful Gemini 2.0 Flash model to generate high-quality, beginner-friendly code explanations.
- **Elegant UI/UX**: Built with Streamlit for a clean, intuitive, and responsive user interface.
- **Resilient Architecture**: Implements a robust fallback mechanism. If the API fails, the app provides a basic static analysis instead of crashing.
- **Zero Configuration for Beginners**: Users can try the app immediately without an API key, with clear instructions provided for unlocking the full AI capabilities.

## 🛠️ Tech Stack

- **Frontend & Web Framework**: `Streamlit`
- **Backend & API Integration**: `Python`, `Requests`
- **AI Model & API**: **Google Gemini 2.0 Flash** (Primary), Custom local fallback logic
- **Environment Management**: `python-dotenv`
- **Deployment**: Streamlit Community Cloud (for live demo)

## 🚀 Live Demo

Experience the application live here:  
**[👉 AI Code Explainer Live Demo](https://ai-code-explainer-cgi6dou2aer6yldctlghkr.streamlit.app/)**  
*(Note: The live demo uses the basic analysis mode. For full AI power, clone the repo and add your API key.)*

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/ai-code-explainer.git
    cd ai-code-explainer
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API Key**
    - Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    - Create a `.env` file in the project root.
    - Add your key to the file:
      ```env
      GEMINI_API_KEY=your_actual_api_key_here
      ```

4.  **Run the application**
    ```bash
    streamlit run app.py
    ```

## 📁 Project Structure
ai-code-explainer/

├── app.py # Main Streamlit application

├── .env # Environment variables (gitignored)

├── requirements.txt # Project dependencies

└── README.md # Project documentation


## 🔮 Future Enhancements

- Support for multiple programming languages (JavaScript, Java, C++).
- Explanation depth selector (Beginner, Intermediate, Expert).
- Code summarization and documentation generation.
- Integration with additional AI models (e.g., GPT, Claude).

## 👨‍💻 Developer

**Disha Jain**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/disha-jain-562940251/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/D562-jain)

---
⭐ Star this repo if you found it helpful!
