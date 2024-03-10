# Compiler-Team04
# Execute the code by as "python3 Lexer.py code.xd" You can change the file name on the prompt if tou change the name of your file
Example 1.
#                                                                                               CurrentChar     Current   Current   Current
#                                                                                                      |         |         |         |
#PeekChar in types word: The lexer found the following entrance INT x. The char pointers will be like: INT x --> INT x --> INT x --> INT x --> STOP and do smthg
#                                                                                                      |         |          |          |
#                                                                                                 PeekChar        Peek       Peek       Peek 
#                                                                                                      Store in buffer every single transition (while)

Example 2.
#                                                                                               CurrentChar     Current   Current   Current
#                                                                                                      |         |         |         |
#PeekChar in types word: The lexer found the following entrance INT x. The char pointers will be like: INT x --> INT x --> INT x --> INT x --> STOP and do smthg
#                                                                                                          |        |          |          |
#                                                                                                          Peek         Peek       Peek       Peek 
#                                                                                                      Store in buffer every single transition (while)