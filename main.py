queriesString = ""

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def generateCypherCreate():
    global queriesString
    for name in ["Alice", "Bob", "Carol"]:
        queriesString =queriesString + "CREATE (student:Student name:"+name+") RETURN student\n"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Learn Path git. Welcome good sir.')
    f = open("Cypher.txt", "w")  #"a" - Append - will append to the end of the file, "w" - Write - will overwrite any existing content
    generateCypherCreate()
    print("query:\n"+queriesString)
    f.write(queriesString)
    #
    f.close()


