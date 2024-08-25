import streamlit as st
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv
from openai import OpenAI
import imagehash

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set page config
st.set_page_config(page_title="Chef's Fridge Recipe Generator", layout="wide")

def image_hash(image):
    return str(imagehash.average_hash(image))

def is_duplicate(new_image, existing_images):
    new_hash = image_hash(new_image)
    for img in existing_images:
        if image_hash(img) == new_hash:
            return True
    return False

def identify_items(images):
    all_items = []
    for image in images:
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "List all the food items you can see in this fridge image. Provide the list in a comma-separated format."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=300
            )
            
            items = response.choices[0].message.content.split(',')
            all_items.extend([item.strip() for item in items])
        except Exception as e:
            st.error(f"An error occurred while identifying items: {str(e)}")
    
    return list(set(all_items))  # Remove duplicates

def generate_recipe(items, diet_preference, cuisine_preference):
    try:
        diet_instruction = f"The recipe should be {diet_preference.lower()}." if diet_preference != "None" else ""
        cuisine_instruction = f"The recipe should be {cuisine_preference} cuisine." if cuisine_preference != "Any" else ""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"Create a recipe using these ingredients: {', '.join(items)}. {diet_instruction} {cuisine_instruction} Provide the recipe name, ingredients with quantities, and step-by-step instructions."
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred while generating the recipe: {str(e)}")
        return "Unable to generate recipe. Please try again."

def main():
    st.title("Chef's Fridge Recipe Generator")
    
    if 'images' not in st.session_state:
        st.session_state.images = []
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Fridge Contents")
        image_option = st.radio("Choose an option:", ("Take Pictures", "Upload Images"))
        
        if image_option == "Take Pictures":
            camera_image = st.camera_input("Take a picture of your fridge contents")
            if camera_image:
                new_image = Image.open(camera_image)
                if not is_duplicate(new_image, st.session_state.images):
                    st.session_state.images.append(new_image)
                    st.success("Image added successfully!")
        else:
            uploaded_files = st.file_uploader("Upload fridge images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
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
                    st.success(f"{new_images} new image(s) added successfully!")
                if duplicates > 0:
                    st.info(f"{duplicates} duplicate image(s) were not added.")
        
        if st.session_state.images:
            st.subheader("Captured/Uploaded Images")
            for i, img in enumerate(st.session_state.images):
                st.image(img, caption=f'Fridge Content Image {i+1}', use_column_width=True)
            
            if st.button('Clear All Images'):
                st.session_state.images = []
                st.experimental_rerun()
            
            if st.button('Identify Ingredients'):
                with st.spinner('Analyzing fridge contents...'):
                    identified_items = identify_items(st.session_state.images)
                    st.session_state.ingredients = identified_items
    
    with col2:
        st.header("Ingredients and Recipe")
        
        if 'ingredients' in st.session_state:
            st.subheader("Identified Ingredients")
            ingredients = st.text_area("Edit, add, or remove ingredients:",
                                       value='\n'.join(st.session_state.ingredients))
            st.session_state.ingredients = [item.strip() for item in ingredients.split('\n') if item.strip()]
            
            st.subheader("Final Ingredient List")
            st.write(", ".join(st.session_state.ingredients))
            
            # Dietary Preferences
            st.subheader("Dietary Preferences")
            diet_options = ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Low-Carb", "Paleo"]
            diet_preference = st.selectbox("Select dietary preference:", diet_options)
            
            cuisine_options = ["Any", "Italian", "Mexican", "Asian", "Mediterranean", "American", "Indian", "French"]
            cuisine_preference = st.selectbox("Select cuisine preference:", cuisine_options)
            
            if st.button('Generate Recipe'):
                with st.spinner('Crafting your recipe...'):
                    recipe = generate_recipe(st.session_state.ingredients, diet_preference, cuisine_preference)
                    st.subheader("Your Recipe")
                    st.write(recipe)
        else:
            st.info("Take or upload pictures of your fridge contents, then click 'Identify Ingredients' to start.")

if __name__ == "__main__":
    main()
