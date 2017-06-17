from math import log
import operator

# precision = number of relevant documents retrieved / number of retrieved documents
def precision(ranked_array):
    precision_list = []
    nr_docs_retrieved = 0
    nr_relevant_docs_retrieved = 0
    for rank in ranked_array:
        nr_docs_retrieved += 1
        nr_relevant_docs_retrieved += rank[1]
        precision_list.append(nr_relevant_docs_retrieved/float(nr_docs_retrieved))
    return precision_list

# recall = number of relevant documents retrieved /	number of relevant documents
def recall(ranked_array):
    recall_list = []
    nr_relevant_docs_retrieved = 0
    nr_relevant_docs = sum([rank[1] for rank in ranked_array])
    # Don't divide by zero
    if nr_relevant_docs == 0:
        return None
    else:
        for rank in ranked_array:
            nr_relevant_docs_retrieved += rank[1]
            recall_list.append(nr_relevant_docs_retrieved/float(nr_relevant_docs))
        return recall_list

# Returns a float with the precision after K documents have been retrieved
def precision_at_k(k, precisions):
    try:
        # K starts at 1, list index starts at 0
        return precisions[k-1]
    except:
        return None

# Returns the float Discounted Cumulative Gain (DCG) for a ranked result set
def discounted_cumulative_gain(serp):
    # First Element as it is
    sum = serp[0][1]
    # Iterate over rest of the elements to find the DCG
    for items in serp[1:]:
        sum += items[1]/log(items[0],2)
    return sum

######################################## PROGRAM ########################################

# Open the file to get the relevance info
with open('cacm.rel.txt', 'r') as f:
    relevance_list = [line.strip() for line in f]

# Fetch the relevance info and store it in reusable format
rel_docs = {}
for rel in relevance_list:
    rel_array = rel.split(" ")

    queryId = rel_array[0]
    docId = rel_array[2].replace("CACM-","")
    relevance = rel_array[3]

    if relevance != '1':
        continue

    if queryId in rel_docs.keys():
        new_list = rel_docs[queryId]
        new_list.append(docId)
    else:
        new_list = []
        new_list.append(docId)
        rel_docs[queryId] = new_list


# Open queries file
with open('queries1.txt', 'r') as f:
    temp_queries_list = [line.strip() for line in f]

# Store queries and query id's
queries_list = {}
for query in temp_queries_list:
    open_parenth = query.rindex('(')
    close_parenth = query.rindex(')')
    query_no = query[open_parenth+1:close_parenth]
    queries_list[query_no] = query[:open_parenth-1]

# Open the results evaluated by BM25 search engine
with open('results1.eval', 'r') as f:
    results = [line.strip() for line in f]

# Store the results in reusable format
query_results = {}
for result in results:
    res_array = result.split()

    queryId = res_array[0]
    docId = res_array[2]
    rank = res_array[3]
    score = res_array[4]

    if queryId == "query_id":
        continue

    if queryId in query_results.keys():
        new_r_list = query_results[queryId]
        new_r_list[rank] = [docId,score]
    else:
        new_r_list = {}
        new_r_list[rank] = [docId,score]
        query_results[queryId] = new_r_list

# To store the map value for all queries
map = {}
for queryId, value in query_results.items():
    rank_arr = []
    relevant_documents = rel_docs[queryId]
    for rank, doc_arr in value.items():

        relevance = 0
        if doc_arr[0] in relevant_documents:
            relevance = 1
        new_array = [int(rank),relevance]
        rank_arr.append(new_array)


    rank_arr = sorted(rank_arr, key=operator.itemgetter(0))
    print(rank_arr)
    precision_list = precision(rank_arr)
    recall_list = recall(rank_arr)

    f = open(queries_list[queryId]+".txt", 'w')

    print("Rank\tDocument Id\tDocument Score\tRelevance Level\tPrecision\tRecall\tNDCG")
    f.write("Rank\tDocument Id\tDocument Score\tRelevance Level\tPrecision\tRecall\tNDCG\n")
    count = 0
    temp_list_dcg = []
    temp_list_idcg = []
    precistion_at_20 = precision_at_k(20, precision_list)
    total_relevant_documents = len(relevant_documents)
    sum_precision = 0
    for items in rank_arr:
        rank = str(items[0])
        docId = value[rank][0]
        docScore = value[rank][1]
        relevanceLevel = items[1]
        prec = precision_list[count]
        rec = recall_list[count]
        temp_list_dcg.append(items)
        if count < total_relevant_documents:
            temp_list_idcg.append([items[0],1])
        dcg = discounted_cumulative_gain(temp_list_dcg)
        idcg = discounted_cumulative_gain(temp_list_idcg)

        ndcg = dcg / idcg

        if relevanceLevel == 1:
            sum_precision += prec
        map[queryId] = sum_precision / total_relevant_documents

        count+=1

        print("{0}\t{1}\t{2}\t{3}\t{4:.7f}\t{5:.7f}\t{6:.7f}".format(rank,docId,docScore,relevanceLevel,prec,rec,ndcg))
        f.write("{0}\t{1}\t{2}\t{3}\t{4:.7f}\t{5:.7f}\t{6:.7f}\n".format(rank,docId,docScore,relevanceLevel,prec,rec,ndcg))

    f.close()
    print("Precistion at 20 is - ",precistion_at_20)

# Computation for map value
map_value = 0
queryCount = 0
for queryId, value in map.items():
    map_value += value
    queryCount += 1

print("Map value is ", map_value/queryCount)