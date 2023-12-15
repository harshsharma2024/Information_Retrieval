# Roll No.: 21CS30023
# Name: Harsh Sharma
# IR Assignment 2


import sys
import spacy
import pickle
nlp = spacy.load("en_core_web_sm")  # Load the English NLP model
import numpy as np
import math

# For Preprocessing String
def preprocessing_string(str_for_preprocessing):
    Temp = ""
    doc = nlp(str_for_preprocessing)         # tokenize 
    for token in doc:
        if(not token.is_stop and not token.is_punct and token.is_alpha):        # Ignoring Puctuators and Stop Words
            word = token.lemma_.lower()         # Lower Case
            Temp += word + " "             

    return Temp


# For Calculating Term Frequency
def termfrequency_data(data):
    # Initialize an empty dictionary to store dictionary for each term document which wouls store terms and frequency to maintain all the documents
    TF_Dict = {}
    # Initialize an dictionary for eacd document which would store terms and frequency for each document
    doc_dict = {}
    doc_id = None
    temp_string_for_Pre_Process = ""
    for line in data.splitlines():
        if line.startswith(".I"):
            if(doc_id != None):
                temp_string_for_Pre_Process = preprocessing_string(temp_string_for_Pre_Process)
                # print(temp_string_for_Pre_Process)
                for word in temp_string_for_Pre_Process.split():
                    if(word not in doc_dict):
                        doc_dict[word] = 1
                    else:
                        doc_dict[word] += 1

                TF_Dict[doc_id] = doc_dict
                # print(TF_Dict[doc_id])
            doc_id = line.split()[1]
            current_field = None
            temp_string_for_Pre_Process = ""
        elif line.startswith(".W"):
            doc_dict = {}
            current_field = "Text"
        elif line.startswith(".T"):
            current_field = "Document Title"
        elif line.startswith(".A"):
            current_field = "Author"
        elif line.startswith(".B"):
            current_field = "Source Location"
        else:
            if(current_field == "Text"):
                for word in line.split():
                    temp_string_for_Pre_Process += word + " "

    if(doc_id != None):
                temp_string_for_Pre_Process = preprocessing_string(temp_string_for_Pre_Process)
                # print(temp_string_for_Pre_Process)
                for word in temp_string_for_Pre_Process.split():
                    if(word not in doc_dict):
                        doc_dict[word] = 1
                    else:
                        doc_dict[word] += 1

                TF_Dict[doc_id] = doc_dict

    return TF_Dict


# For Query Extraction and Preprocessing
def Query_Generator(data):
    query= {}
    query_id = None
    temp_string_for_Pre_Process = ""
    for line in data.splitlines():
        if line.startswith(".I"):
            if(query_id != None):
                temp_string_for_Pre_Process = preprocessing_string(temp_string_for_Pre_Process)
                # print(temp_string_for_Pre_Process)
                query[query_id] = temp_string_for_Pre_Process
            query_id = line.split()[1]
            current_field = None
            temp_string_for_Pre_Process = ""
        elif line.startswith(".W"):
            current_field = "Text"
        elif line.startswith(".T"):
            current_field = "Document Title"
        elif line.startswith(".A"):
            current_field = "Author"
        elif line.startswith(".B"):
            current_field = "Source Location"
        else:
            if(current_field == "Text"):
                for word in line.split():
                    temp_string_for_Pre_Process += word + " "

    if(query_id != None):
        temp_string_for_Pre_Process = preprocessing_string(temp_string_for_Pre_Process)
        # print(temp_string_for_Pre_Process)
        query[query_id] = temp_string_for_Pre_Process

    return query



def Doc_Frequency(TF_Dict):         # Calculating Document Frequency
    Dict = {}
    for index in TF_Dict:
        Dict[index] = len(TF_Dict[index])

    return Dict


# For Calculating ltc Normalization Factor
def ltc_Normalize(Query_TF_Dict ,DF_Dict , Total_Documents):
        sum = 0
        for word in Query_TF_Dict:
            if(word not in DF_Dict):
                continue
            p = (1 + math.log10(Query_TF_Dict[word])) * (math.log10(Total_Documents/DF_Dict[word]))
            sum += p*p
        sum = math.sqrt(sum)

        return sum


# For Calculating lnc Normalization Factor
def lnc_Normalize(TF_Dict):
    sum = 0
    for word in TF_Dict:
        sum += (1 + math.log10(TF_Dict[word])) * (1 + math.log10(TF_Dict[word]))
    sum = math.sqrt(sum)    
    return sum


# For Calculating Ltc Normalization Factor
def Ltc_Normalize(Query_TF_Dict , DF_Dict , Total_Documents):
    denominator = 0
    for word in Query_TF_Dict:
        denominator += Query_TF_Dict[word]

    denominator = 1 + math.log10((denominator)/len(Query_TF_Dict))

    sum = 0

    for word in Query_TF_Dict:
            if(word not in DF_Dict):
                continue
            p = (1 + math.log10(Query_TF_Dict[word])) * (math.log10(Total_Documents/DF_Dict[word]))/denominator

            sum += p*p

    sum = math.sqrt(sum)
    return sum,denominator


