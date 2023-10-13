import random
import pandas as pd
import tkinter as tk
from functools import partial
from tkinter import messagebox, Listbox
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification


def read_and_clean_csv(file_path):
    """
    Read a CSV file and clean its content.
    Args: The path to the CSV file.
    Returns: A cleaned dataframe.
    """
    df = pd.read_csv(file_path, sep=',')
    return df.replace(r"[^A-Za-z0-9 .,;!?()#$&%'´-]+", "", regex=True)


def on_search_retailer():
    """
    Handles the action when the "Search by Retailer" button is clicked.
    Fetches and displays offers related to the entered retailer.
    """
    retailer_name = search_text_entry.get().strip()
    retailer_name = retailer_name.upper()
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, f"{retailer_name}")
    if retailer_name:
        search_by_retailer(retailer_name)
    else:
        messagebox.showwarning("Warning", "Please enter a retailer name.")


def on_search_brand():
    """
    Handles the action when the "Search by Brand" button is clicked.
    Fetches and displays offers related to the entered brand.
    """
    brand_name = search_text_entry.get().strip()
    brand_name = brand_name.upper()
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, f"{brand_name}")
    if brand_name:
        search_by_brand(brand_name)
    else:
        messagebox.showwarning("Warning", "Please enter a brand name.")


def on_search_category():
    """
    Handles the action when the "Search by Category" button is clicked.
    Fetches and displays offers related to the entered product category.
    """
    category_name = search_text_entry.get().strip()
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, f"{category_name}")
    if category_name:
        search_by_category(category_name)
    else:
        messagebox.showwarning("Warning", "Please enter a category name.")


def search_by_retailer(retailer_name):
    """
    Searches for offers related to the provided retailer and updates the UI with results.
    Args: retailer_name (str): The name of the retailer to search offers for.
    """
    no_offers = 0
    results_offers.delete(0, tk.END)
    results_scores.delete(0, tk.END)
    if retailer_name not in offer_by_retailer:
        messagebox.showwarning("Warning", "No offers found for this retailer.")
        return
    for related_offer in offer_by_retailer.get(retailer_name, []):
        related_retailer = classifier(related_offer, retailer_name)
        if related_retailer['scores'][0] > 0.70:
            no_offers = 1
            results_offers.insert(tk.END, f"{related_offer}")
            results_scores.insert(tk.END, f"({round(related_retailer['scores'][0], 2)})")
    if no_offers == 0:
        results_offers.insert(tk.END, "No offers found for this retailer.")


def search_by_brand(brand_name):
    """
    Searches for offers related to the provided brand and updates the UI with results.
    Args: brand_name (str): The name of the brand to search offers for.
    """
    no_offers = 0
    results_offers.delete(0, tk.END)
    results_scores.delete(0, tk.END)
    if brand_name not in offer_by_brand:
        messagebox.showwarning("Warning", "No offers found for this brand.")
        return
    results_offers.delete(0, tk.END)
    results_scores.delete(0, tk.END)
    for related_offer in offer_by_brand[brand_name]:
        related_brand = classifier(related_offer, brand_name)
        if related_brand['scores'][0] > 0.65:
            no_offers = 1
            results_offers.insert(tk.END, f"{related_offer}")
            results_scores.insert(tk.END, f"({round(related_brand['scores'][0], 2)})")
    if no_offers == 0:
        results_offers.insert(tk.END, "No offers found for this brand.")


def search_by_category(category_name):
    """
    Searches for offers related to the provided product category and updates the UI with results.
    Args: category_name (str): The name of the product category to search offers for.
    """
    no_offers = 0
    results_offers.delete(0, tk.END)
    results_scores.delete(0, tk.END)
    if category_name not in brand_by_category:
        messagebox.showwarning("Warning", "No offers found for this category.")
        return
    brands_name = brand_by_category[category_name]
    temp_brand = []
    for brand_name in brands_name:
        if brand_name in offer_by_brand:
            temp_brand.extend(offer_by_brand[brand_name])
    for related_offer in temp_brand:
        related_category = classifier(related_offer, category_name)
        if related_category['scores'][0] > 0.6:
            no_offers = 1
            results_offers.insert(tk.END, f"{related_offer}")
            results_scores.insert(tk.END, f"({round(related_category['scores'][0], 2)})")
    if no_offers == 0:
        keys_with_value = [value for key, value in similar_categories.items() if category_name in value]
        results_offers.insert(tk.END, "No offers found for this category.", "Try with similar categories:", f"{', '.join(keys_with_value[0])}")


