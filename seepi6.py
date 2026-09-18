class ForwardChaining:
    def __init__(self, rules, facts):
        self.rules = rules
        self.facts = facts
    def apply_rules(self):
        inferred = set(self.facts)
        new_inferred = True
        while new_inferred:
            new_inferred = False
            for rule in self.rules:
                if rule["if"].issubset(inferred) and not rule["then"].issubset(inferred):
                    inferred.update(rule["then"])
                    new_inferred = True
        return inferred
# Define some rules
rules = [
    {"if": {"A"}, "then": {"B"}},
    {"if": {"B"}, "then": {"C"}},
    {"if": {"C"}, "then": {"D"}}
]
# Define initial facts
facts = {"A"}
# Create forward chaining object
fc = ForwardChaining(rules, facts)
# Apply rules to infer new facts
inferred_facts = fc.apply_rules()
print("Inferred facts:", inferred_facts)




