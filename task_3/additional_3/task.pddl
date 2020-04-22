; THIS IS THE ADDITIONAL TASK #3 - THERE WON'T BE A PEARL IN THE SEA

(define (problem planning)
    (:domain zum-task2)
    (:requirements :strips)
    (:objects
        seaman
    
        forest river harbour tavern city academy sea lighthouse island
        
        boat fregate caravel
        
        golden_seed golden_coin golden_brick
        
        wood leather alcohol flowers map coconut pearl cocaine ring
    )
    (:init
        (seaman seaman)
        
        (location forest)
        (location river)
        (location harbour)
        (location tavern)
        (location city)
        (location academy)
        (location sea)
        (location lighthouse)
        (location island)
        
        (forest forest)
        (river river)
        (harbour harbour)
        (tavern tavern)
        (city city)
        (academy academy)
        (sea sea)
        (lighthouse lighthouse)
        (island island)
        
        (to_sober_up river)
        (to_sober_up sea)
        
        (ship boat)
        (ship fregate)
        (ship caravel)
        
        (boat boat)
        (fregate fregate)
        (caravel caravel)
        
        (seed golden_seed)
        (coin golden_coin)
        (brick golden_brick)
        
        (wood wood)
        (alcohol alcohol)
        (flowers flowers)
        (map map)
        (pearl pearl)
        (cocaine cocaine)
        (ring ring)
        
        (sellable leather)
        (sellable coconut)
        
        (path_on_earth forest river)
        (path_on_earth river forest)
        (path_on_earth river harbour)
        (path_on_earth harbour river)
        (path_on_earth harbour tavern)
        (path_on_earth tavern harbour)
        (path_on_earth harbour city)
        (path_on_earth city harbour)
        (path_on_earth city academy)
        (path_on_earth academy city)
        
        (path_on_water harbour sea)
        (path_on_water sea harbour)
        (path_on_water harbour lighthouse)
        (path_on_water lighthouse harbour)
        (path_on_water sea lighthouse)
        (path_on_water lighthouse sea)
        (path_on_water sea island)
        (path_on_water island sea)
        
        (at harbour seaman)
    )
    (:goal (and
            (endpoint_reached)
        )
    )
)

