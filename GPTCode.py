def extract_relevant_info(filename):
    relevant_fields = ['Name', 'In-Network', 'Gender', 'Specialty', 'Location', 'Telephone']

    with open(filename, 'r') as file:
        lines = file.readlines()

    providers = []
    current_provider = {}

    for line in lines:
        line = line.strip()
        if line:
            if line.endswith(','):
                if current_provider:
                    providers.append(current_provider)
                    current_provider = {}
                    print(current_provider)
                current_provider['Name'] = line[:-1]
            else:
                key, value = line.split(':', 1)
                field = key.strip()
                if field in relevant_fields:
                    current_provider[field] = value.strip()

    if current_provider:
        providers.append(current_provider)

    return providers


# Example usage:
filename = 'PortlandGPsRaw.txt'
relevant_info = extract_relevant_info(filename)
for provider in relevant_info:
    print(provider)
    print('-' * 30)
