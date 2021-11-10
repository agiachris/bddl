from copy import Error
import re
import os
import json
import os.path as osp
from bddl.object_taxonomy import ObjectTaxonomy
from bddl.parsing import parse_domain, parse_problem
from bddl.config import get_definition_filename
from bddl.converter import convert_goal_state
from igibson.object_states.factory import get_states_by_dependency_order
from pddlgym.parser import (PDDLDomain, PDDLProblemParser, Operator)
from pddlgym.structs import *


DOMAIN = 'igibson'
ROOT_DIR = osp.dirname(osp.realpath(__file__))
PDDL_ROOT = osp.join(ROOT_DIR, 'pddl_activity_definitions')
# observed in BDDL domains / problems & object taxonomy / class abilities
_MATCHED_ABILITIES = {                 
    "breakable": "broken",
    "burnable": "burnt",
    "cookable": "cooked",
    "dustyable": "dusty",
    "freezable": "frozen", 
    "openable": "open",
    "perishable": "perished",
    "screwable": "screwed",
    "sliceable": "sliced",
    "soakable": "soaked", 
    "stainable": "stained", 
    "timeSetable": "timeset", 
    "toggleable": "toggled_on",
}
# only observed in object taxonomy / class abilities
_UNMATCHED_ABILITIES = {
    "cleaningTool": "cleaning_tool",
    "coldSource": "cold_source",
    "heatSource": "heat_source",
    "liquid": "liquid",
    "slicer": "slicer",
    "waterSource": "water_source"
}
_UNARY_PROPERTIES = {
    **_MATCHED_ABILITIES, **_UNMATCHED_ABILITIES
}
_UNARY_PROPERTIES_INV = {v: k for k, v in _UNARY_PROPERTIES.items()}

# only observed in BDDL domains / problems
_TWOARY_PROPERTIES = {
    "inroom": "in_room",
    "inside": "inside",
    "nextto": "next_to",
    "onfloor": "on_floor",
    "ontop": "on_top",
    "touching": "touching",
    "under": "under"
}


def get_pddl_problem_fname(activity, instance):
    fname = get_definition_filename(activity, instance)
    return 'pddl_' + osp.splitext(fname)[0] + '.pddl'


def get_pddl_problems(root=PDDL_ROOT):
    activities = [(osp.join(PDDL_ROOT, act), act) for act in os.listdir(PDDL_ROOT) if act != 'domain_igibson.pddl']
    problems = [(osp.join(act[0], inst), int(re.search(r"\d+", inst).group())) for act in activities 
                            for inst in os.listdir(act[0])]
    problem_fnames = [x[0] for x in problems]
    activity_names = [x[-1] for x in activities]
    inst_ids = [x[-1] for x in problems]
    return problem_fnames, activity_names, inst_ids


def get_goal_state_predicates_recurse(x, predicates):
    for i in range(len(x)):
        if isinstance(x[i], list):
            get_goal_state_predicates_recurse(x[i], predicates)
        else:
            is_logical = x[i] in ["forall", "or", "not", "exists", "and"]
            is_variable = x[i][0] == '?'
            is_separator = x[i] == '-'
            is_object = re.search("n\.", x[i]) is not None
            if not (is_logical or is_variable or is_separator or is_object):
                predicates.add(x[i])


