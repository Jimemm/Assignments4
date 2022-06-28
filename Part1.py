# Dimitrios Emmanouilidis, 2967

import sys
import time
import heapq

# Commit Success

# Part 1
def naive(transactions, queries):
    results = []
    start_time = time.time()

    for q in queries:

        result = []
        for t in range(len(transactions)):
            if all(transaction in transactions[t] for transaction in q):
                result.append(t)
        results.append(result)

    return results, time.time() - start_time


# Part 2
def write_sigfile(data_signatures, file_name):
    sigfile = open(file_name, 'w')
    for d in data_signatures:
        sigfile.write(str(d) + "\n")

    sigfile.close()


def create_signature(data_list):
    sigfile = []

    for d in data_list:
        bitmap = 0
        for i in d:
            bitmap += 2 ** i
        sigfile.append(bitmap)

    return sigfile


def containment(transactions, queries):
    results = []

    transaction_signatures = create_signature(transactions)
    query_signatures = create_signature(queries)

    write_sigfile(transaction_signatures, "sigfile.txt")

    start_time = time.time()

    for q_signature in query_signatures:
        result = []
        for t_id in range(len(transaction_signatures)):
            if transaction_signatures[t_id] & q_signature == q_signature:
                result.append(t_id)
        results.append(result)

    return results, time.time() - start_time


# Part 3
def write_bitslice_file(data, file_name):
    bitslice_file = open(file_name, 'w')
    for d in range(len(data)):
        bitslice_file.write(str(d) + ": " + str(data[d]) + "\n")

    bitslice_file.close()


def create_bitslice(data_list):
    bitslise_hash = {}
    for i in range(len(data_list)):
        for t in data_list[i]:
            if t in bitslise_hash:
                bitslise_hash[t] += 2 ** i
            else:
                bitslise_hash[t] = 2 ** i

    max_key = max(bitslise_hash.keys())
    bitslice = [0] * (max_key + 1)
    for i in range(len(bitslice)):
        bitslice[i] = bitslise_hash[i] if i in bitslise_hash else 0

    return bitslice


def two_powers(num):
    num = bin(num)
    num = num[2:]
    num = [int(x) for x in str(num)]
    enabled_powers = []
    for i in range(len(num) - 1, -1, -1):
        if num[i] & 1:
            enabled_powers.append(len(num) - 1 - i)

    return enabled_powers


def bitslice_containment(transactions, queries):
    results = []

    bitslice = create_bitslice(transactions)

    write_bitslice_file(bitslice, "bitslice.txt")

    time_start = time.time()

    for q in queries:
        mask = bitslice[q[0]]

        for i in range(1, len(q)):
            mask = bitslice[q[i]] & mask

        results.append(two_powers(mask))

    return results, time.time() - time_start


# Part 4
def write_invfile(data, file_name):
    bitslice_file = open(file_name, 'w')
    for d in range(len(data)):
        bitslice_file.write(str(d) + ": " + str(data[d]) + "\n")

    bitslice_file.close()


def create_inverted_file(data_list):
    inverted_file_dict = {}

    for t in range(len(data_list)):
        for i in data_list[t]:
            if i in inverted_file_dict:
                heapq.heappush(inverted_file_dict[i], t)
            else:
                inverted_file_dict[i] = [t]

    max_key = max(inverted_file_dict.keys())
    inverted_file = [0] * (max_key + 1)
    for i in range(len(inverted_file)):
        inverted_file[i] = inverted_file_dict[i] if i in inverted_file_dict else []

    return inverted_file


def merge_intersect_sorted_lists(list1, list2):
    result = []
    i, j = 0, 0

    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            if len(result):
                if list1[i] > result[-1]:
                    result.append(list2[j])
            else:
                result.append(list2[j])
            i += 1
            j += 1
        elif list1[i] > list2[j]:
            j += 1
        else:
            i += 1

    return result


def inverted_file_containment(transactions, queries):
    results = []

    inverted_file = create_inverted_file(transactions)
    write_invfile(inverted_file, "invfile.txt")

    time_start = time.time()

    for q in queries:
        result = inverted_file[q[0]]

        for i in range(1, len(q)):
            result = merge_intersect_sorted_lists(result, inverted_file[q[i]])

        results.append(result)

    return results, time.time() - time_start


# Main

if len(sys.argv) < 5:
    print("Python script usage: python3 part1.py <transaction_file.txt> <queries_file.txt> <qnum(-1 for all)> "
          "<method(-1 for all | 0: naive, 1: exact signature, 2: exact bitslice signature, 3: inverted file>")
    exit(-1)

transaction_file = open(sys.argv[1], 'r')
queries_file = open(sys.argv[2], 'r')
qnum = int(sys.argv[3])
method = int(sys.argv[4])

transactions = []
queries = []

for line in transaction_file:
    line = line[1:-2]
    non_duplicates_list = list(set(line.split(", ")))
    transaction_list = [int(i) for i in non_duplicates_list]
    transactions.append(transaction_list)

transaction_file.close()

for line in queries_file:
    line = line[1:-2]
    non_duplicates_list = list(set(line.split(", ")))
    query_list = [int(i) for i in non_duplicates_list]
    queries.append(query_list)

queries_file.close()

selected_queries = []

if qnum == -1:
    selected_queries = queries
else:
    selected_queries = [queries[qnum]]

if method == -1:
    naive_results, naive_time = naive(transactions, selected_queries)
    esf_results, esf_time = containment(transactions, selected_queries)
    ebsf_results, ebsf_time = bitslice_containment(transactions, selected_queries)
    if_results, if_time = inverted_file_containment(transactions, selected_queries)

    if qnum != -1:
        print("Naive Method result:")
        print(naive_results[0])
        print("Naive Method computation time = " + str(naive_time))
        print("Signature File result:")
        print(esf_results[0])
        print("Signature File computation time = " + str(esf_time))
        print("Bitsliced Signature File result:")
        print(ebsf_results[0])
        print("Bitsliced Signature File computation time = " + str(ebsf_time))
        print("Inverted File result:")
        print(if_results[0])
        print("Inverted File Computation time = " + str(if_time))
    else:
        print("Naive Method computation time = " + str(naive_time))
        print("Signature File computation time = " + str(esf_time))
        print("Bitsliced Signature File computation time = " + str(ebsf_time))
        print("Inverted File Computation time = " + str(if_time))

elif method == 0:
    naive_results, naive_time = naive(transactions, selected_queries)

    if qnum != -1:
        print("Naive Method result:")
        print(naive_results[0])
        print("Naive Method computation time = " + str(naive_time))
    else:
        print("Naive Method computation time = " + str(naive_time))

elif method == 1:
    esf_results, esf_time = containment(transactions, selected_queries)

    if qnum != -1:
        print("Signature File result:")
        print(esf_results[0])
        print("Signature File computation time = " + str(esf_time))
    else:
        print("Signature File computation time = " + str(esf_time))

elif method == 2:
    ebsf_results, ebsf_time = bitslice_containment(transactions, selected_queries)

    if qnum != -1:
        print("Bitsliced Signature File result:")
        print(ebsf_results[0])
        print("Bitsliced Signature File computation time = " + str(ebsf_time))
    else:
        print("Bitsliced Signature File computation time = " + str(ebsf_time))

elif method == 3:
    if_results, if_time = inverted_file_containment(transactions, selected_queries)

    if qnum != -1:
        print("Inverted File result:")
        print(if_results[0])
        print("Inverted File Computation time = " + str(if_time))
    else:
        print("Inverted File Computation time = " + str(if_time))
