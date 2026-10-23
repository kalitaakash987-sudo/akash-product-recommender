# NOVA — Product Recommendation System

A dark, responsive e-commerce discovery website built with Python, Flask, HTML, CSS, and a small amount of JavaScript. Product data is sample/demo data for a college assignment.

## Features
- Product catalog across Electronics, Fashion, Home, and Lifestyle
- Search by product name, category, subcategory, or tags
- Category filters, sorting, and maximum-price filter
- Rule-based personalized recommendations based on selected interests and budget
- Related-product suggestions on product detail pages
- Session-based wishlist and shopping bag
- Responsive dark UI with gradients, animated product cards, and mobile layout

## Requirements
- Python 3.10 or newer
- Internet connection for Google Fonts; the site otherwise works without external product images because the catalog uses emoji artwork.

## Run locally

### Windows
1. Extract the ZIP.
2. Open the extracted `novanest_recommender` folder in VS Code.
3. Open the VS Code terminal in that folder.
4. Create a virtual environment:
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the website:
   ```bash
   python app.py
   ```
7. Open `http://127.0.0.1:5000` in your browser.

If `py` is not recognized, try `python` instead. If PowerShell blocks activation, use Command Prompt or run `.venv\\Scripts\\python.exe -m pip install -r requirements.txt`, then `.venv\\Scripts\\python.exe app.py`.

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000`.

## How the recommendation logic works
The recommender is intentionally simple and explainable:
1. The user chooses interest tags and a maximum budget.
2. Products outside the budget (and any selected category filter) are excluded.
3. Each matching interest tag adds 2 points to a product's score.
4. The product rating contributes a small bonus (`rating / 5`).
5. Products are sorted by score, then rating, and shown as recommendations.

This is a rule-based recommendation system, not a trained machine-learning model. That makes it easy to explain during a viva.

## Project structure
```text
novanest_recommender/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── product.html
│   └── cart.html
└── static/
    ├── style.css
    └── script.js
```

## Important notes
- Product prices and ratings are sample data; they are not live retail listings.
- The bag is a demo cart; no payment or real checkout is implemented.
- `app.secret_key` is a development placeholder. Replace it with a secure random value before deploying publicly.
- `debug=True` is for local development only. Turn it off for public deployment.
