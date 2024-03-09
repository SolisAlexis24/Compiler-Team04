import sys
global code #String were the code will be "Downloaded"
code = ""
global Token #Dictionary where tokens will be stored an classified
Token = {"keyword":[], "identifier":[],  "operator":[], "constant":[], "puctuation":[]} #It will have the form {type:[value1, value2, ..., valueN]}
T_kw = ["int", "bool", "if", "else", "return"] #Token type keyword (RESERVED WORDS)
T_op = ["+", "-", "/", "*", "**", "and" , "or" , "not","<", ">", "<=", ">=", "==", "!=", "="] #Token type operator
T_punct = [";", "(", ")", "{", "}"] #Token type punctuation
Comment = "@" #Comment
numbers = "0123456789"
letters = "abcdefghijklmnopqrstuvwxyz"



def codeGetter():
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


codeGetter()

class Lexer:
    def __init__(self, codeString):
        self.codeString = code #Set the string to analize as the code that the function "codeGetter" gets
        self.currentPos = -1 #The initial position for the lexer is -1 (The method advance will update this inmediatly)
        self.peekPos = -1
        self.currentChar = None #The initial char of the lexer is None (The method advance will update this inmediatly)
        self.peekChar = None 
        self.line = 0
        self.buffer = ""
        self.flag = 0

    def advanceCurrent(self):
        """
        this method made the current char advance a space
        """
        self.currentPos += 1 
        if (self.currentPos < len(self.codeString)):
            self.currentChar = self.codeString[self.currentPos]
        else:
            self.currentChar = None

    def Peek(self):
        """
        this method made the peek char advance a space
        """
        self.peekPos += 1 
        if (self.peekPos < len(self.codeString)):
            self.peekChar = self.codeString[self.peekPos]
        else:
            self.peekChar = None

    def equalize(self):
        """
        This method equalize both pointers position, the current char to the peek char
        """
        self.currentPos = self.peekPos
        self.currentChar = self.peekChar
    
    def emptyBuffer(self):
        """
        This method empty the buffer
        """
        self.buffer = ""

    def advance_eol(self):
        """
        This method advance untill it found the end of line
        """
        while(self.peekChar != "\n"):
            self.Peek()

    def scan(self):
        if (self.peekChar != None): #Executes until reach the eof
            if (self.peekChar == " " or self.peekChar =="\t"): #The peek char looks forward if the char is a non-imprimible char.
                self.Peek() #If it's, it moves forward
                self.equalize() #Equalize the both pointers
                self.scan() #Recursion
            elif (self.peekChar == Comment): #If detects the beginning of a coment 
                self.advance_eol() #Advance until the end of the line
                self.Peek() #Advance again to be in the next line
                self.line += 1 #Increment the atribute line
                self.equalize() #Equalize pointers
                self.scan() #Recursion
            elif(self.peekChar == "\n"):
                self.Peek() #Advance again to be in the next line
                self.line += 1 #Increment the atribute line
                self.equalize() #Equalize pointers
                self.scan() #Recursion
            
            elif (self.currentChar in letters): #If the lexeme begin with a letter, it could be a keyword, an identifier or an operator (and, or, not)      
                while(self.peekChar != " " and self.peekChar in letters): #moves the peekChar until it found a whitespace. Look for the example 1 in the README file
                    if(not(self.peekChar in letters)): # If the character is not found in letters, it cannot be a keyword, operator (and, or, not) or an identifier 
                        self.Peek() #Advance
                        break
                    self.buffer += self.peekChar #Store the chain onto a buffer
                    self.Peek() #Advance
                if (self.buffer in T_kw): #If the buffer string is a reserved word
                    if(not(self.buffer in Token["keyword"])): #if is not still stored
                        Token["keyword"].append(self.buffer) #Store it
                    self.emptyBuffer() #empty the buffer
                    self.Peek()
                    self.equalize()
                    self.scan()
                elif (self.buffer in T_op): #If the buffer string is a operator ("and", "or", "not")
                    if(not(self.buffer in Token["operator"])): #if is not still stored
                        Token["operator"].append(self.buffer) #Store it
                    self.emptyBuffer() #empty the buffer
                    self.Peek()
                    self.equalize()
                    self.scan()
                else: #if the char is a letter and it is not a keyword or operator ("and", "or", "not"), it is an identifier
                    if(not(self.buffer in Token["identifier"])): #if it is not stored already
                        Token["identifier"].append(self.buffer) #Store it
                    self.emptyBuffer() #empty the buffer
                    self.Peek() #Advance the peekchar
                    self.equalize() #equalize the chars
                    self.scan() #Recursion
            
            elif (self.currentChar in T_punct):#If the lexeme is an puctuation
                if (not(self.currentChar in Token["puctuation"])): #if it is not stored already
                    Token["puctuation"].append(self.currentChar) #Store it
                self.emptyBuffer() #empty the buffer
                self.Peek() #Advance the peekchar
                self.equalize() #equalize the chars
                self.scan() #Recursion 
            
            elif (self.currentChar in T_op): #If the lexeme is a operator ("+", "-", "/", "*", "**","<", ">", "<=", ">=", "==", "!=", "=")
                self.buffer += self.peekChar
                self.Peek()
                self.buffer += self.peekChar
                if (self.buffer in T_op):
                    if(not(self.currentChar in Token["operator"])):
                        Token["operator"].append(self.currentChar)
                else:
                    self.emptyBuffer()
                    if(not(self.currentChar in Token["operator"])):
                        Token["operator"].append(self.currentChar)
                self.equalize() #equalize the chars
                self.scan() #Recursion  
            
            elif (self.currentChar in numbers): #If the lexeme begin a digit
                while(self.peekChar != " "): #moves the peekChar until it found a whitespace
                    if (not(self.peekChar in numbers )):  
                        break
                    self.buffer += self.peekChar #Store the chain onto a buffer
                    self.Peek() #Advance
                if (not(self.buffer in Token["constant"])): #if it is not stored already
                    Token["constant"].append(self.buffer) #Store it
                self.emptyBuffer() #empty the buffer
                self.Peek() #Advance the peekchar
                self.equalize() #equalize the chars
                self.scan() #Recursion  
        else:
            return

Lexer1 = Lexer(code)
Lexer1.advanceCurrent()
Lexer1.Peek()
Lexer1.scan()
print(Token)