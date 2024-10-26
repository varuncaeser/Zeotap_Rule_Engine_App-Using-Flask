class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # 'operator' or 'operand'
        self.left = left       # Left child node
        self.right = right     # Right child node
        self.value = value     # Operand value (for conditions)

def create_rule(rule_string):
    # Simplified rule parsing: create an AST from the rule_string
    # You can improve this with more sophisticated parsing techniques
    # For this demo, we'll keep it basic.
    if "AND" in rule_string:
        left_rule, right_rule = rule_string.split("AND")
        return Node("operator", Node("operand", value=left_rule.strip()), Node("operand", value=right_rule.strip()))
    elif "OR" in rule_string:
        left_rule, right_rule = rule_string.split("OR")
        return Node("operator", Node("operand", value=left_rule.strip()), Node("operand", value=right_rule.strip()))
    else:
        return Node("operand", value=rule_string.strip())

def combine_rules(rule_nodes):
    # Simplistic combination: AND the rules
    combined_node = rule_nodes[0]
    for node in rule_nodes[1:]:
        combined_node = Node("operator", left=combined_node, right=node)
    return combined_node

def evaluate_rule(ast, data):
    if ast.type == "operator":
        left_eval = evaluate_rule(ast.left, data)
        right_eval = evaluate_rule(ast.right, data)
        if "AND" in ast.value:
            return left_eval and right_eval
        elif "OR" in ast.value:
            return left_eval or right_eval
    elif ast.type == "operand":
        key, operator, value = ast.value.split()
        if operator == ">":
            return data[key] > int(value)
        elif operator == "<":
            return data[key] < int(value)
        elif operator == "=":
            return data[key] == value
    return False
