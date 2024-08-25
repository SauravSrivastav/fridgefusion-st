# FridgeFusion 🍳🥗 - Your Smart Kitchen Assistant

**FridgeFusion** is an innovative AI-powered app that turns your fridge contents into delicious recipes! 🚀 Say goodbye to food waste and hello to creative cooking with personalized recipe suggestions tailored to your available ingredients and dietary preferences.

## 🌟 Overview

FridgeFusion is the ultimate solution for anyone looking to make the most of their kitchen inventory. Whether you're a seasoned chef 👨‍🍳 or a cooking novice 🍽️, our application provides customized recipe recommendations based on what's in your fridge. Leveraging cutting-edge AI technology, FridgeFusion delivers accurate, actionable recipes that help you create tasty meals while reducing food waste. 🌿♻️

## 🔥 Key Features

- 📸 **Image-Based Ingredient Recognition**: Upload fridge photos for instant ingredient identification
- 🍽️ **Customized Recipe Generation**: Get personalized recipes based on your available ingredients
- 🍣 **Multiple Recipe Options**: Choose from various recipe suggestions
- 🥕 **Dietary Preference Support**: Tailor recipes to your specific dietary needs or restrictions
- 📄 **PDF Recipe Download**: Save generated recipes as PDFs for offline use
- 🖥️ **User-Friendly Interface**: Navigate effortlessly with our intuitive, step-by-step process

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+ 🐍
- Streamlit 🌟
- Pillow (PIL) 🖼️
- python-dotenv 🔐
- google-generativeai 🧠
- fpdf 📄

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/SauravSrivastav/fridgefusion-st.git
    cd fridgefusion-st
    ```

2. **Create and Activate a Virtual Environment:**
    - Windows:
      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```
    - macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3. **Install required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up Google Generative AI (Gemini) API key:**
    - Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
    - Create a `.env` file in the project root:
      ```env
      GEMINI_API_KEY=your_api_key_here
      ```

5. **Launch the app:**
    ```bash
    streamlit run app.py
    ```

6. **Deactivate Virtual Environment (When Done):**
    ```bash
    deactivate
    ```

## 🚀 How to Use FridgeFusion

1. 📸 Upload fridge images or snap photos with your device
2. 📝 Review and edit the AI-identified ingredients
3. 🍽️ Select dietary preferences and number of recipes
4. 👨‍🍳 Generate personalized recipes from your ingredients
5. 💾 Download recipes as PDF or view in-app

## 📸 App Screenshots

[Insert eye-catching screenshots of your application here]

## 🤝 Contributing

We welcome contributions! 🎉 To improve FridgeFusion:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss your ideas.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact Us

Have questions or suggestions? Reach out to us:

- 📧 Email: [Sauravsrivastav2205@gmail.com](mailto:Sauravsrivastav2205@gmail.com)
- 💼 LinkedIn: [in/sauravsrivastav2205](https://www.linkedin.com/in/sauravsrivastav2205)
- 🐙 GitHub: [https://github.com/SauravSrivastav](https://github.com/SauravSrivastav)

---
