import ast
import astor
import pprint

# Read the configuration file
with open('config.py', 'r') as file:
    tree = ast.parse(file.read())

# Define a visitor class to modify the AST
class ConfigModifier(ast.NodeTransformer):
    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'my_dict':
            # Modify the dictionary
            new_values = {
                'key1': 'new_value1',
                'key3': 'value3'
            }
            for key, value in new_values.items():
                node.value.keys.append(ast.Constant(key))
                node.value.values.append(ast.Constant(value))
        return node

# Modify the AST
modifier = ConfigModifier()
modified_tree = modifier.visit(tree)

# Pretty print the dictionary
for node in ast.walk(modified_tree):
    if isinstance(node, ast.Assign) and node.targets[0].id == 'my_dict':
        pretty_dict = pprint.pformat(ast.literal_eval(node.value))
        node.value = ast.parse(pretty_dict).body[0].value

# Write the modified AST back to the file
with open('config.py', 'w') as file:
    file.write(astor.to_source(modified_tree))