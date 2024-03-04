import sys
global code #String were the code will be "Downloaded"
code = ""

def code_getter():
    """
    This function read the content of a file and store the content onto the "code" variable
    """
    global code
    if(len(sys.argv)!= 2): #This line tests if the number of elements in the list of arguments from the command line is equal to two, this is because the first argument is the Python file name, and the second must be our file name
        sys.exit()
    else:
        file_name = sys.argv[1]
        with open(file_name) as file:
            for line in file.readlines():
                
                code = code + line #Open the file and line by line, it reads the content and concatenate each line onto the string "code"

code_getter()
print(code)