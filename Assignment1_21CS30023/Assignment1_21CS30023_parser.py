import sys
import spacy
# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# To craete a query list
def create_query_list(query_file, query_list):

    current_query = {}  # Initialize an empty dictionary for the current query
    current_field = None  # Initialize a variable to keep track of the current field

    for line in query_file:
        # Strip whitespace from the beginning and end of each line
        line = line.strip()

        if line.startswith(".I"):       # Found a new query ID
            if current_query:           # If there was a previous query, add it to the list
                query_list.append(current_query)
                
            current_query = {}  # Reset the dictionary for the new query
            queryID = line[3:].strip()
            current_query["Query ID"] = int(queryID)  # Convert to integer
            current_field = None  # Reset the current field
        elif line.startswith(".W"):
            current_field = "Text"
            current_query[current_field] = []  # Initialize a list for multi-line data
        elif current_field is not None:
            # Append the line to the current field's list
            current_query[current_field].append(line)

    # Append the last query to the list
    if current_query:
        query_list.append(current_query)

    for query in query_list:
        query["Text"] = " ".join(query["Text"])  # Join multi-line data

    return query_list


def preprocessing_document_list(document_list):
    for document in document_list:
        Temp = []
        doc = nlp(document["Text"])         # Tokenize

        for token in doc:
            if(not token.is_stop and not token.is_punct and token.is_alpha):        # Removing Stop words , Punctuators
                word = token.lemma_.lower()
                Temp.append(word)
        document["Text"] = Temp

    return document_list


def make_tokens_unique(document_list):      # Unique Tokens
    for document in document_list:
        unique_terms = []
        seen = set()

        for term in document["Text"]:
            if term not in seen:
                unique_terms.append(term)
                seen.add(term)

        document["Text"] = unique_terms

    return document_list

def print_query_postings_list(postings_list):
    with open('queries_21CS30023.txt', 'w') as file:

        for query in postings_list:
            query["Text"] = " ".join(query["Text"])
            file.write(str(query["Query ID"]) + "   ")
            file.write(str(query["Text"]))
            file.write("\n")


def main():
    if(len(sys.argv) != 2):
        print("ERROR : python3 Assignment1_21CS30023_bool.py [Either Excess or No arguments]")
        sys.exit(1)

    query_file = sys.argv[1]

    try:
        query_file = open(query_file, "r")
    except:
        print("ERROR IN LOADING CRAN.QUERY")
        sys.exit(1)

    query_list = []
    query_list = create_query_list(query_file,query_list)
    query_list = preprocessing_document_list(query_list)
    query_list = make_tokens_unique(query_list)
    print_query_postings_list(query_list)


if __name__ == "__main__":
    main()