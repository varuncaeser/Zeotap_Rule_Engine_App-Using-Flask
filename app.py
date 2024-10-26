from flask import Flask, request, jsonify, render_template
from ast_engine import create_rule, combine_rules, evaluate_rule
from database import db, Rule

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def create_new_rule():
    rule_string = request.json['rule']
    rule_node = create_rule(rule_string)
    rule = Rule(rule_string=rule_string, ast_data=str(rule_node))  # Simplified AST storage
    db.session.add(rule)
    db.session.commit()
    return jsonify({'message': 'Rule created successfully!', 'rule': rule_string})

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    rule_ids = request.json['rule_ids']
    rules = Rule.query.filter(Rule.id.in_(rule_ids)).all()
    combined_ast = combine_rules([create_rule(rule.rule_string) for rule in rules])
    return jsonify({'message': 'Rules combined successfully!', 'combined_ast': str(combined_ast)})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate():
    rule_id = request.json['rule_id']
    rule = Rule.query.get(rule_id)
    data = request.json['data']
    ast = create_rule(rule.rule_string)
    result = evaluate_rule(ast, data)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
