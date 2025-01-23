; THIS DOMAIN IS USED IN ADDITIONAL TASK #1

(define (domain zum-task2)
    (:requirements :strips)
    (:predicates
        (seaman ?seaman)
        (location ?location)
        
        (forest ?forest)
        (river ?river)
        (harbour ?harbour)
        (tavern ?tavern)
        (city ?city)
        (academy ?academy)
        (sea ?sea)
        (lighthouse ?lighthouse)
        (island ?island)
        
        (to_sober_up ?location)
        
        ; needed to sail
        (ship ?ship)
        
        ; needed to build bigger ships
        (boat ?boat)
        (fregate ?fregate)
        (caravel ?caravel)
    
        ; needed to distinguish different items
        (seed ?golden_seed)
        (coin ?golden_coin)
        (brick ?golden_brick)
        (wood ?wood)
        (leather ?leather)
        (alcohol ?alcohol)
        (flowers ?flowers)
        (map ?map)
        (pearl ?pearl)
        (coconut ?coconut)
        (cocaine ?cocaine)
        (ring ?ring)
        
        (sellable ?what)
    
        ; seaman here is like a container with items
        (at ?where ?what)
        (path_on_earth ?from ?to)
        (path_on_water ?from ?to)
        
        (drank)
        (drunk)
        (addicted)
        
        (strengthened)
        (convicted)
        
        (badly_acquainted)
        (well_acquainted)
        
        (defeated_a_bear)
        (defeated_pirates)
        
        (is_captain)
        (is_pirate)
        
        (knows_contrabandists)
        (amazed_a_girl)
        
        (endpoint_reached)
    )
    
    ; ----------------------------- MOVING -----------------------------
    
    (:action move_on_earth
        :parameters (?seaman ?loc_1 ?loc_2)
        :precondition (and
            (seaman ?seaman)
            (location ?loc_1)
            (location ?loc_2)
        
            (at ?loc_1 ?seaman)
            (not (at ?loc_2 ?seaman))
            (path_on_earth ?loc_1 ?loc_2)
        )
        :effect (and 
            (at ?loc_2 ?seaman)
            (not (at ?loc_1 ?seaman))
        )
    )
    
    (:action move_on_water
        :parameters (?seaman ?loc_1 ?loc_2 ?ship)
        :precondition (and
            (seaman ?seaman)
            (location ?loc_1)
            (location ?loc_2)
            (ship ?ship)
        
            (at ?loc_1 ?seaman)
            (at ?seaman ?ship)
            (not (at ?loc_2 ?seaman))
            (path_on_water ?loc_1 ?loc_2)
        )
        :effect (and 
            (at ?loc_2 ?seaman)
            (not (at ?loc_1 ?seaman))
        )
    )
    
    ; ----------------------------- CRAFTING -----------------------------
    
    (:action make_boat
        :parameters (?seaman ?wood ?boat)
        :precondition (and
            (seaman ?seaman)
            (wood ?wood)
            (boat ?boat)
        
            (at ?seaman ?wood)
        )
        :effect (and
            (at ?seaman ?boat)
            (not (at ?seaman ?wood))
        )
    )
    
    (:action make_fregate
        :parameters (?seaman ?boat ?wood ?golden_seed ?fregate)
        :precondition (and
            (seaman ?seaman)
            (wood ?wood)
            (seed ?golden_seed)
            (boat ?boat)
            (fregate ?fregate)
        
            (at ?seaman ?boat)
            (at ?seaman ?wood)
            (at ?seaman ?golden_seed)
        )
        :effect (and
            (at ?seaman ?fregate)
            (not (at ?seaman ?boat))
            (not (at ?seaman ?wood))
            (not (at ?seaman ?golden_seed))
        )
    )
    
    (:action make_caravel
        :parameters (?seaman ?boat ?wood ?golden_coin ?caravel)
        :precondition (and
            (seaman ?seaman)
            (boat ?boat)
            (wood ?wood)
            (coin ?golden_coin)
            (caravel ?caravel)
        
            (at ?seaman ?boat)
            (at ?seaman ?wood)
            (at ?seaman ?golden_coin)
        )
        :effect (and
            (at ?seaman ?caravel)
            (not (at ?seaman ?boat))
            (not (at ?seaman ?wood))
            (not (at ?seaman ?golden_coin))
        )
    )
    
    (:action make_ring
        :parameters (?seaman ?golden_brick ?pearl ?ring)
        :precondition (and
            (seaman ?seaman)
            (brick ?golden_brick)
            (pearl ?pearl)
            (ring ?ring)
            
            (at ?seaman ?golden_brick)
            (at ?seaman ?pearl)
        )
        :effect (and
            (not (at ?seaman ?golden_brick))
            (not (at ?seaman ?pearl))
            (at ?seaman ?ring)
        )
    )
    
    ; ----------------------------- DRINKING -----------------------------
    
    (:action drink_a_little
        :parameters (?seaman ?alcohol)
        :precondition (and
            (seaman ?seaman)
            (alcohol ?alcohol)
        
            (not (drank))
            (at ?seaman ?alcohol)
        )
        :effect (and
            (drank)
            (not (at ?seaman ?alcohol))
        )
    )
    
    (:action drink_again
        :parameters (?seaman ?alcohol)
        :precondition (and
            (seaman ?seaman)
            (alcohol ?alcohol)
        
            (drank)
            (not (drunk))
            (at ?seaman ?alcohol)
        )
        :effect (and
            (drunk)
            (not (at ?seaman ?alcohol))
        )
    )
    
    (:action become_addicted
        :parameters (?seaman ?alcohol)
        :precondition (and
            (seaman ?seaman)
            (alcohol ?alcohol)
        
            (drunk)
            (not (addicted))
            (at ?seaman ?alcohol)
        )
        :effect (and
            (addicted)
            (not (at ?seaman ?alcohol))
        )
    )
    
    ; ----------------------------- FOREST -----------------------------
    
    (:action gain_wood_forest
        :parameters (?seaman ?forest ?wood)
        :precondition (and
            (seaman ?seaman)
            (forest ?forest)
            (wood ?wood)
            
            (at ?forest ?seaman)
        )
        :effect (and
            (at ?seaman ?wood)
        )
    )
    
    (:action gain_flowers
        :parameters (?seaman ?forest ?flowers)
        :precondition (and
            (seaman ?seaman)
            (forest ?forest)
            (flowers ?flowers)
            
            (at ?forest ?seaman)
        )
        :effect (and
            (at ?seaman ?flowers)
        )
    )
    
    (:action fight_a_bear
        :parameters (?seaman ?forest ?leather)
        :precondition (and
            (seaman ?seaman)
            (forest ?forest)
            (leather ?leather)
            
            (at ?forest ?seaman)
        )
        :effect (and
            (at ?seaman ?leather)
            (strengthened)
            (defeated_a_bear)
        )
    )
    
    (:action meet_a_wizard
        :parameters (?seaman ?forest ?alcohol ?map)
        :precondition (and
            (seaman ?seaman)
            (forest ?forest)
            (alcohol ?alcohol)
            (map ?map)
            
            (at ?forest ?seaman)
            (at ?seaman ?alcohol)
        )
        :effect (and
            (not (at ?seaman ?alcohol))
            (at ?seaman ?map)
            (badly_acquainted)
        )
    )
    
    ; ----------------------------- RIVER -----------------------------
    
    (:action steal_a_boat
        :parameters (?seaman ?river ?boat)
        :precondition (and
            (seaman ?seaman)
            (river ?river)
            (boat ?boat)
            
            (at ?river ?seaman)
        )
        :effect (and
            (at ?seaman ?boat)
            (convicted)
        )
    )
    
    (:action gain_seed
        :parameters (?seaman ?river ?golden_seed)
        :precondition (and
            (seaman ?seaman)
            (river ?river)
            (seed ?golden_seed)
            
            (at ?river ?seaman)
        )
        :effect (and
            (at ?seaman ?golden_seed)
        )
    )
    
    (:action sober_up  ; river or sea
        :parameters (?seaman ?where)
        :precondition (and
            (seaman ?seaman)
            (to_sober_up ?where)
            
            (at ?where ?seaman)
            (drank)
        )
        :effect (and
            (not (drank))
            (not (drunk))
        )
    )
    
    ; ----------------------------- HARBOUR -----------------------------
    
    (:action work_in_the_harbour
        :parameters (?seaman ?harbour ?golden_seed)
        :precondition (and
            (seaman ?seaman)
            (harbour ?harbour)
            (seed ?golden_seed)
            
            (at ?harbour ?seaman)
        )
        :effect (and
            (at ?seaman ?golden_seed)
        )
    )
    
    (:action sell_something
        :parameters (?seaman ?harbour ?what ?golden_coin)
        :precondition (and
            (seaman ?seaman)
            (harbour ?harbour)
            (sellable ?what)
            (coin ?golden_coin)
            
            (at ?harbour ?seaman)
            (at ?seaman ?what)
        )
        :effect (and
            (at ?seaman ?golden_coin)
            (not (at ?seaman ?what))
        )
    )
    
    (:action meet_contrabandists
        :parameters (?seaman ?harbour ?golden_brick)
        :precondition (and
            (seaman ?seaman)
            (harbour ?harbour)
            (brick ?golden_brick)
            
            (at ?harbour ?seaman)
            (at ?seaman ?golden_brick)
            (badly_acquainted)
        )
        :effect (and
            (knows_contrabandists)
        )
    )
    
    ; ----------------------------- TAVERN -----------------------------
    
    (:action buy_alcohol
        :parameters (?seaman ?tavern ?alcohol ?golden_seed)
        :precondition (and
            (seaman ?seaman)
            (tavern ?tavern)
            (alcohol ?alcohol)
            (seed ?golden_seed)
            
            (at ?tavern ?seaman)
            (at ?seaman ?golden_seed)
        )
        :effect (and
            (at ?seaman ?alcohol)
            (not (at ?seaman ?golden_seed))
        )
    )
    
    (:action buy_alcohol_for_everyone
        :parameters (?seaman ?tavern ?golden_coin)
        :precondition (and
            (seaman ?seaman)
            (tavern ?tavern)
            (coin ?golden_coin)
            
            (at ?tavern ?seaman)
            (at ?seaman ?golden_coin)
        )
        :effect (and
            (not (at ?seaman ?golden_coin))
            (well_acquainted)
        )
    )
    
    (:action fight_in_the_tavern
        :parameters (?seaman ?tavern)
        :precondition (and
            (seaman ?seaman)
            (tavern ?tavern)
            
            (at ?tavern ?seaman)
            (drank)
        )
        :effect (and
            (strengthened)
        )
    )
    
    ; ----------------------------- CITY -----------------------------
    
    (:action save_gold
        :parameters (?seaman ?city ?golden_seed ?golden_coin)
        :precondition (and
            (seaman ?seaman)
            (city ?city)
            (seed ?golden_seed)
            (coin ?golden_coin)
            
            (at ?city ?seaman)
            (at ?seaman ?golden_seed)
        )
        :effect (and
            (at ?seaman ?golden_coin)
            (not (at ?seaman ?golden_seed))
            (well_acquainted)
        )
    )
    
    (:action invest_gold
        :parameters (?seaman ?city ?golden_coin ?golden_brick)
        :precondition (and
            (seaman ?seaman)
            (city ?city)
            (coin ?golden_coin)
            (brick ?golden_brick)
            
            (at ?city ?seaman)
            (at ?seaman ?golden_coin)
        )
        :effect (and
            (at ?seaman ?golden_brick)
            (not (at ?seaman ?golden_coin))
            (well_acquainted)
        )
    )
    
    (:action steal_gold
        :parameters (?seaman ?city ?golden_coin)
        :precondition (and
            (seaman ?seaman)
            (city ?city)
            (coin ?golden_coin)
            
            (at ?city ?seaman)
        )
        :effect (and
            (at ?seaman ?golden_coin)
            (convicted)
        )
    )
    
    (:action remove_conviction_buy
        :parameters (?seaman ?city ?golden_seed)
        :precondition (and
            (seaman ?seaman)
            (city ?city)
            (seed ?golden_seed)
            
            (at ?city ?seaman)
            (at ?seaman ?golden_seed)
            (convicted)
        )
        :effect (and
            (not (convicted))
            (not (at ?seaman ?golden_seed))
        )
    )
    
    (:action remove_conviction_work
        :parameters (?seaman ?city)
        :precondition (and
            (seaman ?seaman)
            (city ?city)
            
            (at ?city ?seaman)
            (convicted)
        )
        :effect (and
            (not (convicted))
            (drank)
        )
    )
    
    ; ----------------------------- ACADEMY -----------------------------
    
    (:action become_captain
        :parameters (?seaman ?academy ?golden_coin) 
        :precondition (and
            (seaman ?seaman)
            (academy ?academy)
            (coin ?golden_coin)
            
            (at ?academy ?seaman)
            (at ?seaman ?golden_coin)
            (not (convicted))
        )
        :effect (and
            (is_captain)
            (not (at ?seaman ?golden_coin))
        )
    )
    
    ; ----------------------------- SEA -----------------------------
    
    (:action gain_pearl
        :parameters (?seaman ?sea ?pearl)
        :precondition (and
            (seaman ?seaman)
            (sea ?sea)
            (pearl ?pearl)
            
            (at ?sea ?seaman)
        )
        :effect (and
            (at ?seaman ?pearl)
        )
    )
    
    (:action become_pirate
        :parameters (?seaman ?sea)
        :precondition (and
            (seaman ?seaman)
            (sea ?sea)
            
            (at ?sea ?seaman)
            (badly_acquainted)
        )
        :effect (and
            (is_pirate)
            (drank)
        )
    )
    
    (:action lose_to_pirates
        :parameters (?seaman ?sea ?golden_seed ?golden_coin ?golden_brick ?boat ?fregate ?caravel)
        :precondition (and
            (seaman ?seaman)
            (sea ?sea)
            (seed ?golden_seed)
            (coin ?golden_coin)
            (brick ?golden_brick)
            (boat ?boat)
            (fregate ?fregate)
            (caravel ?caravel)
            
            (at ?sea ?seaman)
            (not (strengthened))
        )
        :effect (and
            (strengthened)
            (not (at ?seaman ?golden_seed))
            (not (at ?seaman ?golden_coin))
            (not (at ?seaman ?golden_brick))
            (at ?seaman ?boat)
            (not (at ?seaman ?fregate))
            (not (at ?seaman ?caravel))
        )
    )
    
    (:action defeat_pirates
        :parameters (?seaman ?sea ?golden_seed ?golden_coin ?golden_brick ?boat ?fregate ?caravel)
        :precondition (and
            (seaman ?seaman)
            (sea ?sea)
            (seed ?golden_seed)
            (coin ?golden_coin)
            (brick ?golden_brick)
            (boat ?boat)
            (fregate ?fregate)
            (caravel ?caravel)
            
            (at ?sea ?seaman)
            (at ?seaman ?caravel)
            (strengthened)
        )
        :effect (and
            (at ?seaman ?boat)
            (at ?seaman ?fregate)
            (at ?seaman ?golden_seed)
            (at ?seaman ?golden_coin)
            (at ?seaman ?golden_brick)
            (defeated_pirates)
        )
    )
    
    ; ----------------------------- LIGHTHOUSE -----------------------------
    
    (:action amaze_a_girl_captain
        :parameters (?seaman ?lighthouse)
        :precondition (and
            (seaman ?seaman)
            (lighthouse ?lighthouse)
            
            (at ?lighthouse ?seaman)
            (is_captain)
        )
        :effect (and
            (amazed_a_girl)
        )
    )
    
    (:action amaze_a_girl_bear
        :parameters (?seaman ?lighthouse)
        :precondition (and
            (seaman ?seaman)
            (lighthouse ?lighthouse)
            
            (at ?lighthouse ?seaman)
            (defeated_a_bear)
        )
        :effect (and
            (amazed_a_girl)
        )
    )
    
    (:action amaze_a_girl_pirates
        :parameters (?seaman ?lighthouse)
        :precondition (and
            (seaman ?seaman)
            (lighthouse ?lighthouse)
            
            (at ?lighthouse ?seaman)
            (defeated_pirates)
        )
        :effect (and
            (amazed_a_girl)
        )
    )
    
    ; ----------------------------- ISLAND -----------------------------
    
    (:action gain_wood_island
        :parameters (?seaman ?island ?wood)
        :precondition (and
            (seaman ?seaman)
            (island ?island)
            (wood ?wood)
            
            (at ?island ?seaman)
        )
        :effect (and
            (at ?seaman ?wood)
        )
    )
    
    (:action gain_coconut
        :parameters (?seaman ?island ?coconut)
        :precondition (and
            (seaman ?seaman)
            (island ?island)
            (coconut ?coconut)
            
            (at ?island ?seaman)
        )
        :effect (and
            (at ?seaman ?coconut)
        )
    )
    
    (:action gain_cocaine
        :parameters (?seaman ?island ?map ?cocaine)
        :precondition (and
            (seaman ?seaman)
            (island ?island)
            (map ?map)
            (cocaine ?cocaine)
            
            (at ?island ?seaman)
            (at ?seaman ?map)
        )
        :effect (and
            (at ?seaman ?cocaine)
        )
    )
    
    ; ----------------------------- ENDPOINTS -----------------------------
    
    (:action marriage_ending
        :parameters (?seaman ?island ?ring ?flowers)
        :precondition (and
            (seaman ?seaman)
            (island ?island)
            (ring ?ring)
            (flowers ?flowers)
        
            (at ?island ?seaman)
            (amazed_a_girl)
            (at ?seaman ?ring)
            (at ?seaman ?flowers)
            (well_acquainted)
            (not (convicted))
            (not (drank))
            (not (drunk))
            (not (addicted))
        )
        :effect (and
            (endpoint_reached)
        )
    )
    
    (:action admiral_ending
        :parameters (?seaman ?academy)
        :precondition (and
            (seaman ?seaman)
            (academy ?academy)
            
            (is_captain)
            (defeated_pirates)
            (at ?academy ?seaman)
            (not (drank))
            (not (drunk))
            (not (addicted))
        )
        :effect (and
            (endpoint_reached)
        )
    )
    
    (:action cocaine_ending
        :parameters (?seaman ?cocaine ?fregate ?golden_brick)
        :precondition (and
            (seaman ?seaman)
            (cocaine ?cocaine)
            (fregate ?fregate)
            (brick ?golden_brick)
            
            (at ?seaman ?cocaine)
            (at ?seaman ?fregate)
            (at ?seaman ?golden_brick)
            (addicted)
            (knows_contrabandists)
        )
        :effect (and
            (endpoint_reached)
        )
    )
)

