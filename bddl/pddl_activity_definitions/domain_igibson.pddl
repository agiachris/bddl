(define (domain igibson)

    (:requirements 
        :strips 
        :adl    
    )

    (:types
        agent.n.01
        room
        floor.n.01
    )

    ;; constants parsed from predicates across all Behavior activities
    (:constants
        bathroom - room
        bedroom - room
        closet - room
        corridor - room
        dining_room - room
        garage - room
        home_office - room
        kitchen - room
        living_room - room
        storage_room - room
        utility_room - room
    )

    (:predicates
        ;; object properties - reflected in domain and problem file descriptions
        (broken ?obj1)
        (burnt ?obj1)
        (cooked ?obj1)
        (dusty ?obj1)
        (frozen ?obj1)
        (open ?obj1)
        (perished ?obj1)
        (screwed ?obj1)
        (stained ?obj1)
        (sliced ?obj1)
        (soaked ?obj1)
        (timeset ?obj1)
        (toggled_on ?obj1)
        
        ;; object properties - reflected in object class hierarchy's abilities
        (cleaning_tool ?obj1)
        (cold_source ?obj1)
        (heat_source ?obj1)
        (liquid ?obj1)
        (slicer ?obj1)
        (water_source ?obj1)

        ;; spatial predicates - reflected in domain and problem file descriptions
        (inroom ?obj1 ?obj2)        ; in initial states only
        (touching ?obj1 ?obj2)      ; in goal states only        
        (onfloor ?obj1 ?obj2)       ; in both initial and goal states
        (inside ?obj1 ?obj2)        ; from original domain_igibson.bddl 
        (nextto ?obj1 ?obj2)        ; from original domain_igibson.bddl 
        (ontop ?obj1 ?obj2)         ; from original domain_igibson.bddl 
        (under ?obj1 ?obj2)         ; from original domain_igibson.bddl 
    )

    (:action GoToRoom
        :parameters (?a - agent.n.01 ?rStart - room ?rEnd - room ?fStart - floor.n.01 ?fEnd - floor.n.01)
        :precondition (and 
            (inRoom ?agent ?)
        )
    )

    (:action GoToFloorFromRoom)

)