# For Calculating lnc_ltc TF-IDF
def lnc_ltc(TF_Dict, DF_Dict, Query_Dict,Total_Documents):
    TF_IDF_Dict = {}
    for query_id in Query_Dict:
        TF_IDF_Dict[query_id] = {}
        Query_TF_Dict = {}
        for word in Query_Dict[query_id].split():
            if(word not in Query_TF_Dict):
                Query_TF_Dict[word] = 1
            else:
                Query_TF_Dict[word] += 1
        #finding Normalization Factor for Query
        sum = ltc_Normalize(Query_TF_Dict , DF_Dict , Total_Documents)
        for Doc in TF_Dict:
            TF_IDF_Dict[query_id][Doc] = 0 
            Doc_lst = []
            Query_lst = []

            for word in Query_Dict[query_id].split():
                if(word in TF_Dict[Doc] and word in DF_Dict):
                    Doc_lst.append(1 + math.log10(TF_Dict[Doc][word])) # Document Term Frequency * 1
                    Query_lst.append((1 + math.log10(Query_TF_Dict[word])) * math.log10(Total_Documents/DF_Dict[word]))                  # Query Term Frequency * log(Total Docs/Doc Frequency)
            if(len(Doc_lst) == 0 or len(Query_lst) == 0):
                continue
            Doc_Norm_factor = lnc_Normalize(TF_Dict[Doc])
            Doc_vctr = np.array(Doc_lst)
            Query_vctr = np.array(Query_lst)
            #Normalize the vectors
            Doc_vctr = Doc_vctr/Doc_Norm_factor #TODO
            Query_vctr = Query_vctr/sum #TODO
            # Taking Dot Product
            TF_IDF_Dict[query_id][Doc] = np.dot(Doc_vctr,Query_vctr)
        
        # Sorting the Dictionary and taking top 50
        TF_IDF_Dict[query_id] = dict(sorted(TF_IDF_Dict[query_id].items(), key=lambda item: item[1], reverse = True)[:50])


    return TF_IDF_Dict
    
# For Calculating lnc_Ltc TF-IDF
def lnc_Ltc(TF_Dict, DF_Dict, Query_Dict,Total_Documents):
    TF_IDF_Dict = {}
    for query_id in Query_Dict:
        TF_IDF_Dict[query_id] = {}
        Query_TF_Dict = {}
        for word in Query_Dict[query_id].split():
            if(word not in Query_TF_Dict):
                Query_TF_Dict[word] = 1
            else:
                Query_TF_Dict[word] += 1
        #finding Normalization Factor for Query
        sum_ = Ltc_Normalize(Query_TF_Dict , DF_Dict , Total_Documents)
        sum = sum_[0]
        denominator = sum_[1]
        # print(sum)

        for Doc in TF_Dict:
            TF_IDF_Dict[query_id][Doc] = 0 
            Doc_lst = []
            Query_lst = []

            for word in Query_Dict[query_id].split():
                if(word in TF_Dict[Doc] and word in DF_Dict):
                    Doc_lst.append(1 + math.log10(TF_Dict[Doc][word])) # Document Term Frequency * 1
                    Query_lst.append((1 + math.log10(Query_TF_Dict[word])) * (math.log10(Total_Documents/DF_Dict[word]))/denominator)                  # Query Term Frequency * log(Total Docs/Doc Frequency)
            if(len(Doc_lst) == 0 or len(Query_lst) == 0):
                continue
            Doc_Norm_factor = lnc_Normalize(TF_Dict[Doc])
            Doc_vctr = np.array(Doc_lst)
            Query_vctr = np.array(Query_lst)
            #Normalize the vectors
            Doc_vctr = Doc_vctr/Doc_Norm_factor #TODO
            Query_vctr = Query_vctr/sum #TODO
            # Taking Dot Product
            TF_IDF_Dict[query_id][Doc] = np.dot(Doc_vctr,Query_vctr)
        
        # Sorting the Dictionary and taking top 50
        TF_IDF_Dict[query_id] = dict(sorted(TF_IDF_Dict[query_id].items(), key=lambda item: item[1], reverse = True)[:50])


    return TF_IDF_Dict


# For Calculating apc Normalization Factor
def apc_Normalize(Query_TF_Dict ,DF_Dict , Total_Documents):
    max_freq = 0
    for word in Query_TF_Dict:
        if(Query_TF_Dict[word] > max_freq):
            max_freq = Query_TF_Dict[word]

    sum = 0
    for word in Query_TF_Dict:
        if(word not in DF_Dict):
            continue
        p = (0.5 + 0.5 * Query_TF_Dict[word]/max_freq) * max(0 , math.log10((Total_Documents - DF_Dict[word])/DF_Dict[word]))
        sum += p*p
    return math.sqrt(sum),max_freq


# For Calculating anc Normalization Factor
def anc_Normalize(TF_Dict):
    max_freq = 0
    for word in TF_Dict:
        if(TF_Dict[word] > max_freq):
            max_freq = TF_Dict[word]
    
    sum = 0
    for word in TF_Dict:
        p = (0.5 + 0.5 * TF_Dict[word]/max_freq)
        sum += p*p

    return math.sqrt(sum),max_freq


