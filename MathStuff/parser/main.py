from tokenizer import Tokenizer
from parse import Parser
from interpreter import Interpreter

while True:
    value = input("Math |> ")
    if value == "quit" or value == "exit":
        break

    try:
        tokens = Tokenizer(value).generate_tokens()
        print(list(tokens))
    except Exception as e:
        print("Lexing: ", e)
        continue

    try:
        parsed_object = Parser(Tokenizer(value).generate_tokens()).parse()
        print(parsed_object)
    except Exception as e:
        print("Parsing: ", e)

    try:
        print(Interpreter().visit(parsed_object))
    except Exception as e:
        print("Interpreting: ", e)
