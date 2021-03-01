
(:goal 
    (and 
        (forpairs 
            (?plate - plate) 
            (?chair - chair) 
            (and 
                (ontop ?plate ?table1 
                    (dining_room)) 
                (nextto ?plate ?chair)
            )
        ) 
        (forpairs 
            (?bowl - bowl) 
            (?chair - chair) 
            (and 
                (ontop ?bowl ?table1 
                    (dining_room)) 
                (nextto ?bowl ?chair)
            )
        ) 
        (forpairs 
            (?fork - fork) 
            (?plate - plate) 
            (and 
                (ontop ?fork ?table1 
                    (dining_room)) 
                (nextto ?fork ?plate)
            )
        ) 
        (forpairs 
            (?knife - knife) 
            (?plate - plate) 
            (and 
                (ontop ?knife ?table1 
                    (dining_room)) 
                (nextto ?knife ?plate)
            )
        ) 
        (forpairs 
            (?spoon - spoon) 
            (?plate - plate) 
            (and 
                (ontop ?spoon ?table1 
                    (dining_room)) 
                (nextto ?spoon ?plate)
            )
        ) 
        (forall 
            (?tenderloin - tenderloin) 
            (cooked ?tenderloin)
        ) 
        (forpairs 
            (?tenderloin - tenderloin) 
            (?plate - plate) 
            (ontop ?tenderloin ?plate)
        ) 
        (forall 
            (?gazpacho - gazpacho) 
            (not 
                (frozen ?gazpacho)
            )
        ) 
        (forpairs 
            (?gazpacho - gazpacho) 
            (?bowl - bowl) 
            (inside ?gazpacho ?bowl)
        )
    )
)