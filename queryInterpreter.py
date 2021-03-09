import re


def query_interpreter(query_string, db):
    # operate the colon operator ':'
    object_field = query_string.split(':')[0].strip()
    keywords = query_string.split(':')[1].strip()

    mycol = dot_operator(object_field)[0]
    attr = dot_operator(object_field)[1]

    if ('AND' in keywords) or ('OR' in keywords) or ('NOT' in keywords):
        logical_op = logical_operator(keywords)[0]
        logical_exp = logical_operator(keywords)[1]
        if logical_op == '$not':
            query = parse_expression(attr, logical_exp[0])
            temp = {attr: {'$not': query}}
            print(temp)
            data = db[mycol].find({attr: {'$not': query}}, {"_id": 0})
            return data

        else:
            query1 = parse_expression(attr, logical_exp[0])
            query2 = parse_expression(attr, logical_exp[1])
            temp = {logical_op: [{attr: query1}, {attr: query2}]}
            print(temp)
            data = db[mycol].find({logical_op: [{attr: query1}, {attr: query2}]}, {"_id": 0})
            return data

    else:
        query = parse_expression(attr, keywords)
        temp = {attr: query}
        print(temp)
        data = db[mycol].find({attr: query}, {"_id": 0})
        return data


def parse_expression(attr, expression):
    if ('>' in expression) or ('<' in expression):
        query = comparison_operator(expression)

    elif '\"' in expression:
        query = quote_operator(expression)
        if (attr == 'rating') or (attr == 'rating_count') or (attr == 'review_count'):
            query = float(query)

    else:
        re_expression = '.*' + expression + '.*'
        query = re.compile(re_expression, re.IGNORECASE)

    return query


def dot_operator(object_field):
    obj = object_field.split('.')[0]
    field = object_field.split('.')[1]
    return obj, field


def quote_operator(keywords):
    # exact
    if keywords.count('\"') != 2:
        return "Bad request. Quotes not enclose correctly", 400

    search_term = re.findall('"([^"]*)"', keywords)[0]
    return search_term


def logical_operator(keywords):
    if 'AND' in keywords:
        logical_list = [x.strip() for x in keywords.split('AND')]

        return '$and', logical_list

    elif 'OR' in keywords:
        logical_list = [x.strip() for x in keywords.split('OR')]
        return '$or', logical_list

    elif 'NOT' in keywords:
        logical_list = [keywords.split('NOT')[1].strip()]
        return '$not', logical_list


def comparison_operator(keywords):
    try:
        compare_val = float(re.split(r'[<>]', keywords)[1].strip())
    except:
        return "Bad request. Please enter a valid number to compare", 400

    if '>' in keywords:
        query = {'$gt': compare_val}
        return query
    elif '<' in keywords:
        query = {'$lt': compare_val}
        return query
