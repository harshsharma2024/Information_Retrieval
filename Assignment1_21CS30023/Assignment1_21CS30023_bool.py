import sys
import pickle
def merge_AND_two_list(list1 , list2):
    result = []
    i = 0
    j = 0
    while(i < len(list1) and j < len(list2)):
        if((list1[i]) == (list2[j])):
            result.append(list1[i])
            i = i + 1
            j = j + 1
        elif(list1[i] < list2[j]):
            i = i + 1
        else:
            j = j + 1
    return result


def Merge(query_file , inverted_index):
    with open('Assignment1_21CS30023_results.txt', 'w') as file:            # Creating a new/empty file Assignment1_21CS30023_results.txt
        pass
    for query_line in query_file:
        term_list=[]
        flag = 1
        query_line = query_line.strip()
        query_line = query_line.split()
        query_id = query_line[0]
        query_terms = (query_line[1:])
        for term in query_terms:
            term = str(term)
            # print(term)
            if term in inverted_index:
                if(flag == 1):
                    flag = 0
                    term_list = inverted_index[term]
                else:
                    term_list = merge_AND_two_list(term_list , inverted_index[term])
                
                               
        # Writing the result in file Assignment1_21CS30023_results.txt
        with open('Assignment1_21CS30023_results.txt', 'a') as file:
            file.write(query_id + " : ")
            for name in term_list:
                file.write(str(name) + " ")
            file.write("\n")


                
def main():
    if(len(sys.argv) != 3):
        print("ERROR : python3 Assignment1_21CS30023_bool.py  [Either Excess or No arguments]")
        sys.exit(1)

    model_file = sys.argv[1]
    query_file = sys.argv[2]

    try:
        query_file = open(query_file, "r")
    except:
        print("ERROR IN LOADING QUERY FILE")
        sys.exit(1)

    try:
        with open(model_file , 'rb') as file:
            inverted_index = pickle.load(file)
    except:
        print("ERROR IN LOADING MODEL_QUERY FILE")
        sys.exit(1)

    Merge(query_file , inverted_index)


if __name__ == "__main__":
    main()