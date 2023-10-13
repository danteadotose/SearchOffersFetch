# Fetch: Search for Offers 

### Task: build a tool that allows users to intelligently search for offers via text input from the user.

You will be provided with a dataset of offers and some associated metadata around the retailers and brands that are sponsoring the offer. You will also be provided with a dataset of some brands that we support on our platform, and the categories that those products belong to.

**Acceptance Criteria:**
- If a user searches for a category (ex. diapers) the tool should return a list of offers that are relevant to that category.
- If a user searches for a brand (ex. Huggies) the tool should return a list of offers that are relevant to that brand.
- If a user searches for a retailer (ex. Target) the tool should return a list of offers that are relevant to that retailer.
- The tool should also return the score that was used to measure the similarity of the text input with each offer

## My Approach:

## Run it locally:
Python version = 3.11.5 
Download the repository and install the required packages
```
python -m venv FetchNLP
source FetchNLP/bin/activate
pip install -r requirements.txt
```
Run the following script from the main dir (FetchNLP):
```
python bin/FetchTaskNLP.py
```
An interactive window will show up on the screen.

# Video Demonstration:
[![Video Demo](http://img.youtube.com/vi/SJFtMZTk7Mk/0.jpg)](http://www.youtube.com/watch?v=SJFtMZTk7Mk)
