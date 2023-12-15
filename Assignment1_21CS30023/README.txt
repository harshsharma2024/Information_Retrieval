************Inverted Index, Boolean Document Retrieval************


Introduction:

This document provides insights of my Assignment, which revolves around implementing an
advanced Boolean retrieval system.


Contents:

• I. Requirements
• II. Design Specifications
• III. Limitations



I. Requirements

Environment

To run this project, ensure the following:

• Python: Version 3.10.12 was used.

• Libraries:
– spaCy: Version 3.6.1 for advanced text processing.
– pickle: For serializing and deserializing Python objects.

• spaCy Model:Install Spacy and Load the English language model using:

pip install spacy
python3 -m spacy download en_core_web_sm

II. Design Specifications

Dataset
The project processes a collection of text documents:
• Total documents: 1400
• Unique terms (after preprocessing): 5195

Queries
The Project had queries that needs to processed and relevant documents needed to shown
• Total queries: 225


Text Preprocessing:

The text preprocessing pipeline includes:
• Tokenization: Dividing cleaned text into individual words (tokens).
• Stopword/ Punctuators Removal: Eliminating common stopwords/Punctuators.
• Normalization: Lowercasing, removing special characters, and numbers.
• Lemmatization: Converting tokens into base forms using spaCy library.
• Unique Tokens: Removing repetitive tokens

Input Data => tokenization  => Remove Stopwords, Punctuators => Normalization => Lemmatization => Unique Tokens =>Preprocessed Data


Inverted Index ( Assignment1 21CS30023 indexer.py)
The Indexer component creates an inverted index:
• Documents Input: Set of Documents.
• Document Processing: Using the mechanism explained above and storing in Inverted Index.
• Total terms in the inverted index: 5195
• Structure: TokenName : [ List of Documents]

Parser (Assignment1 21CS30023 parser.py)
The Parse component handles query processing :
• Query Input: Set of queries.
• Query Processing: Using the mechanism explained above.
• Stores Query Output with QueryID and related terms

Project Output (Assignment1 21CS30023 bool.py)
Upon completion, the project generates:
• Results file: Contains relevant document IDs for each query.
• Document Retrieval: Retrieving relevant documents for each query.
• Output: Results saved in an output file with document IDs for each query.



III. LIMITATIONS

Limited Complex Queries
The system is designed for basic Boolean queries using AND. It does not support more
advanced query types such as phrase queries or proximity searches.

Lack of Relevance Ranking
Boolean retrieval systems do not rank documents by relevance. They treat all documents
that match a query equally, which can be a limitation when users are looking for the most
relevant information.

Scalability Issues
The system’s performance may degrade when dealing with a very large document collec-
tion. Boolean operations on extensive document sets can be computationally expensive.

Exact Match Requirement
Boolean queries require an exact match of terms. This means that documents containing
synonyms or related terms may not be retrieved unless those terms are explicitly included
in the query