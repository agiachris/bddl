(define (problem packing_lunches_1)
    (:domain igibson)

    (:objects
     	box1 box2 - box
    	shelf1 - shelf
    	bag1 bag2 bag3 bag4 bag5 bag6 bag7 bag8 - bag
    	water1 water2 water3 water4 - water
    	counter1 - counter
    	apple1 apple2 apple3 apple4 - apple
    	fridge1 - fridge
    	hamburger1 hamburger2 hamburger3 hamburger4 - hamburger
    	plum1 plum2 plum3 plum4 - plum
    	dinner_napkin1 dinner_napkin2 dinner_napkin3 dinner_napkin4 - dinner_napkin
    	chocolate_box1 chocolate_box2 chocolate_box3 chocolate_box4 - chocolate_box
    	backpack1 backpack2 backpack3 backpack4 - backpack
    )
    
    (:init 
        (and 
            (ontop box1 shelf1) 
            (ontop box2 shelf1) 
            (and 
                (inside bag1 box1) 
                (under shelf1 bag1)
            ) 
            (and 
                (inside bag2 box1) 
                (under shelf1 bag2)
            ) 
            (and 
                (inside bag3 box1) 
                (under shelf1 bag3)
            ) 
            (and 
                (inside bag4 box1) 
                (under shelf1 bag4)
            ) 
            (and 
                (inside bag5 box1) 
                (under shelf1 bag5)
            ) 
            (and 
                (inside bag6 box1) 
                (under shelf1 bag6)
            ) 
            (and 
                (inside bag7 box1) 
                (under shelf1 bag7)
            ) 
            (and 
                (inside bag8 box1) 
                (under shelf1 bag8)
            )
        ) 
        (and 
            (ontop bottle1 counter1) 
            (ontop bottle2 counter1) 
            (ontop bottle3 counter1) 
            (ontop bottle4 counter1) 
        ) 
        (and 
            (inside apple1 fridge1) 
            (inside apple2 fridge1) 
            (inside apple3 fridge1) 
            (inside apple4 fridge1) 
            (inside hamburger1 fridge1) 
            (inside hamburger2 fridge1) 
            (inside hamburger3 fridge1) 
            (inside hamburger4 fridge1)
        ) 
        (and 
            (and 
                (inside plum1 box2) 
                (under shelf1 plum1)
            ) 
            (and 
                (inside plum2 box2) 
                (under shelf1 plum2)
            ) 
            (and 
                (inside plum3 box2) 
                (under shelf1 plum3)
            ) 
            (and 
                (inside plum4 box2) 
                (under shelf1 plum4)
            )
        ) 
        (and 
            (ontop dinner_napkin1 shelf1) 
            (ontop dinner_napkin2 shelf1) 
            (ontop dinner_napkin3 shelf1) 
            (ontop dinner_napkin4 shelf1) 
            (ontop chocolate_box1 shelf1) 
            (ontop chocolate_box2 shelf1) 
            (ontop chocolate_box3 shelf1) 
            (ontop chocolate_box4 shelf1)
        ) 
        (and 
            (ontop backpack1 counter1) 
            (ontop backpack2 counter1) 
            (ontop backpack3 counter1) 
            (ontop backpack4 counter1)
        ) 
        (inroom counter1 kitchen) 
        (inroom fridge1 kitchen) 
        (inroom shelf1 kitchen)
    )
    
    (:goal 
        (and 
            (forn 
                (4) 
                (?backpack - backpack) 
                (and 
                    (fornpairs 
                        (4) 
                        (?bag - bag) 
                        (?hamburger - hamburger) 
                        (and 
                            (inside ?hamburger ?bag) 
                            (inside ?bag ?backpack) 
                            (not 
                                (open ?bag)
                            )
                        )
                    ) 
                    (fornpairs 
                        (4) 
                        (?bag - bag) 
                        (?plum - plum) 
                        (and 
                            (inside ?plum ?bag) 
                            (inside ?bag ?backpack) 
                            (not 
                                (open ?bag)
                            )
                        )
                    )
                )
            ) 
            (fornpairs 
                (4) 
                (?backpack - backpack) 
                (?dinner_napkin - dinner_napkin) 
                (inside ?dinner_napkin ?backpack)
            ) 
            (fornpairs 
                (4) 
                (?backpack - backpack) 
                (?water - water) 
                (inside ?water ?backpack)
            ) 
            (fornpairs 
                (4) 
                (?backpack - backpack) 
                (?apple - apple) 
                (inside ?apple ?backpack)
            ) 
            (fornpairs 
                (4) 
                (?backpack - backpack) 
                (?chocolate_box - chocolate_box) 
                (inside ?chocolate_box ?backpack)
            ) 
            (forall 
                (?backpack - backpack) 
                (and 
                    (ontop ?backpack ?counter1) 
                    (not 
                        (open ?backpack)
                    )
                )
            )
        )
    )
)
