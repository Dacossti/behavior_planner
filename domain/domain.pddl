(define (domain house-tasks)
  (:requirements :strips :typing)
  
  (:types 
    agent object location
  )

  (:predicates
    (at ?a - agent ?l - location)
    (at-object ?o - object ?l - location)
    (holding ?a - agent ?o - object)
    (empty-hand ?a - agent)
  )

  (:action move
    :parameters (?a - agent ?from - location ?to - location)
    :precondition (and (at ?a ?from))
    :effect (and (not (at ?a ?from)) (at ?a ?to))
  )

  (:action pick-up
    :parameters (?a - agent ?o - object ?l - location)
    :precondition (and (at ?a ?l) (at-object ?o ?l) (empty-hand ?a))
    :effect (and (holding ?a ?o) (not (at-object ?o ?l)) (not (empty-hand ?a)))
  )

  (:action put-down
    :parameters (?a - agent ?o - object ?l - location)
    :precondition (and (at ?a ?l) (holding ?a ?o))
    :effect (and (at-object ?o ?l) (empty-hand ?a) (not (holding ?a ?o)))
  )
)