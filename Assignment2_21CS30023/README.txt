Roll No.: 21CS30023
Name: Harsh Sharma
Assignment 2
Information Retrieval

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

Also need to import -numpy
                    -sys
                    -math

II.
Running the code :

Assignment2_21CS30023_ranker.py

    1. To run the code, open the terminal and go to the directory where the code is present.
    2. Run the following command -
        python Assignment2_21CS30023_ranker.py <path to the CRAN folder> <path to model queries file>
        python3 Assignment2_21CS30023_ranker.py cran_folder/ model_queries_21CS30023.bin 
    3. The code will run and create three ranked list files in the same directory as the code.
        a. Assignment2_21CS30023_ranked_list_A.txt : Scoring based on lnc.ltc
        b. Assignment2_21CS30023_ranked_list_B.txt : Scoring based on lnc.Ltc
        c. Assignment2_21CS30023_ranked_list_C.txt : Scoring based on anc.apc


Assignment2_21CS30023_evaluator.py
    1. Now run the following command -
        python Assignment2_21CS30023_evaluator.py <path to the golden standard> <path to the result file>
        python3 Assignment2_21CS30023_evaluator.py cranqrel Assignment2_21CS30023_ranked_list_B.txt 

    2. The code will generate the file according to the result file name and print the following metrics:
        1. For each query:
            a. Average Precision@10 , Average Precision@20 for each query
            b. NDCG@10 , NDCG@20 for each query

        2. Mean Average Precision@10 , Mean Average Precision@20
        3. Mean NDCG@10 , Mean NDCG@20

IV.
Functionalities:

Assignment2_21CS30023_ranker.py


    ### `preprocessing_string(str_for_preprocessing)`

    - Input: `str_for_preprocessing` - The input string to be preprocessed.
    - Output: Returns a preprocessed string after tokenization, lemmatization, and removal of stop words and punctuation.

    ### `termfrequency_data(data)`

    - Input: `data` - The raw data containing document information.
    - Output: Returns a dictionary (`TF_Dict`) containing term frequencies for each document.

    ### `Query_Generator(data)`

    - Input: `data` - The raw data containing query information.
    - Output: Returns a dictionary (`query`) containing preprocessed queries.

    ### `Doc_Frequency(TF_Dict)`

    - Input: `TF_Dict` - The dictionary containing term frequencies for documents.
    - Output: Returns a dictionary (`Dict`) containing document frequencies for each term.

    ### `lnc_Normalize(TF_Dict)`

    - Input: `TF_Dict` - The dictionary containing term frequencies for a document.
    - Output: Returns the lnc normalization factor for a document.

    ### `ltc_Normalize(Query_TF_Dict, DF_Dict, Total_Documents)`

    - Input:
      - `Query_TF_Dict` - The dictionary containing term frequencies for a query.
      - `DF_Dict` - The dictionary containing document frequencies.
      - `Total_Documents` - Total number of documents.
    - Output: Returns the ltc normalization factor for a query.

    ### `Ltc_Normalize(Query_TF_Dict, DF_Dict, Total_Documents)`

    - Input:
      - `Query_TF_Dict` - The dictionary containing term frequencies for a query.
      - `DF_Dict` - The dictionary containing document frequencies.
      - `Total_Documents` - Total number of documents.
    - Output: Returns both the ltc normalization factor and denominator for a query.

    ### `lnc_ltc(TF_Dict, DF_Dict, Query_Dict, Total_Documents)`

    - Input:
      - `TF_Dict` - Dictionary of term frequencies for documents.
      - `DF_Dict` - Dictionary of document frequencies.
      - `Query_Dict` - Dictionary of preprocessed queries.
      - `Total_Documents` - Total number of documents.
    - Output: Returns a dictionary (`TF_IDF_Dict`) containing TF-IDF scores for each query and document pair using lnc-ltc weighting.

    ### `lnc_Ltc(TF_Dict, DF_Dict, Query_Dict, Total_Documents)`

    - Input:
      - `TF_Dict` - Dictionary of term frequencies for documents.
      - `DF_Dict` - Dictionary of document frequencies.
      - `Query_Dict` - Dictionary of preprocessed queries.
      - `Total_Documents` - Total number of documents.
    - Output: Returns a dictionary (`lnc_Ltc_dict`) containing TF-IDF scores for each query and document pair using lnc-Ltc weighting.

    ### `anc_Normalize(TF_Dict)`

    - Input: `TF_Dict` - The dictionary containing term frequencies for a document.
    - Output: Returns both the anc normalization factor and maximum term frequency for a document.

    ### `apc_Normalize(Query_TF_Dict, DF_Dict, Total_Documents)`

    - Input:
      - `Query_TF_Dict` - The dictionary containing term frequencies for a query.
      - `DF_Dict` - The dictionary containing document frequencies.
      - `Total_Documents` - Total number of documents.
    - Output: Returns both the apc normalization factor and maximum term frequency for a query.

    ### `anc_apc(TF_Dict, DF_Dict, Query_Dict, Total_Documents)`

    - Input:
      - `TF_Dict` - Dictionary of term frequencies for documents.
      - `DF_Dict` - Dictionary of document frequencies.
      - `Query_Dict` - Dictionary of preprocessed queries.
      - `Total_Documents` - Total number of documents.
    - Output: Returns a dictionary (`anc_apc_dict`) containing TF-IDF scores for each query and document pair using anc-apc weighting.


Assignment2_21CS30023_evaluator.py

    ### `Proces_Gold_Standard(data, mappingQID)`

    - Input: 
      - `data` - The raw data from the gold standard file.
      - `mappingQID` - A mapping of cranqrel query ID and RankedList query ID.
    - Output: Returns a dictionary (`Dict`) containing relevance scores for each query and document pair.

    ### `Proces_Ranked_Data(data)`

    - Input: `data` - The raw data from the ranked list file.
    - Output: Returns a dictionary (`Dict`) containing the top 20 ranked documents for each query.

    ### `mappingQIDs(data, A_Ranked_List)`

    - Input: 
      - `data` - The raw data from the gold standard file.
      - `A_Ranked_List` - The dictionary containing the top 20 ranked documents for each query.
    - Output: Returns a mapping of cranqrel query ID and RankedList query ID.

    ### `Precision(A_Ranked_List, Gold_Standard, file)`

    - Input:
      - `A_Ranked_List` - The dictionary containing the top 20 ranked documents for each query.
      - `Gold_Standard` - The dictionary containing relevance scores for each query and document pair.
      - `file` - The file object for writing the results.
    - Output: Calculates and writes Average Precision at 10 and 20, and NDCG at 10 and 20 for each query to the specified file.


V. Data Preprocessing

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