import inspect
import service


def get_service_data() -> dict:
    members = inspect.getmembers(service)
    service_class_name = None

    for member in members:
        if "service" in member[0].lower():
            service_class_name = member[0]

    if service_class_name is None:
        print("Nameko class not identified")
        exit(1)

    service_class = getattr(service, service_class_name)
    members_of_class = inspect.getmembers(service_class)
    methods_and_params = []

    for member in members_of_class:
        # Ignore builtin methods
        if member[0].startswith("__"):
            continue

        if member[0] == "name":
            service_name = member[1]

        # Filter only functions
        if not inspect.isfunction(member[1]):
            continue


        method_name = member[0]
        method_data = {
            'name': method_name,
            'params': []
        }

        # Get params of method
        params = inspect.signature(member[1])
        for param in params.parameters:
            if param == "self":
                continue
            method_data['params'].append(param)
        methods_and_params.append(method_data)

    return {
        'service_name': service_name,
        'methods': methods_and_params,
    }
