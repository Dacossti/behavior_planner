;; domain/domain.pddl
;; Title: Rich House Domain for Move, Pick‑Up, and Put‑Down

(define (domain house)
  (:requirements :strips :typing)
  
  (:types
    agent object location
  )

  (:predicates
    (at         ?a - agent    ?l - location)    ;; agent’s current room
    (at-object  ?o - object   ?l - location)    ;; object’s current location
    (holding    ?a - agent    ?o - object)      ;; agent is holding object
    (placed     ?o - object   ?l - location)    ;; object has been placed
    (empty-hand ?a - agent)                     ;; agent’s hand is free
  )

  ;; Move from one room to another
  (:action move
    :parameters (?a - agent ?from - location ?to - location)
    :precondition  (and (at ?a ?from))
    :effect        (and (not (at ?a ?from)) (at ?a ?to))
  )

  ;; Pick up an object at the current location
  (:action pick-up
    :parameters (?a - agent ?o - object ?l - location)
    :precondition  (and (at ?a ?l) (at-object ?o ?l) (empty-hand ?a))
    :effect        (and (holding ?a ?o)
                        (not (at-object ?o ?l))
                        (not (empty-hand ?a)))
  )

  ;; Put an object down at the current location
  (:action put-down
    :parameters (?a - agent ?o - object ?l - location)
    :precondition  (and (at ?a ?l) (holding ?a ?o))
    :effect        (and (placed ?o ?l)
                        (empty-hand ?a)
                        (not (holding ?a ?o)))
  )
)