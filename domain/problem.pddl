;; domain/problem.pddl
;; Title: Set‑the‑Table Task

(define (problem set-the-table)
  (:domain house)

  ;; Declared objects and locations in this scenario
  (:objects
    agent1           - agent
    Plate1 Cup1      - object
    LivingRoom       Kitchen DiningRoom Table Counter  - location
  )

  ;; Initial world state
  (:init
    (at agent1 LivingRoom)
    (at-object Plate1 Table)
    (at-object Cup1 Table)
    (empty-hand agent1)
  )

  ;; Goal: Agent in DiningRoom & both items placed on the Counter
  (:goal
    (and
      (at agent1 DiningRoom)
      (placed Plate1 Counter)
      (placed Cup1 Counter)
    )
  )
)