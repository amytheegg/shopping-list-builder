# 🛒 Weekly Shopping List Builder

A Streamlit app that helps you plan your weekly meals and automatically generates a shopping list organized by shop sections.

## Features

- Select meals for the week from your recipe collection
- Automatically aggregates ingredients (e.g., if two meals need red peppers, it adds them up)
- Groups shopping list by shop sections: Fruit & Veg, Fridge, Dry Store, Freezer, Non-Consumables
- Provides copy-friendly text output for your phone
- Easy to add new recipes and ingredients

## Local Setup

1. **Install requirements:**
   ```bash
   pip install streamlit pandas
   ```

2. **Run the app:**
   ```bash
   streamlit run shopping_list_app.py
   ```

3. **Open in browser:**
   - The app will automatically open at `http://localhost:8501`
   - Access from your phone on the same WiFi network using your PC's IP address (e.g., `http://192.168.1.100:8501`)

## Deploying to Streamlit Cloud (FREE)

1. **Create a GitHub account** (if you don't have one): https://github.com

2. **Create a new repository:**
   - Go to https://github.com/new
   - Name it something like `shopping-list-app`
   - Set to Public (required for free tier)
   - Click "Create repository"

3. **Upload your files to GitHub:**
   - Click "uploading an existing file"
   - Drag and drop these files:
     - `shopping_list_app.py`
     - `ingredients.json`
     - `recipes.json`
     - `requirements.txt`
     - `README.md`
   - Click "Commit changes"

4. **Deploy to Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Sign up/log in with your GitHub account
   - Click "New app"
   - Select your repository (`shopping-list-app`)
   - Main file path: `shopping_list_app.py`
   - Click "Deploy!"

5. **Access your app:**
   - You'll get a URL like `https://your-username-shopping-list-app.streamlit.app`
   - Bookmark this on your phone!
   - Share with family if you want

## Customizing Your App

### Adding New Ingredients

Edit `ingredients.json`:

```json
{
  "ingredient_name": {
    "section": "Fruit & Veg",  // or "Fridge", "Dry Store", "Freezer", "Non-Consumables"
    "unit": "whole"  // or "g", "ml", "pieces", "tins", etc.
  }
}
```

### Adding New Recipes

Edit `recipes.json`:

```json
{
  "Recipe Name": {
    "ingredients": {
      "ingredient_name": 2,  // quantity
      "another_ingredient": 400
    }
  }
}
```

### Updating the App

If deployed to Streamlit Cloud:
1. Edit the JSON files on GitHub (click the file, then the pencil icon)
2. Commit your changes
3. Streamlit Cloud will automatically redeploy (takes 1-2 minutes)

## Tips

- **Planning ahead:** Select meals at the start of the week and copy the list to your phone
- **Editing on the go:** Access from your phone's browser to check what you've selected
- **Family collaboration:** Share the URL so everyone can see the meal plan
- **Stock check:** Cross off items you already have before heading to the shop

## Troubleshooting

**App shows "Missing data files" error:**
- Make sure `ingredients.json` and `recipes.json` are in the same folder as the Python file
- If on Streamlit Cloud, ensure all files were uploaded to GitHub

**Want to make recipes/ingredients private:**
- Keep the app URL private (only share with trusted people)
- Or upgrade to Streamlit Cloud paid tier ($20/month) for private repos

**App not loading:**
- For local: Check that Streamlit is installed and you're running from the correct folder
- For Streamlit Cloud: Check the deployment logs for errors

## Future Enhancements Ideas

- Track what's already in your cupboard/fridge to avoid buying duplicates
- Nutritional information per meal
- Cost estimation based on typical prices
- Export to Google Keep or other apps
- Multiple shopping lists (e.g., separate list for health food shop)

Enjoy your organized shopping! 🎉
