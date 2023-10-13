# Fetch: Search for Offers 

### Task: build a tool that allows users to intelligently search for offers via text input from the user.

You will be provided with a dataset of offers and some associated metadata around the retailers and brands that are sponsoring the offer. You will also be provided with a dataset of some brands that we support on our platform and the categories that those products belong to.

**Acceptance Criteria:**
- If a user searches for a category (ex. diapers) the tool should return a list of offers that are relevant to that category.
- If a user searches for a brand (ex. Huggies) the tool should return a list of offers that are relevant to that brand.
- If a user searches for a retailer (ex. Target) the tool should return a list of offers that are relevant to that retailer.
- The tool should also return the score that was used to measure the similarity of the text input with each offer

## My Approach:

#### Data Cleaning and Pre-processing:

I cleaned the data from the CSV files by removing special characters and converting words in all-uppercase to lowercase. Offers with numerous uppercase words and special characters consistently received the lowest scores.
```
sequence: Starry lemon lime soda, 7.5-ounce 10 pack, at amazon storefront
labels: ['Starry']
scores: [0.96726]
```
```
sequence: Starry™ Lemon Lime Soda, 7.5-ounce 10 pack, at Amazon Storefront
labels: ['STARRY']
scores: [0.92603]
```
I constructed dictionaries to correlate offers with their corresponding retailers and brands. Subsequently, brands tied to a specific product category were grouped together in a separate dictionary. This strategy enabled the efficient utilization of the NLP model on potentially related sentence pairs. For instance, assessing whether the offer "L’Oréal Paris Men Expert hair color, priced at $9 at Walmart" pertains to the "Frozen Fruits" category would be inefficient, given the evident lack of association between the two in terms of brands and product categories.

#### NLP Model:

I treated the problem as a sentence pair classification task. Therefore, a pre-trained MultiNLP model seemed like a good option. In this strategy, the model computes a score reflecting the relationship between a premise (offer) and a hypothesis (category/brand/retailer). I used the ```transformers``` Hugging Face library to implement a zero-shot classification model that measures the relevance between offers and user queries (categories, brands, or retailers) employing the pre-trained model ```roberta-large-mnli```. 

#### GUI:

I built a simple GUI using the tkinter library, featuring an entry widget for user search queries. To submit their search, users can choose from three buttons: 'Search by Retailer', 'Search by Brand', or 'Search by Category'. For a more spontaneous approach, I've also integrated three 'Random' buttons to retrieve random offers related to either retailers, brands, or categories. After executing a search, results appear in a Listbox widget, accompanied by their scores.

#### Assumptions and tradeoffs:

The threshold value for an offer to be deemed relevant to a category, retailer, or brand is set at 0.60. While this might result in more non-related offers, it's a more cautious choice than raising the threshold and potentially overlooking pertinent offers. Although the pre-trained model can perform multi-label classification—which would allow an offer to be linked to multiple product categories simultaneously—this method proved too computationally intensive and time-consuming, so it was not adopted.

## Run it locally:
Python version = 3.11.5 
Download the repository and install the required packages
```
pip install -r requirements.txt
```
Run the following script from the main dir (SearchOffersFetch-main):
```
python bin/FetchTaskNLP.py
```
An interactive window will show up on the screen.

# Video Demonstration:
[![Video Demo](http://img.youtube.com/vi/SJFtMZTk7Mk/0.jpg)](http://www.youtube.com/watch?v=SJFtMZTk7Mk)
