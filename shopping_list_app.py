import streamlit as st
import pandas as pd
import json
from collections import defaultdict

# Page config
st.set_page_config(page_title="Weekly Shopping List Builder", page_icon="🛒", layout="wide")

# Load data files
@st.cache_data
def load_ingredients():
    try:
        with open('ingredients.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@st.cache_data
def load_recipes():
    try:
        with open('recipes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def generate_shopping_list(selected_meals, recipes, ingredients):
    """Generate shopping list grouped by shop section"""
    shopping_dict = defaultdict(lambda: defaultdict(float))
    
    # Aggregate ingredients from selected meals
    for meal in selected_meals:
        if meal in recipes:
            for ingredient, quantity in recipes[meal]['ingredients'].items():
                if ingredient in ingredients:
                    section = ingredients[ingredient]['section']
                    shopping_dict[section][ingredient] = shopping_dict[section][ingredient] + quantity
    
    return shopping_dict

def format_shopping_list(shopping_dict, ingredients):
    """Format shopping list as text with sections"""
    section_order = ['Fruit & Veg', 'Fridge', 'Dry Store', 'Freezer', 'Non-Consumables']
    
    output = "=== WEEKLY SHOPPING LIST ===\n\n"
    
    for section in section_order:
        if section in shopping_dict:
            output += f"--- {section.upper()} ---\n"
            for ingredient, quantity in sorted(shopping_dict[section].items(), key=lambda x: ingredients[x[0]].get('order', 999)):
                if quantity == int(quantity):
                    quantity = int(quantity)
                output += f"  • {ingredient}: {quantity}\n"
            output += "\n"
    
    return output

# Main app
st.title("🛒 Weekly Shopping List Builder")
st.markdown("Select your meals for the week and generate your shopping list organized by shop section")

# Load data
ingredients = load_ingredients()
recipes = load_recipes()

if not ingredients or not recipes:
    st.error("⚠️ Missing data files! Please ensure ingredients.json and recipes.json are in the same folder.")
    st.stop()

# --- User filter ---
USERS = ["All", "Amy", "Roi", "Hannah"]

st.sidebar.header("👤 Whose recipes?")
selected_user = st.sidebar.selectbox(
    label="Show recipes for:",
    options=USERS,
    index=0,  # default to "All"
    label_visibility="collapsed"
)

# Filter recipes by selected user
if selected_user == "All":
    filtered_recipes = recipes
else:
    filtered_recipes = {
        name: data for name, data in recipes.items()
        if data.get("user", "Amy") == selected_user
    }

# Sidebar for meal selection
st.sidebar.header("📅 This Week's Meals")
st.sidebar.markdown("Select the meals you're planning:")

selected_meals = []
for recipe_name in sorted(filtered_recipes.keys()):
    if st.sidebar.checkbox(recipe_name, key=recipe_name):
        selected_meals.append(recipe_name)

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear All", use_container_width=True):
    st.rerun()

# Main content area
if selected_meals:
    st.subheader(f"Selected Meals ({len(selected_meals)})")
    cols = st.columns(min(3, len(selected_meals)))
    for idx, meal in enumerate(selected_meals):
        with cols[idx % 3]:
            st.info(f"✓ {meal}")
    
    st.markdown("---")
    
    # Generate shopping list
    shopping_dict = generate_shopping_list(selected_meals, recipes, ingredients)
    
    if shopping_dict:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Your Shopping List")

            # Track ticked items in session state
            if 'ticked' not in st.session_state:
                st.session_state.ticked = set()

            col_reset, col_progress = st.columns([1, 2])
            with col_reset:
                if st.button("↺ Reset ticks"):
                    st.session_state.ticked = set()
                    st.rerun()

            section_order = ['Fruit & Veg', 'Fridge', 'Dry Store', 'Freezer', 'Non-Consumables']
            total_items = sum(len(shopping_dict[s]) for s in section_order if s in shopping_dict)
            ticked_count = len(st.session_state.ticked)

            with col_progress:
                st.progress(ticked_count / total_items if total_items > 0 else 0,
                            text=f"{ticked_count} of {total_items} done")

            for section in section_order:
                if section in shopping_dict:
                    st.markdown(f"**{section}**")
                    for ingredient, quantity in sorted(shopping_dict[section].items(), key=lambda x: ingredients[x[0]].get('order', 999)):
                        if quantity == int(quantity):
                            quantity = int(quantity)
                        item_key = f"tick_{ingredient}"
                        ticked = ingredient in st.session_state.ticked
                        label = f"~~{ingredient}: {quantity}~~" if ticked else f"{ingredient}: **{quantity}**"
                        if st.checkbox(label, value=ticked, key=item_key):
                            st.session_state.ticked.add(ingredient)
                        else:
                            st.session_state.ticked.discard(ingredient)
                    st.markdown("")
        
        with col2:
            st.subheader("📱 Copy to Phone")
            text_output = format_shopping_list(shopping_dict, ingredients)
            st.text_area("Copy this text:", text_output, height=400)
            st.caption("Copy the text above and paste into your phone's notes or messaging app")
    
else:
    st.info("👈 Select meals from the sidebar to generate your shopping list")
    
    # Show available recipes
    st.subheader("Available Recipes")
    recipe_cols = st.columns(3)
    for idx, (recipe_name, recipe_data) in enumerate(sorted(filtered_recipes.items())):
        with recipe_cols[idx % 3]:
            with st.expander(recipe_name):
                st.markdown("**Ingredients:**")
                for ingredient, qty in recipe_data['ingredients'].items():
                    st.markdown(f"- {ingredient}: {qty}")

# Footer
st.markdown("---")