def random_search(list_uniq_elements, search_function):
    """
    Randomly selects an item from a list and displays it in the search box to perform a search using it.
    Args: list_uniq_elements (list): A list of unique items to choose from.
          search_function (function): The function to call with the randomly selected item.
    """
    search_text_entry.delete(0, tk.END)
    random_element = random.choice(list_uniq_elements)
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, f"{random_element}")
    search_function(random_element)


# ------------- Data Processing -------------

# Read and clean the dataset.
print('Loading...')
brand_categories = read_and_clean_csv('data/brand_category.csv')
categories = read_and_clean_csv('data/categories.csv')
offer_retailer = read_and_clean_csv('data/offer_retailer.csv')


# Create dictionaries for brands, categories, and offers.
offer_by_retailer = offer_retailer.groupby('RETAILER')['OFFER'].apply(list).to_dict()
offer_by_brand = offer_retailer.groupby('BRAND')['OFFER'].apply(list).to_dict()
brand_by_category = brand_categories.groupby('BRAND_BELONGS_TO_CATEGORY')['BRAND'].apply(list).to_dict()
similar_categories = categories.groupby('IS_CHILD_CATEGORY_TO')['PRODUCT_CATEGORY'].apply(list).to_dict()


# Create lists of all retailers, brands, and categories.
all_retailers = list(offer_by_retailer.keys())
all_brands = list(offer_by_brand.keys())
all_categories = list(brand_by_category.keys())


# Call a pre-trained model from Hugging Face library.
# Zero shot classification would work fine for this case (sentence classification) without finetunning.
classifier = pipeline('zero-shot-classification', model='roberta-large-mnli')


# ------------- GUI -------------

root = tk.Tk()
button_width = 18
small_button_width = 12
root.title("Search Offers")
root.geometry("800x600")


# -------------- Input Widgets --------------

# Text box for search
search_text_var = tk.StringVar()
search_text_label = tk.Label(root, text="Search for Offers! Type in a retailer, brand, or category.\nPress the 'Random' buttons to search for random offers!", font=('bold', 15))
search_text_label.pack(expand=True, pady=10)
search_text_entry = tk.Entry(root, textvariable=search_text_var)
search_text_entry.pack(expand=True, pady=10)
search_text_entry.focus()

# Create a frame for the Retailer button and its corresponding Random button
retailer_frame = tk.Frame(root)
retailer_frame.pack(pady=5)
retailer_button = tk.Button(retailer_frame, text="Search by retailer", command=partial(on_search_retailer), width=button_width)
retailer_button.pack(side=tk.LEFT)
# Retailer Random button
retailer_random_button = tk.Button(retailer_frame, text="Random Retailer", width=small_button_width, command=partial(random_search, all_retailers, search_by_retailer))
retailer_random_button.pack(side=tk.LEFT, padx=5)

# Create a frame for the Brand button and its corresponding Random button
brand_frame = tk.Frame(root)
brand_frame.pack(pady=5)
brand_button = tk.Button(brand_frame, text="Search by Brand", command=partial(on_search_brand), width=button_width)
brand_button.pack(side=tk.LEFT)
# Brand Random button
brand_random_button = tk.Button(brand_frame, text="Random Brand", width=small_button_width, command=partial(random_search, all_brands, search_by_brand))
brand_random_button.pack(side=tk.LEFT, padx=5)

# Create a frame for the Category button and its corresponding Random button
category_frame = tk.Frame(root)
category_frame.pack(pady=5)
category_button = tk.Button(category_frame, text="Search by Category", command=partial(on_search_category), width=button_width)
category_button.pack(side=tk.LEFT)
# Category Random button
category_random_button = tk.Button(category_frame, text="Random Category", width=small_button_width, command=partial(random_search, all_categories, search_by_category))
category_random_button.pack(side=tk.LEFT, padx=5)


# -------------- Output Widgets --------------

# Create a frame for the text widget
text_widget = tk.Text(root, width=30, height=2)
text_widget.pack(pady=5, padx=20)

# Create a frame for Offers
offers_frame = tk.Frame(root)
offers_frame.pack(pady=25, padx=10, side=tk.LEFT)

# Title for results_offers Listbox inside the offers frame
offers_title = tk.Label(offers_frame, text="OFFERS")
offers_title.pack(pady=(0, 25))

# Listbox widget to display offers results
results_offers = tk.Listbox(offers_frame, width=75, height=14)
results_offers.pack()

# Create a frame for Scores
scores_frame = tk.Frame(root)
scores_frame.pack(pady=25, padx=10, side=tk.RIGHT)

# Title for results_scores Listbox inside the scores frame
scores_title = tk.Label(scores_frame, text="SCORE")
scores_title.pack(pady=(0, 25))

# Listbox widget to display scores results
results_scores = tk.Listbox(scores_frame, width=7, height=14, justify='center')
results_scores.pack()


root.mainloop()
