import ast


def inspect_content(file_content) -> dict:
    """
    Parse file content using ast, and identify methods and params.
    Returns a dict like this:
    {
        "service_name": string,
        "methods": [
            {
                "name": string,
                "params": [string]
            }
        ]
    }
    """
    node = ast.parse(file_content)

    # Identify classes
    classes = [n for n in ast.walk(node) if isinstance(n, ast.ClassDef)]
    class_name = None
    methods_and_params = []

    for class_ in classes:
        if not "service" in class_.name.lower():
            continue

        class_name = class_.name
        # variables = [n for n in ast.walk(class_) if isinstance(n, ast.Name) and n.id == "name"]
        methods = [n for n in ast.walk(class_) if isinstance(n, ast.FunctionDef)]

        # Get methods
        for method in methods:
            method_data = {
                'name': method.name,
                'params': []
            }

            # Get method params
            for arg in method.args.args:
                if arg.arg == "self":
                    continue
                method_data["params"].append(arg.arg)

            methods_and_params.append(method_data)

    return {
        "service_name": class_name,
        "methods": methods_and_params
    }