class BehaviorPDDLConstructor:

    def __init__(self, abstract_plan=True, hierarchy_type='all', ig_properties=True):
        self.taxonomy = ObjectTaxonomy(hierarchy_type=hierarchy_type)
        class_to_ability_path = osp.realpath(osp.join(ROOT_DIR, '../utils/synsets_to_filtered_properties.json'))
        if ig_properties:
            class_to_ability_path = class_to_ability_path.replace(".json", "_pruned_igibson.json") 
        with open(class_to_ability_path, 'r') as fp:
            self.class_to_ability_map = json.load(fp)

        # pddlgym.parser.PDDLDomain relatesd objects
        self.types = dict()                 # dict<str type_name, pddlgym.structs.Type type>
        self.type_hierarchy = dict()        # dict<pddlgym.structs.Type type, list<pddlgym.structs.Type type>>
        self.parse_types()

        self.constants = list()             # list<str constants>
        self.predicates = dict()            # dict<predicate_name, pddlgym.structs.Predicate predicate>
        self.type_to_predicate_map = dict() # dict<str type_name, str unary_predicate_name>
        self.parse_predicates()

        self.operators = dict()             # dict<str operator_name, pddlgym.parser.Operator operator>
        self.generate_operators(abstract_plan)

    def write_domain(self, filepath):
        """Write PDDL domain file to filepath with the current set of
        types, type_hierarchy, constants, and predicates
        """
        pddl_domain = PDDLDomain(
            domain_name=DOMAIN, 
            types=self.types, 
            type_hierarchy=self.type_hierarchy, 
            predicates=self.predicates,
            operators=self.operators,
            constants=self.constants,
            operators_as_actions=False
        )
        pddl_domain.write(filepath)
        
    def parse_types(self):
        """Acquire all object types specified in the iGibson taxonomy.
        """
        # construct types
        for _class in self.class_to_ability_map:
            self.types[_class] = Type(_class)

        for _class in self.taxonomy.taxonomy.nodes():
            if _class not in self.types:
                self.types[_class] = Type(_class)    
        
        # construct type hierachy
        for _class in self.types:
            if _class in self.taxonomy.taxonomy.nodes():
                self.type_hierarchy[self.types[_class]] = [self.types[_child_class] for _child_class in self.taxonomy.get_children(_class)]
            else:
                self.type_hierarchy[self.types[_class]] = list()
        
    def parse_predicates(self):
        """Parse class-specified abilities (e.g., affordances) into unary and twoary predicates.
        """
        # parse object-cemtric affordances from object taxonomy / class to ability map
        abilities = set()
        for _class in self.class_to_ability_map:
            self.type_to_predicate_map[_class] = list()
            for _ability in self.class_to_ability_map[_class]:
                assert _ability in _UNARY_PROPERTIES and _ability not in _TWOARY_PROPERTIES
                abilities.add(_ability)
                self.type_to_predicate_map[_class].append(_UNARY_PROPERTIES[_ability])
                
        for _class in self.taxonomy.get_leaf_descendants("entity.n.01"):
            if _class not in self.type_to_predicate_map:
                self.type_to_predicate_map[_class] = list()
            for _ability in self.taxonomy.get_abilities(_class):
                assert _ability in _UNARY_PROPERTIES and _ability not in _TWOARY_PROPERTIES
                abilities.add(_ability)
                # avoid double counting properties
                if _UNARY_PROPERTIES[_ability] not in self.type_to_predicate_map[_class]:
                    self.type_to_predicate_map[_class].append(_UNARY_PROPERTIES[_ability])
        
        for _ability in abilities:
            self.predicates[_UNARY_PROPERTIES[_ability]] = Predicate(_UNARY_PROPERTIES[_ability], 1)
        
        # parse for unary / twoary properties observed in the BDDL database (Behavior 100)
        constants = set()
        domain_predicates = set(parse_domain(DOMAIN)[4].keys())
        problem_predicates = set()
        _, activities, instances = get_pddl_problems()
        for a, i in zip(activities, instances):
            _, objects, initial_state, goal_state = parse_problem(a, i, DOMAIN)
            for x in initial_state:
                if x[0] == "not":
                    x = x[1]                

                problem_predicates.add(x[0])
                constants.update(set([c for c in x[1:] if re.search("n\.", c) is None]))
                if len(x) == 2:
                    _type = x[1].split('_')[:-1]
                    if not isinstance(_type, str):
                        temp = ""
                        sep = "_"
                        for s in _type:
                            if ".n." in s:
                                sep = ""
                            temp += s
                            temp += sep
                        _type = temp
                    assert _type in self.types
                    assert x[0] in self.type_to_predicate_map[_type]
                
            # TODO: assert that predicates grounded over objects in goals are valid w.r.t. self.type_to_predicate_map
            convert_goal_state(goal_state, objects)
            get_goal_state_predicates_recurse(goal_state, problem_predicates)
        behavior_predicates = domain_predicates | problem_predicates

        # store behavior constants and predicates unspecified in object taxonomy / class to ability map
        self.constants = list(constants)
        for _predicate in behavior_predicates:
            arity = 1
            if _predicate in _UNARY_PROPERTIES_INV:
                _ability = _UNARY_PROPERTIES_INV[_predicate]
                if _ability in abilities:
                    continue
            elif _predicate in _TWOARY_PROPERTIES:
                arity += 1
                _predicate = _TWOARY_PROPERTIES[_predicate]
            else:
                print(f"Undefined predicate {_predicate} used in BDDL domain or activity definitions")
                exit(1)
            self.predicates[_predicate] = Predicate(_predicate, arity)

    def generate_operators(abstract_plan):
        """Generate the domain operators (aka., actions) when:
        (a) abstract_plan = True: operators correspond to abstract task definitions; i.e., lifted tasks
        (b) abstract_plan = False: operators correspond to tasks fully grounded in the iGibson simulator
        """
        # TODO: implement operators for tasks fully grounded on iGibson2.0 states            
        assert abstract_plan
        
        self.operators["PickUp"] = Operator(
            
        )

        

def main():
    parser = BehaviorPDDLConstructor()
    parser.write_domain('./igibson_test_domain.pddl')


if __name__ == '__main__':
    print("\n")
    main()

    