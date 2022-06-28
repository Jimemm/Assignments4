# Dimitrios Emmanouilidis, 2967

import sys
import time


def write_invfile(data, file_name, T_trf):
    bitslice_file = open(file_name, 'w')
    for d in range(len(data)):
        bitslice_file.write(str(d) + ": " + str(T_trf[d]) + ", " + str(data[d]) + "\n")

    bitslice_file.close()


def create_inverted_file(data):
    inverted_file_dict = {}

    for d in range(len(data)):
        for i in data[d]:
            if i in inverted_file_dict:
                if d in inverted_file_dict[i]:
                    inverted_file_dict[i][d] += 1
                else:
                    inverted_file_dict[i][d] = 1
            else:
                inverted_file_dict[i] = {d: 1}

    max_key = max(inverted_file_dict.keys())
    inverted_file = [0] * (max_key + 1)
    for i in range(len(inverted_file)):
        if i in inverted_file_dict:
            temp = []
            for key in inverted_file_dict[i]:
                temp.append([key, inverted_file_dict[i][key]])
            inverted_file[i] = temp
        else:
            inverted_file[i] = []

    return inverted_file, inverted_file_dict


def create_T_trf(inverted_file, T):
    T_trf = []
    for d in range(len(inverted_file)):
        T_trf.append(T / len(inverted_file[d]) if len(inverted_file[d]) != 0 else 0)

    return T_trf


def merge_join_cmpr_first_item(list1, list2):
    result = []
    i, j = 0, 0

    while i < len(list1) and j < len(list2):
        if list1[i][0] < list2[j][0]:
            result.append([list1[i][0]])
            i += 1
        elif list1[i][0] > list2[j][0]:
            result.append([list2[j][0]])
            j += 1
        else:
            if len(result):
                if list1[i][0] > result[-1][0]:
                    result.append([list2[j][0]])
            else:
                result.append([list2[j][0]])

            i += 1
            j += 1

    while i < len(list1):
        if list1[i][0] > result[-1][0]:
            result.append([list1[i][0]])
        i += 1

    while j < len(list2):
        if list2[j][0] > result[-1][0]:
            result.append([list2[j][0]])
        j += 1

    return result


def relevance(transactions, queries, k):
    results = []

    inverted_file, inverted_file_dict = create_inverted_file(transactions)
    T_trfs = create_T_trf(inverted_file, len(transactions))
    write_invfile(inverted_file, "invfileocc.txt", T_trfs)

    time_start = time.time()

    for q in queries:
        result = []
        rels = {}

        merged_transactions = inverted_file[q[0]]

        for i in range(1, len(q)):
            merged_transactions = merge_join_cmpr_first_item(merged_transactions, inverted_file[q[i]])

        for i in q:

            for t in range(len(merged_transactions)):
                ti = merged_transactions[t][0]
                if ti in rels:
                    if ti in inverted_file_dict[i]:
                        rels[ti] += inverted_file_dict[i][ti] * T_trfs[i]
                    else:
                        rels[ti] += 0
                else:
                    if ti in inverted_file_dict[i]:
                        rels[ti] = inverted_file_dict[i][ti] * T_trfs[i]
                    else:
                        rels[ti] = 0

        rels = list(sorted(rels.items(), key=lambda x: x[1], reverse=True))[:k]
        for r in rels:
            result.append([r[1], r[0]])

        results.append(result)

    return results, time.time() - time_start


def create_T_trf_naive(transactions):
    trf = {}
    T = len(transactions)

    for t in transactions:
        for i in set(t):
            if i in trf:
                trf[i] += 1
            else:
                trf[i] = 1

    for i in trf:
        trf[i] = T / trf[i]

    return trf


def naive(transactions, queries, k):
    results = []

    T_trf = create_T_trf_naive(transactions)

    time_start = time.time()

    for q in queries:
        result = []
        rels = {}

        for i in q:

            for t in range(len(transactions)):
                if t in rels:
                    rels[t] += transactions[t].count(i) * T_trf[i]
                else:
                    rels[t] = transactions[t].count(i) * T_trf[i]

        rels = list(sorted(rels.items(), key=lambda x: x[1], reverse=True))[:k]
        for r in rels:
            if r[1] != 0:
                result.append([r[1], r[0]])

        results.append(result)

    return results, time.time() - time_start


# Main

if len(sys.argv) != 6:
    print("Python script usage: python3 part2.py <transaction_file.txt> <queries_file.txt> <qnum(-1 for all)> "
          "<method(-1 for all | 0: naive, 1: inverted files> <k>")
    exit(-1)

transaction_file = open(sys.argv[1], 'r')
queries_file = open(sys.argv[2], 'r')
qnum = int(sys.argv[3])
method = int(sys.argv[4])
k = int(sys.argv[5])

transactions = []
queries = []

for line in transaction_file:
    line = line[1:-2].split(", ")
    # non_duplicates_list = list(set(line))
    transaction_list = [int(i) for i in line]
    transactions.append(transaction_list)

transaction_file.close()

for line in queries_file:
    line = line[1:-2].split(", ")
    # non_duplicates_list = list(set(line))
    query_list = [int(i) for i in line]
    queries.append(query_list)

queries_file.close()

if qnum == -1:
    selected_queries = queries
else:
    selected_queries = [queries[qnum]]

if method == -1:
    naive_results, naive_time = naive(transactions, selected_queries, k)
    if_results, if_time = relevance(transactions, selected_queries, k)

    if qnum != -1:
        print("Naive Method result:")
        print(naive_results[0])
        print("Naive Method computation time = " + str(naive_time))
        print("Inverted File result:")
        print(if_results[0])
        print("Inverted File Computation time = " + str(if_time))
    else:
        print("Naive Method computation time = " + str(naive_time))
        print("Inverted File Computation time = " + str(if_time))

elif method == 0:
    naive_results, naive_time = naive(transactions, selected_queries, k)

    if qnum != -1:
        print("Naive Method result:")
        print(naive_results[0])
        print("Naive Method computation time = " + str(naive_time))
    else:
        print("Naive Method computation time = " + str(naive_time))

elif method == 1:
    if_results, if_time = relevance(transactions, selected_queries, k)

    if qnum != -1:
        print("Inverted File result:")
        print(if_results[0])
        print("Inverted File Computation time = " + str(if_time))
    else:
        print("Inverted File Computation time = " + str(if_time))
