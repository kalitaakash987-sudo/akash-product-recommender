from flask import Flask, render_template, request, redirect, url_for, session
from collections import Counter

app = Flask(__name__)
app.secret_key = "change-this-secret-key-for-production"

# Demo catalog: prices and ratings are sample data for the college project.
PRODUCTS = [
    {"id": 1, "name": "AeroBeat Pro", "category": "Electronics", "subcategory": "Audio", "price": 4999, "rating": 4.7, "emoji": "🎧", "color": "violet", "tags": ["audio", "music", "wireless", "tech"], "description": "Immersive wireless audio with rich bass and all-day comfort."},
    {"id": 2, "name": "PixelWave X", "category": "Electronics", "subcategory": "Phones", "price": 42999, "rating": 4.8, "emoji": "📱", "color": "blue", "tags": ["phone", "camera", "tech", "daily"], "description": "A bright display, crisp photos, and fast everyday performance."},
    {"id": 3, "name": "Pulse Smartwatch", "category": "Electronics", "subcategory": "Wearables", "price": 6999, "rating": 4.4, "emoji": "⌚", "color": "cyan", "tags": ["fitness", "wearable", "tech", "daily"], "description": "Track your activity, stay connected, and keep your day moving."},
    {"id": 4, "name": "NovaBook Air", "category": "Electronics", "subcategory": "Laptops", "price": 64999, "rating": 4.6, "emoji": "💻", "color": "pink", "tags": ["laptop", "study", "work", "tech"], "description": "A lightweight laptop built for study sessions and creative work."},
    {"id": 5, "name": "CloudStep Sneakers", "category": "Fashion", "subcategory": "Shoes", "price": 2799, "rating": 4.5, "emoji": "👟", "color": "orange", "tags": ["shoes", "streetwear", "comfort", "fashion"], "description": "Everyday sneakers with a clean silhouette and cushioned feel."},
    {"id": 6, "name": "Metro Sling Bag", "category": "Fashion", "subcategory": "Bags", "price": 1499, "rating": 4.3, "emoji": "🎒", "color": "green", "tags": ["bag", "travel", "daily", "fashion"], "description": "A compact carry-all for campus, commutes, and quick trips."},
    {"id": 7, "name": "Essential Hoodie", "category": "Fashion", "subcategory": "Clothing", "price": 1899, "rating": 4.6, "emoji": "🧥", "color": "violet", "tags": ["clothing", "streetwear", "comfort", "fashion"], "description": "A soft, relaxed-fit layer for cool evenings and laid-back days."},
    {"id": 8, "name": "Sundaze Sunglasses", "category": "Fashion", "subcategory": "Accessories", "price": 999, "rating": 4.2, "emoji": "🕶️", "color": "yellow", "tags": ["accessories", "summer", "fashion", "travel"], "description": "Minimal sunglasses that finish off your everyday look."},
    {"id": 9, "name": "GlowDesk Lamp", "category": "Home", "subcategory": "Lighting", "price": 1299, "rating": 4.4, "emoji": "💡", "color": "yellow", "tags": ["home", "study", "desk", "lighting"], "description": "Warm adjustable light for focused work and cozy nights."},
    {"id": 10, "name": "CloudNine Cushion", "category": "Home", "subcategory": "Decor", "price": 799, "rating": 4.1, "emoji": "🛋️", "color": "pink", "tags": ["home", "decor", "comfort"], "description": "A soft accent cushion to add texture and comfort to your space."},
    {"id": 11, "name": "BrewBuddy Tumbler", "category": "Lifestyle", "subcategory": "Drinkware", "price": 699, "rating": 4.5, "emoji": "🥤", "color": "cyan", "tags": ["lifestyle", "travel", "daily", "drinkware"], "description": "A reusable tumbler made for busy days and on-the-go sips."},
    {"id": 12, "name": "FocusFlow Notebook", "category": "Lifestyle", "subcategory": "Stationery", "price": 349, "rating": 4.7, "emoji": "📓", "color": "green", "tags": ["study", "stationery", "daily", "lifestyle"], "description": "A simple, satisfying notebook for ideas, plans, and class notes."},
    {"id": 13, "name": "TrailBlaze Backpack", "category": "Fashion", "subcategory": "Bags", "price": 2299, "rating": 4.6, "emoji": "🎒", "color": "orange", "tags": ["bag", "travel", "study", "fashion"], "description": "Roomy, durable storage for campus essentials and weekend plans."},
    {"id": 14, "name": "GameGrid Controller", "category": "Electronics", "subcategory": "Gaming", "price": 3499, "rating": 4.5, "emoji": "🎮", "color": "blue", "tags": ["gaming", "tech", "wireless", "fun"], "description": "Responsive controls and comfortable grips for long gaming sessions."},
    {"id": 15, "name": "PureSip Bottle", "category": "Lifestyle", "subcategory": "Drinkware", "price": 499, "rating": 4.3, "emoji": "🧴", "color": "green", "tags": ["fitness", "travel", "daily", "lifestyle"], "description": "A reusable bottle to keep hydration close throughout the day."},
    {"id": 16, "name": "FramePop Wall Art", "category": "Home", "subcategory": "Decor", "price": 1599, "rating": 4.4, "emoji": "🖼️", "color": "pink", "tags": ["home", "decor", "design"], "description": "Bold, modern wall art to give your room a personal touch."},
]

