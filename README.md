# FridgeFusion

> AI-powered recipe generator that transforms your fridge ingredients into personalized recipes — powered by Google Gemini Vision API and OpenAI.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google_Gemini-API-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)
[![Stars](https://img.shields.io/github/stars/SauravSrivastav/fridgefusion-st?style=flat-square)](https://github.com/SauravSrivastav/fridgefusion-st)

---

## Overview

FridgeFusion solves the daily problem of "what should I cook?" by using **AI image recognition** to identify ingredients from a photo of your fridge and generate creative, personalized recipes — instantly.

Built with **Streamlit** for the UI, **Google Gemini Vision** for image analysis, and **OpenAI** for recipe generation.

---

## Features

- **Ingredient Recognition** — Upload a fridge photo, AI identifies all ingredients automatically
- **Personalized Recipes** — Recipes tailored to your dietary preferences and available items
- **Nutritional Info** — Calorie count and macro breakdown for each recipe
- **Waste Reduction** — Uses what you already have, minimizes food waste
- **Multi-Cuisine** — Suggests recipes across cuisines based on ingredients

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI Vision | Google Gemini Vision API |
| Recipe Gen | OpenAI GPT |
| Language | Python 3.9+ |
| Deployment | Streamlit Cloud / Azure |

---

## Quick Start

```bash
git clone https://github.com/SauravSrivastav/fridgefusion-st.git
cd fridgefusion-st
pip install -r requirements.txt

# Add your API keys to .env
echo "GEMINI_API_KEY=your_key" >> .env
echo "OPENAI_API_KEY=your_key" >> .env

streamlit run app.py
```

---

## Project Structure

```
fridgefusion-st/
├── app.py              # Main Streamlit application
├── openai.py           # OpenAI recipe generation module
├── requirements.txt    # Dependencies
├── data/               # Sample data and test images
└── .env                # API keys (not committed)
```

---

## Built By

**Saurav Srivastav** — Cloud & DevSecOps Leader | Azure · MLOps · LLMOps | Dubai, UAE

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/sauravsrivastav2205/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-0078D4?style=flat-square&logo=vercel)](https://saurav-srivastav-portfolio.vercel.app)

---

<sub>Streamlit · Gemini API · OpenAI · Python · AI · Generative AI · Recipe Generator · Computer Vision · LLM · Azure AI</sub>