# For Calculating anc_apc TF-IDF
def anc_apc(TF_Dict, DF_Dict, Query_Dict,Total_Documents):
    TF_IDF_Dict = {}
    for query_id in Query_Dict:
        TF_IDF_Dict[query_id] = {}
        Query_TF_Dict = {}
        for word in Query_Dict[query_id].split():
            if(word not in Query_TF_Dict):
                Query_TF_Dict[word] = 1
            else:
                Query_TF_Dict[word] += 1
        #finding Normalization Factor for Query
        apc_norm_query = apc_Normalize(Query_TF_Dict , DF_Dict , Total_Documents)
        sum = apc_norm_query[0]
        dr_query = apc_norm_query[1]
        # print(sum)

        for Doc in TF_Dict:
            TF_IDF_Dict[query_id][Doc] = 0 
            Doc_lst = []
            Query_lst = []

            anc_Norm_factor = anc_Normalize(TF_Dict[Doc])
            Doc_Norm_factor = anc_Norm_factor[0]
            dr_doc = anc_Norm_factor[1]
            for word in Query_Dict[query_id].split():
                if(word in TF_Dict[Doc] and word in DF_Dict):
                    Doc_lst.append(0.5 + (0.5*(TF_Dict[Doc][word])/dr_doc)) 
                    Query_lst.append((0.5 + (0.5*Query_TF_Dict[word]/dr_query)) * max(0 , math.log10((Total_Documents - DF_Dict[word])/DF_Dict[word])))                # Query Term Frequency * log(Total Docs/Doc Frequency)
            if(len(Doc_lst) == 0 or len(Query_lst) == 0):
                continue

            #  DOT PRODUCT
            Doc_vctr = np.array(Doc_lst)
            Query_vctr = np.array(Query_lst)
            #Normalize the vectors
            Doc_vctr = Doc_vctr/Doc_Norm_factor #TODO
            Query_vctr = Query_vctr/sum #TODO
            # Taking Dot Product
            TF_IDF_Dict[query_id][Doc] = np.dot(Doc_vctr,Query_vctr)
        
        # Sorting the Dictionary and taking top 50
        TF_IDF_Dict[query_id] = dict(sorted(TF_IDF_Dict[query_id].items(), key=lambda item: item[1], reverse = True)[:50])


    return TF_IDF_Dict

def main():

    # TERM FREQUENCY

    if(len(sys.argv) != 3):
        print("Either too many or too few arguments are passed")
        sys.exit(1)

    # Reading the file and storing it in data

    documents_file = (f'{sys.argv[1]}/cran.all.1400')
    queries_file = (f'{sys.argv[1]}/cran.qry')
    try:
        data = open(documents_file,'r').read()
    except:
        print("ERROR : Unable to open file")
        sys.exit(1)

    #reading cran.all.1400 file
    
    TF_Dict = termfrequency_data(data)
    Total_Documents = len(TF_Dict)

    # DOCUMENT FREQUENCY

    model_queries = sys.argv[2]


    # with open('model_queries_21CS30023.bin','rb') as file:
    try:
        file = open(model_queries,'rb')
        DF_Dict = pickle.load(file)
    except:
        print("ERROR : Unable to open file")
        sys.exit(1)

    DF_Dict = Doc_Frequency(DF_Dict)

    # For Query Extraction and Preprocessing
    try:
        with open(queries_file, 'r') as file:
            data = file.read()
    except:
        print("ERROR : Unable to open file")
        sys.exit(1)


    Query_Dict = {}
    Query_Dict = Query_Generator(data)


    # Calculating TF-IDF
    TF_IDF_Dict = {}

    TF_IDF_Dict = lnc_ltc(TF_Dict, DF_Dict, Query_Dict,Total_Documents)
    
    with open('Assignment2_21CS30023_ranked_list_A.txt','w') as file:
        for query_id in TF_IDF_Dict:
            file.write(query_id +" : ")
            for Doc in TF_IDF_Dict[query_id]:
                file.write(Doc + " ")
            file.write("\n")
                
    lnc_Ltc_dict = {}

    lnc_Ltc_dict = lnc_Ltc(TF_Dict, DF_Dict, Query_Dict,Total_Documents)
    
    with open('Assignment2_21CS30023_ranked_list_B.txt','w') as file:
        for query_id in lnc_Ltc_dict:
            file.write(query_id +" : ")
            for Doc in lnc_Ltc_dict[query_id]:
                file.write(Doc + " ")
            file.write("\n")

    anc_apc_dict = {}

    anc_apc_dict = anc_apc(TF_Dict, DF_Dict, Query_Dict,Total_Documents)
    
    with open('Assignment2_21CS30023_ranked_list_C.txt','w') as file:
        for query_id in anc_apc_dict:
            file.write(query_id +" : ")
            for Doc in anc_apc_dict[query_id]:
                file.write(Doc + " ")
            file.write("\n")


if __name__ == "__main__":
    main()