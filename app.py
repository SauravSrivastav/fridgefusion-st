import streamlit as st
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv
import google.generativeai as genai
import hashlib
import pandas as pd
from fpdf import FPDF

# Load environment variables
load_dotenv()

# Set up Google Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Set page config
st.set_page_config(page_title="Chef's Fridge Recipe Generator", layout="wide", page_icon="🍴")

# Custom CSS
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
        background-color: #3498db;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border-color: #bdc3c7;
    }
    .stSelectbox>div>div>div {
        border-radius: 10px;
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .recipe-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .stAlert {
        border-radius: 10px;
    }
    .stProgress > div > div > div > div {
        background-color: #3498db;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper functions
def image_to_bytes(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return buffered.getvalue()

def image_hash(image):
    return hashlib.md5(image_to_bytes(image)).hexdigest()

def is_duplicate(new_image, existing_images):
    new_hash = image_hash(new_image)
    for img in existing_images:
        if image_hash(img) == new_hash:
            return True
    return False

def identify_items(images):
    all_items = []
    for image in images:
        base64_image = base64.b64encode(image_to_bytes(image)).decode('utf-8')

        try:
            response = model.generate_content([
                "List all the food items you can see in this fridge image. Provide the list in a comma-separated format.",
                {"mime_type": "image/jpeg", "data": base64_image}
            ])

            items = response.text.split(',')
            all_items.extend([item.strip() for item in items])
        except Exception as e:
            st.error(f"An error occurred while identifying items: {str(e)}")

    return list(set(all_items))  # Remove duplicates

def generate_recipe(items, diet_preference, cuisine_preference):
    try:
        diet_instruction = f"The recipe should be {diet_preference.lower()}." if diet_preference != "None" else ""
        cuisine_instruction = f"The recipe should be {cuisine_preference} cuisine." if cuisine_preference != "Any" else ""

        prompt = f"Create a recipe using these ingredients: {', '.join(items)}. {diet_instruction} {cuisine_instruction} Provide the recipe name, ingredients with quantities, and step-by-step instructions."

        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        st.error(f"An error occurred while generating the recipe: {str(e)}")
        return "Unable to generate recipe. Please try again."

def generate_multiple_recipes(items, diet_preference, cuisine_preference, num_recipes):
    recipes = []
    for _ in range(num_recipes):
        recipe = generate_recipe(items, diet_preference, cuisine_preference)
        recipes.append(recipe)
    return recipes

def get_pdf_download_link(recipes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Use a default font
    pdf.set_font("Arial", size=12)

    for i, recipe in enumerate(recipes, 1):
        pdf.cell(200, 10, txt=f"Recipe {i}", ln=True, align="C")
        pdf.multi_cell(0, 10, txt=recipe)
        pdf.ln(10)

    pdf_output = pdf.output(dest="S").encode("latin-1", errors="ignore")
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="recipes.pdf">Download PDF File</a>'
    return href

# Initialize session state
def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'
    if 'images' not in st.session_state:
        st.session_state.images = []
    if 'ingredients' not in st.session_state:
        st.session_state.ingredients = []
    if 'recipes' not in st.session_state:
        st.session_state.recipes = []

# Progress bar
def show_progress():
    pages = ['Home', 'Upload Images', 'Identify Ingredients', 'Generate Recipe']
    current_page_index = pages.index(st.session_state.page)
    progress = (current_page_index) / (len(pages) - 1)
    st.progress(progress)
    st.write(f"Step {current_page_index + 1} of {len(pages)}")

# Tooltip helper
def tooltip(text, help_text):
    return f'<div class="tooltip">{text}<span class="tooltiptext">{help_text}</span></div>'

# Page functions
def home_page():
    st.title("🍴 Chef's Fridge Recipe Generator 🍴")
    st.markdown("""
    Welcome to the Chef's Fridge Recipe Generator!

    This app helps you create delicious recipes based on the contents of your fridge.
    Here's how it works:

    1. **Upload Images**: Take pictures of your fridge contents or upload existing images.
    2. **Identify Ingredients**: Our AI will analyze the images and identify the ingredients.
    3. **Generate Recipes**: Choose your dietary preferences, select the number of recipes, and we'll create custom recipes for you.
    4. **Download Recipes**: Save your generated recipes for later use!

    Click 'Start' to begin!
    """)
    if st.button('Start', key='start_button', use_container_width=True):
        st.session_state.page = 'Upload Images'
        st.rerun()

def upload_images_page():
    st.header("📸 Upload Fridge Images")
    st.markdown(tooltip("Instructions:", "Follow these steps to add images of your fridge contents."), unsafe_allow_html=True)
    st.markdown("""
    1. Choose an option to either upload images or take pictures.
    2. Add images of your fridge contents.
    3. Proceed to the next step to identify ingredients.
    """)

    image_option = st.radio("Choose an option:", ("Upload Images", "Take Pictures"), horizontal=True)

    if image_option == "Take Pictures":
        camera_image = st.camera_input("📷 Take a picture of your fridge contents")
        if camera_image:
            new_image = Image.open(camera_image)
            if not is_duplicate(new_image, st.session_state.images):
                st.session_state.images.append(new_image)
                st.success("Image added successfully! 🎉")
            else:
                st.warning("This image is a duplicate and was not added.")
    else:
        uploaded_files = st.file_uploader("📤 Upload fridge images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        if uploaded_files:
            new_images = 0
            duplicates = 0
            for uploaded_file in uploaded_files:
                new_image = Image.open(uploaded_file)
                if not is_duplicate(new_image, st.session_state.images):
                    st.session_state.images.append(new_image)
                    new_images += 1
                else:
                    duplicates += 1

            if new_images > 0:
                st.success(f"{new_images} new image(s) added successfully! 🎉")
            if duplicates > 0:
                st.info(f"{duplicates} duplicate image(s) were not added.")

    if st.session_state.images:
        st.subheader("Captured/Uploaded Images")
        cols = st.columns(3)
        for i, img in enumerate(st.session_state.images):
            cols[i % 3].image(img, caption=f'Image {i+1}', use_column_width=True)

        if st.button('🗑️ Clear All Images', use_container_width=True):
            st.session_state.images = []
            st.rerun()

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('⬅️ Back to Home', key='back_to_home', use_container_width=True):
            st.session_state.page = 'Home'
            st.rerun()
    with col2:
        if st.button('Next ➡️', key='to_identify', use_container_width=True):
            if not st.session_state.images:
                st.error("Please upload at least one image before proceeding.")
            else:
                st.session_state.page = 'Identify Ingredients'
                st.rerun()

def identify_ingredients_page():
    st.header("🔍 Identify Ingredients")
    st.markdown(tooltip("Instructions:", "Follow these steps to identify ingredients from your fridge images."), unsafe_allow_html=True)
    st.markdown("""
    1. Click the 'Identify Ingredients' button to analyze the uploaded images.
    2. Review and edit the identified ingredients.
    3. Proceed to the next step to generate recipes.
    """)

    if not st.session_state.images:
        st.warning("Please upload images of your fridge contents first.")
        return

    if st.button('🔍 Identify Ingredients', use_container_width=True):
        with st.spinner('Analyzing fridge contents... 🕵️‍♂️'):
            identified_items = identify_items(st.session_state.images)
            st.session_state.ingredients = identified_items

    if st.session_state.ingredients:
        st.subheader("Identified Ingredients")
        ingredients = st.text_area("✏️ Edit, add, or remove ingredients:",
                                   value='\n'.join(st.session_state.ingredients),
                                   height=200,
                                   help="Each ingredient should be on a new line.")
        st.session_state.ingredients = [item.strip() for item in ingredients.split('\n') if item.strip()]

        st.subheader("Final Ingredient List")
        st.write(", ".join(st.session_state.ingredients))

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('⬅️ Back to Upload', key='back_to_upload', use_container_width=True):
            st.session_state.page = 'Upload Images'
            st.rerun()
    with col2:
        if st.button('Next ➡️', key='to_generate', use_container_width=True):
            if not st.session_state.ingredients:
                st.error("Please identify ingredients before proceeding.")
            else:
                st.session_state.page = 'Generate Recipe'
                st.rerun()

def generate_recipe_page():
    st.header("🍲 Generate Recipes")
    st.markdown(tooltip("Instructions:", "Follow these steps to generate custom recipes."), unsafe_allow_html=True)
    st.markdown("""
    1. Select your dietary and cuisine preferences.
    2. Choose the number of recipes you want to generate.
    3. Click the 'Generate Recipes' button to create custom recipes.
    4. Download your recipes and enjoy your meals!
    """)

    if not st.session_state.ingredients:
        st.warning("Please identify ingredients first.")
        return

    st.subheader("Preferences")
    col1, col2, col3 = st.columns(3)
    with col1:
        diet_options = ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Low-Carb", "Paleo"]
        diet_preference = st.selectbox("🥗 Select dietary preference:", diet_options)
    with col2:
        cuisine_options = ["Any", "Italian", "Mexican", "Asian", "Mediterranean", "American", "Indian", "French"]
        cuisine_preference = st.selectbox("🌍 Select cuisine preference:", cuisine_options)
    with col3:
        num_recipes = st.slider("🔢 Number of recipes:", min_value=1, max_value=5, value=1)

    if st.button('🧑‍🍳 Generate Recipes', use_container_width=True):
        with st.spinner(f'Crafting your {num_recipes} recipe(s)... 👨‍🍳'):
            recipes = generate_multiple_recipes(st.session_state.ingredients, diet_preference, cuisine_preference, num_recipes)
            st.session_state.recipes = recipes

    if st.session_state.recipes:
        st.subheader("Your Recipes")
        for i, recipe in enumerate(st.session_state.recipes, 1):
            st.markdown(f'<div class="recipe-container"><h3>Recipe {i}</h3>{recipe}</div>', unsafe_allow_html=True)

        # Provide download link
        st.markdown(get_pdf_download_link(st.session_state.recipes), unsafe_allow_html=True)

    # Navigation button
    if st.button('⬅️ Back to Ingredients', key='back_to_ingredients', use_container_width=True):
        st.session_state.page = 'Identify Ingredients'
        st.rerun()

def main():
    init_session_state()
    show_progress()

    # Sidebar navigation
    st.sidebar.title("Navigation")
    pages = ["Home", "Upload Images", "Identify Ingredients", "Generate Recipe"]
    page = st.sidebar.radio("Go to", pages, index=pages.index(st.session_state.page))

    if page != st.session_state.page:
        st.session_state.page = page
        st.rerun()

    # Main content based on current page
    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Upload Images":
        upload_images_page()
    elif st.session_state.page == "Identify Ingredients":
        identify_ingredients_page()
    elif st.session_state.page == "Generate Recipe":
        generate_recipe_page()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Created with ❤️ using Streamlit")
    st.sidebar.markdown("[Report an Issue](https://github.com/yourusername/chef-fridge-recipe-generator/issues)")

if __name__ == "__main__":
    main()