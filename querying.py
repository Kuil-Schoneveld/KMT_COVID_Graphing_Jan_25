
def rivm_query(g):

    user_query = input("Enter your query or 'q' to quit: ")

    # Remove whitespace from input for easier entry, seems flawed
    user_query = user_query.strip()

    if user_query == 'q':
        return None
    # Following elif doesn't accomplish anything, even if input is integer
    # I suspect that python converts all input() to strings, so this is never called
    elif type(user_query) != str:
        print('I need the query to be a string')
        return None
    elif type(user_query) == str:
        pass

    q_output = g.query(user_query)

    #Iterate over the output to give set of var bindings
    count = 0
    for solution in q_output:
        count += 1
        print(count, solution)