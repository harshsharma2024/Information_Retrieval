# Roll No.: 21CS30023
# Name: Harsh Sharma
# IR Assignment 2

import math
import sys

# Proces_Gold_Standard
def Proces_Gold_Standard(data , mappingQID):
    Dict = {}
    for line in data.splitlines():
        line = line.split()
        x = mappingQID[line[0]]
        if x not in Dict:
            Dict[x] = {}
        Dict[x][line[1]] = line[2]
    return Dict

def Proces_Ranked_Data(data):
    # Consider only top 20 Ranked Documents
    Dict = {}
    for line in data.splitlines():
        if line.split()[0] not in Dict:
            Dict[line.split()[0]] = []
        Dict[line.split()[0]] = (line.split()[2:22])
    return Dict

def mappingQIDs(data,A_Ranked_List):
    # Itereate over A_Ranked_List and find the corresponding query ID in cranqrel
    mappingQID = {}
    line = data.splitlines()
    i = 0
    for query in A_Ranked_List:
        if line[i].split()[0] not in mappingQID:
            x = line[i].split()[0]
            mappingQID[line[i].split()[0]] = query
            while line[i].split()[0] == x:
                i += 1
                if i == len(line):
                    break
            if i == len(line):
                break
                

    return mappingQID

def Precision(A_Ranked_List,Gold_Standard,file):
    # Calculate Average Precision at 10 for each query
    A_Precesion = {}

    MAP_ten = 0
    MAP_twenty = 0
    averNDCG_ten = 0
    averNDCG_twenty = 0

    query_cnt = 0

    for query in A_Ranked_List:
        A_Precesion[query] = []
        avg_P_at_10 = 0
        count = 0
        for i in range(10):
            if i<len(A_Ranked_List[query]) and A_Ranked_List[query][i] in Gold_Standard[query] and int(Gold_Standard[query][A_Ranked_List[query][i]]) > 0:
                count += 1
                avg_P_at_10 += count/(i+1)
        if count==0:
            avg_P_at_10 = 0
        else:
            avg_P_at_10 /= count

        A_Precesion[query].append(avg_P_at_10)

        # Calculate Average Precision at 20 for each query
        avg_P_at_20 = 0
        count = 0
        for i in range(20):
            if i<len(A_Ranked_List[query]) and A_Ranked_List[query][i] in Gold_Standard[query] and int(Gold_Standard[query][A_Ranked_List[query][i]]) > 0:
                count += 1
                avg_P_at_20 += count/(i+1)
        # avg_P_at_20 /= count
        if count==0:
            avg_P_at_20 = 0
        else:
            avg_P_at_20 /= count

        A_Precesion[query].append(avg_P_at_20)

        # Calculating NDCG at 10 for each query
        DCG = 0
        for i in range(10):
            if i<len(A_Ranked_List[query]) and A_Ranked_List[query][i] in Gold_Standard[query] and int(Gold_Standard[query][A_Ranked_List[query][i]]) > 0:
                DCG += int(Gold_Standard[query][A_Ranked_List[query][i]])/math.log2(i+2)
        IDCG = 0
        # Sort the Gold_Standard[query] in descending order of relevance
        sorted_Gold_Standard = sorted(Gold_Standard[query].items(), key=lambda x: x[1],reverse=True)
        # print(sorted_Gold_Standard)
        for i in range(10):
            if(i<len(sorted_Gold_Standard) and int(sorted_Gold_Standard[i][1]) > 0):
                IDCG += int(sorted_Gold_Standard[i][1])/math.log2(i+2)
        NDCG = DCG/IDCG
        A_Precesion[query].append(NDCG)

        # Calculating NDCG at 20 for each query
        DCG = 0
        for i in range(20):
            if i<len(A_Ranked_List[query]) and A_Ranked_List[query][i] in Gold_Standard[query] and int(Gold_Standard[query][A_Ranked_List[query][i]]) > 0:
                DCG += int(Gold_Standard[query][A_Ranked_List[query][i]])/math.log2(i+2)
        IDCG = 0
        # Sort the Gold_Standard[query] in descending order of relevance
        sorted_Gold_Standard = sorted(Gold_Standard[query].items(), key=lambda x: x[1],reverse=True)
        # print(sorted_Gold_Standard)
        for i in range(20):
            if(i<len(sorted_Gold_Standard) and int(sorted_Gold_Standard[i][1]) > 0):
                IDCG += int(sorted_Gold_Standard[i][1])/math.log2(i+2)
        NDCG = DCG/IDCG
        A_Precesion[query].append(NDCG)

        # Write the results to file
        file.write("Query ID: "+query+"\n")
        file.write("Average Precision at 10: "+str(avg_P_at_10)+"\n")
        file.write("Average Precision at 20: "+str(avg_P_at_20)+"\n")
        file.write("NDCG at 10: "+str(A_Precesion[query][2])+"\n")
        file.write("NDCG at 20: "+str(A_Precesion[query][3])+"\n")
        file.write("\n")



        MAP_ten += avg_P_at_10
        MAP_twenty += avg_P_at_20
        averNDCG_ten += A_Precesion[query][2]
        averNDCG_twenty += A_Precesion[query][3]
        query_cnt += 1

    MAP_ten /= query_cnt
    MAP_twenty /= query_cnt
    averNDCG_ten /= query_cnt
    averNDCG_twenty /= query_cnt


    file.write("Average MAP@10: "+str(MAP_ten)+"\n")
    file.write("Average MAP@20: "+str(MAP_twenty)+"\n")
    file.write("Average NDCG@10: "+str(averNDCG_ten)+"\n")
    file.write("Average NDCG@20: "+str(averNDCG_twenty)+"\n")




    return A_Precesion
            




def main():

    if(len(sys.argv) != 3):
        print("ERROR : python3 Assignment1_21CS30023_bool.py [Either Excess or No arguments]")
        sys.exit(1)

    ranked_file = sys.argv[1]
    ranked_list = sys.argv[2]


    try:
        data = open(ranked_list,'r').read()
    except:
        print("ERROR : Unable to open file")
        sys.exit(1)

    # print(data)

    A_Ranked_List = {}
    A_Ranked_List = Proces_Ranked_Data(data)
    # print(A_Ranked_List['002'])

    try:
        data = open(ranked_file,'r').read()
    except:
        print("ERROR : Unable to open gold standard file")
        sys.exit(1)

    K = ranked_list.split('_')[4].split('.')[0]
    # print(K)
    
    #Create mapping of cranqrel query ID and RankedList query ID Using A_Ranked_List as they are different in both files
    mappingQID = {}
    mappingQID = mappingQIDs(data,A_Ranked_List)
    # print(mappingQID)



    Gold_Standard = {}
    Gold_Standard = Proces_Gold_Standard(data,mappingQID)

    # print(Gold_Standard['002'])

    # print(A_Ranked_List)
    file_name = f'Assignment2_21CS30023_metrics_{K}.txt'
    # print(file_name)
        
    file = open(file_name,'w')

    A_Precesion = {}
    A_Precesion = Precision(A_Ranked_List,Gold_Standard ,file)



if __name__ == "__main__":
    main()