import copy

def read_input():
    f = open("input.txt")
    num_queries = int(f.readline())
    query_list = []
    for i in xrange(num_queries):
        query_list.append(f.readline().strip())
    num_sent_kb = int(f.readline())
    kb_list = []
    for i in xrange(num_sent_kb):
        kb_list.append(f.readline().strip())
    return query_list, kb_list

def parse_input(kb_list):
    kb_list = [i.replace(" ", "") for i in kb_list]
    new_kb_list = []
    count = 1
    for sent in kb_list: #each sentence in the KB
        pred = sent.split('|')
        d = {}
        new_list = []
        for i in pred: #each predicate i.e F(x)
            new_str = ""
            j = i[i.index('(')+1: i.index(')')]
            new_str += i[:i.index('(')+1]
            list_pred = j.split(',')
            new_pred_list = []
            for k in list_pred:
                if k >= 'a' and k <= 'z':
                    if not k in d:
                        d[k] = 'p' + str(count)
                        count += 1
                    new_pred_list.append(d[k])
                else:
                    new_pred_list.append(k)
            new_pred = ",".join(new_pred_list)
            new_list.append(new_str + new_pred + ")")
        new_kb_list.append("|".join(new_list))
    return new_kb_list

def prepare_dict(kb_list):
    d = {}
    for sent in kb_list:
        list_pred = sent.split('|')
        for pred in list_pred:
            i = pred[:pred.index('(')]
            if not i in d:
                d[i] = []
            d[i].append(sent)
    return d

def negate(query):
    neg = "~"
    if neg in query:
        return query[1:]
    else:
        return neg + query

def resolve(kb_stack, counter, kb_dict, cutoff):

    stack_length = len(kb_stack)
    while  stack_length > 0:
        last_index = len(kb_stack)-1
        query = kb_stack.pop(last_index)

        query_negation = negate(query)

        query_params_str = query_negation.split("(")[1].split(")")[0]
        parameter_queries = query_params_str.split(",")

        query_begin_list = query_negation.split("(")
        query_begin = query_begin_list[0]

        if query_begin in kb_dict:
            same = ""
            kb_with_pred = kb_dict[query_begin]
            for term in kb_with_pred:
                if counter > cutoff:
                    return False

                list_or = term.split("|")
                for i in list_or:
                    if i.split("(")[0] == query_begin:
                        same = i

                kb_match_str = same.split("(")[1].split(")")[0]
                kb_match = kb_match_str.split(",")

                is_unify = unify(parameter_queries, kb_match)

                if is_unify == True:
                    hash_map = {}

                    flag = False
                    j = 0
                    query_parameter_len = len(parameter_queries)

                    while j < query_parameter_len:
                        if kb_match[j] in hash_map.keys():
                            if hash_map[kb_match[j]] != parameter_queries[j]:
                                if parameter_queries[j] >= 'A' and parameter_queries[j] <= 'Z':
                                    flag = True
                                    break
                        else:
                            hash_map[kb_match[j]] = parameter_queries[j]
                        j = j + 1

                    if flag:
                        continue

                    stack_copy, list_or = my_replace(list_or, hash_map, query_begin, copy.deepcopy(kb_stack))

                    output = resolve(stack_copy, counter+1, kb_dict, cutoff)

                    if output:
                        return True
            return False
        else:
            return False
    return True

def my_replace(list_or, hash_map, query_begin, stack_copy):
    i = 0
    while i < len(list_or):
        for term in hash_map.keys():
            if term in list_or[i] and term >= 'a' and term <= 'z':
                list_or[i] = list_or[i].replace(term, hash_map[term])

        list_list_or = list_or[i].split("(")
        if list_list_or[0] != query_begin:
            p = negate(list_or[i])

            if p in stack_copy:
                stack_copy.remove(p)

            else:
                stack_copy.append(list_or[i])
        i += 1
    return stack_copy, list_or

def unify(x, y):
    i = 0
    count = 0
    while (i < len(x)):
        if x[i][0] >= 'a' and x[i][0] <= 'z' and y[i][0] >= 'a' and y[i][0] <= 'z':
            count = count + 1
        elif x[i][0] >= 'a' and x[i][0] <= 'z' and y[i][0] >= 'A' and y[i][0] <= 'Z':
            count = count + 1
        elif x[i][0] >= 'A' and x[i][0] <= 'Z' and y[i][0] >= 'a' and y[i][0] <= 'z':
            count = count + 1
        elif (x[i] == y[i]):
            count = count+1
        i = i+1

    count = check_same_constant(x, y, count)

    if (count == len(x)):
        return True
    else:
        return False

def check_same_constant(x, y, count):
    if count == len(x):
        hash_map = {}
        i = 0
        while i < len(x):
            if x[i] in hash_map.keys() and hash_map[x[i]] >= 'A' and hash_map[x[i]] <= 'Z':
                if y[i] != hash_map[x[i]]:
                    count -= 1
            else:
                hash_map[x[i]] = y[i]
            i += 1
    return count

def write_output(answers):
    f = open("output.txt", "w")
    for i in answers:
        f.write(i)
        f.write("\n")
    f.close()


if __name__ == '__main__':
    query_list, kb_list = read_input()
    new_kb_list = parse_input(kb_list)
    kb_dict = prepare_dict(new_kb_list)

    len_kb = len(new_kb_list)

    if len_kb <= 20:
        cutoff = 40

    else:
        cutoff = 700

    answers = []

    count = 0
    for query in query_list:
        stack = []
        modified_query = query.replace(" ", "")
        if '~' in query:
            modified_query = modified_query[1:]
        else:
            modified_query = '~' + modified_query
        stack.append(modified_query)
        res = resolve(stack, count, kb_dict, cutoff)

        if res:
            answers.append("TRUE")
        else:
            answers.append("FALSE")

    write_output(answers)



