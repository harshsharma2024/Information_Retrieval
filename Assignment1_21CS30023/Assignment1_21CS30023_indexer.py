import sys
import spacy
import pickle
nlp = spacy.load("en_core_web_sm")  # Load the English NLP model


def create_document_list(document_file , document_list):

    file = document_file
    current_document = {}  # Initialize an empty dictionary for the current document
    current_field = None  # Initialize a variable to keep track of the current field
    for line in file:           # Strip whitespace from the beginning and end of each line
        line = line.strip()
        if line.startswith(".I"):       # Found a new document ID
            if current_document:        # If there was a previous document, add it to the list
                document_list.append(current_document)
            
            current_document = {}       # Reset the dictionary for the new query
            docID = line[3:].strip()
            current_document["Document ID"] = int(docID)  # Convert to integer
            current_field = None  # Reset the current field
        elif line.startswith(".T"):
            current_field = "Document Title"
            # current_document[current_field] = []  # Initialize a list for multi-line data
        elif line.startswith(".A"):
            current_field = "Author"
            # current_document[current_field] = []  # Initialize a list for multi-line data
        elif line.startswith(".B"):
            current_field = "Source Location"
            # current_document[current_field] = []  # Initialize a list for multi-line data
        elif line.startswith(".W"):
            current_field = "Text"
            current_document[current_field] = []  # Initialize a list for multi-line data
        elif current_field is not None:
            if current_field == "Text":
                current_document[current_field].append(line)    # Append the line to the current field's list
    # Append the last document to the list
    if current_document:
        document_list.append(current_document)


    # Joining Multi-Line Data
    for document in document_list:
        document["Text"] = " ".join(document["Text"]) # Join multi-line data

    return document_list


def preprocessing_document_list(document_list):
    for document in document_list:
        Temp = []
        doc = nlp(document["Text"])         # tokenize 

        for token in doc:
            if(not token.is_stop and not token.is_punct and token.is_alpha):        # Ignoring Puctuators and Stop Words
                word = token.lemma_.lower()         # Lower Case
                Temp.append(word)             
        document["Text"] = Temp

    return document_list


def make_tokens_unique(document_list):          #Unique Tokens
    for document in document_list:
        unique_terms = []
        seen = set()

        for term in document["Text"]:
            if term not in seen:
                unique_terms.append(term)
                seen.add(term)

        document["Text"] = unique_terms

    return document_list

# Creating Postings List
def Postings_list_document(document_list,postings_list):
    for document in document_list:
        for word in document["Text"]:
            if word not in postings_list:
                postings_list[word] = []
            if document["Document ID"] not in postings_list[word]:
                postings_list[word].append(document["Document ID"])

    return postings_list

def print_postings_list(postings_list):
    with open("model_queries_21CS30023.bin", 'wb') as file:
        pickle.dump(postings_list,file)


def main():
    if(len(sys.argv) != 2):
        print("ERROR : python3 Assignment1_21CS30023_indexer.py <path to cran file >  [Either Excess or No arguments]")
        sys.exit(1)

    cran_folder = sys.argv[1]

    try :
        document_file = open(cran_folder, "r")
    except:
        print("ERROR CAUSED DURING FILE LOADING")
        sys.exit(1)

    document_list = []
    document_list = create_document_list(document_file,document_list)


    document_list = preprocessing_document_list(document_list)
    document_list = make_tokens_unique(document_list)
    postings_list_document = {}
    postings_list_document = Postings_list_document(document_list,postings_list_document)
    print_postings_list(postings_list_document)

if __name__ == "__main__":
    main()