CATEGORIES = ["All", "Electronics", "Fashion", "Home", "Lifestyle"]

def get_product(product_id):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)

def recommend_products(preferences, budget, category="All", exclude_id=None, limit=4):
    """Transparent rule-based recommender: tag overlap + rating + budget/category fit."""
    liked_tags = set(preferences)
    results = []
    for product in PRODUCTS:
        if exclude_id and product["id"] == exclude_id:
            continue
        if category != "All" and product["category"] != category:
            continue
        if product["price"] > budget:
            continue
        overlap = len(liked_tags.intersection(product["tags"]))
        score = overlap * 2 + product["rating"] / 5
        results.append((score, product))
    results.sort(key=lambda item: (item[0], item[1]["rating"], -item[1]["price"]), reverse=True)
    return [p for _, p in results[:limit]]

@app.context_processor
def inject_globals():
    return {"categories": CATEGORIES, "cart_count": len(session.get("cart", [])), "wishlist": session.get("wishlist", [])}

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.args.get("q", "").strip().lower()
    selected_category = request.args.get("category", "All")
    sort = request.args.get("sort", "featured")
    max_price = request.args.get("max_price", "70000")
    try:
        budget = max(0, int(max_price))
    except ValueError:
        budget = 70000

    products = [p for p in PRODUCTS if p["price"] <= budget]
    if selected_category != "All":
        products = [p for p in products if p["category"] == selected_category]
    if query:
        products = [p for p in products if query in p["name"].lower() or query in p["category"].lower() or query in p["subcategory"].lower() or any(query in t for t in p["tags"])]
    if sort == "price-low":
        products.sort(key=lambda p: p["price"])
    elif sort == "price-high":
        products.sort(key=lambda p: p["price"], reverse=True)
    elif sort == "rating":
        products.sort(key=lambda p: p["rating"], reverse=True)
    else:
        products.sort(key=lambda p: (p["rating"], -p["price"]), reverse=True)

    prefs = session.get("preferences", ["tech", "daily", "comfort"])
    recommendations = recommend_products(prefs, budget=70000, limit=4)
    if request.method == "POST":
        chosen = request.form.getlist("interests")
        if not chosen:
            chosen = ["daily"]
        session["preferences"] = chosen
        session["budget"] = int(request.form.get("rec_budget", 15000))
        return redirect(url_for("index", show_recs="1"))
    show_recs = request.args.get("show_recs") == "1"
    if show_recs:
        recommendations = recommend_products(prefs, session.get("budget", 15000), limit=6)
    return render_template("index.html", products=products, recommendations=recommendations,
                           query=query, selected_category=selected_category, sort=sort,
                           max_price=budget, preferences=prefs, show_recs=show_recs)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        return redirect(url_for("index"))
    related = recommend_products(product["tags"], 70000, product["category"], exclude_id=product_id, limit=3)
    return render_template("product.html", product=product, related=related)

@app.post("/wishlist/<int:product_id>")
def toggle_wishlist(product_id):
    if not get_product(product_id):
        return redirect(url_for("index"))
    wishlist = session.get("wishlist", [])
    if product_id in wishlist:
        wishlist.remove(product_id)
    else:
        wishlist.append(product_id)
    session["wishlist"] = wishlist
    return redirect(request.referrer or url_for("index"))

@app.post("/cart/<int:product_id>")
def add_to_cart(product_id):
    if get_product(product_id):
        cart = session.get("cart", [])
        cart.append(product_id)
        session["cart"] = cart
    return redirect(request.referrer or url_for("index"))

@app.route("/cart")
def cart():
    items = [get_product(pid) for pid in session.get("cart", [])]
    items = [p for p in items if p]
    total = sum(p["price"] for p in items)
    return render_template("cart.html", items=items, total=total)

@app.post("/cart/remove/<int:index>")
def remove_from_cart(index):
    cart_items = session.get("cart", [])
    if 0 <= index < len(cart_items):
        cart_items.pop(index)
        session["cart"] = cart_items
    return redirect(url_for("cart"))

if __name__ == "__main__":
    app.run(debug=True)
