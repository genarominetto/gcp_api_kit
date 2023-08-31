# Importing the os module for interacting with the operating system
import os
# Importing the ast module for abstract syntax tree manipulations
import ast

# Defining a function to extract top-level function and class details from a given python file
def extract_items(file_path):
    """Extract function names and class names from a Python file."""
    # Open the file in read mode
    with open(file_path, "r") as source:
        # Parse the source code into an abstract syntax tree (AST)
        tree = ast.parse(source.read())
    # Extract top-level function definitions (name and arguments) from the AST
    functions = [(node.name, [arg.arg for arg in node.args.args]) 
                 for node in tree.body if isinstance(node, ast.FunctionDef)]
    # Extract top-level class definitions (name) from the AST
    classes = [(node.name) for node in tree.body if isinstance(node, ast.ClassDef)]
    # Return the extracted function and class details
    return functions, classes

# Define a function to generate import statements and optionally function calls for all Python files in a directory
def generate_code_snippet(directory, gen_func_calls=True):
    """Generate import statements and function calls from Python files in a directory."""
    # Initialize the import statements string
    import_statements = f'#@title Import statements\n%%capture\nprint(generate_code_snippet("{directory}", False))\n'
    # Initialize the function calls string
    function_calls = ""
    
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        # For each file in the directory
        for file in files:
            # Check if the file is a Python file
            if file.endswith(".py"):
                # Join the root directory and the file name to get the complete file path
                file_path = os.path.join(root, file)
                # Extract function and class details from the Python file
                function_defs, class_defs = extract_items(file_path)
                
                # Generate import statements for each function in the file
                for function_name, _ in function_defs:
                    # Format the import path correctly by replacing slashes with dots and removing the file extension
                    import_path = os.path.splitext(file_path.replace("/", "."))[0]
                    # Add the import statement to the import statements string
                    import_statements += f"from {import_path} import {function_name}\n"
                
                # Generate import statements for each class in the file
                for class_name in class_defs:
                    # Format the import path correctly by replacing slashes with dots and removing the file extension
                    import_path = os.path.splitext(file_path.replace("/", "."))[0]
                    # Add the import statement to the import statements string
                    import_statements += f"from {import_path} import {class_name}\n"
                # Add a newline after the import statements for a file
                import_statements += "\n"

                # If the function calls should be generated
                if gen_func_calls:
                    # If there are function definitions in the file
                    if function_defs:
                        # Add a comment with the file name to the function calls string
                        function_calls += f"# {os.path.splitext(file)[0]}\n"
                        # Generate function calls for each function in the file
                        for function_name, params in function_defs:
                            # Add the function call to the function calls string
                            function_calls += f"{function_name}({', '.join(params)})\n"
                        # Add a newline after the function calls for a file
                        function_calls += "\n"
                    
                    # For each class in the file, add a class instantiation to the function calls string
                    for class_name in class_defs:
                        function_calls += f"{class_name}()\n"
                    
    # If function calls should be generated, return the import statements and the function calls
    if gen_func_calls:
        return import_statements + function_calls
    # If function calls should not be generated, just return the import statements
    else:
        return import_statements
