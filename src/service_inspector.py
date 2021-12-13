import inspect
import examples.service as service


members = inspect.getmembers(service)
service_class_name = None

for member in members:
    if "service" in member[0].lower():
        service_class_name = member[0]

if service_class_name is None:
    print("Nameko class not identified")
    exit(1)

print('service_class_name:')
print(service_class_name)

service_class = getattr(service, service_class_name)

members_of_class = inspect.getmembers(service_class)

methods_and_params = {}

for member in members_of_class:
    # Ignore builtin methods
    if member[0].startswith("__"):
        continue
    # Filter only functions
    if not inspect.isfunction(member[1]):
        continue
    method_name = member[0]
    methods_and_params[method_name] = []
    params = inspect.signature(member[1])
    for param in params.parameters:
        if param == "self":
            continue
        methods_and_params[method_name].append(param)

print('methods_and_params:')
print(methods_and_params)
