(define (problem pick-and-place-cup)
  (:domain house-tasks)

  (:objects
    agent1 - agent
    cup1 - object
    table counter kitchen doorway - location
  )

  (:init
    (at agent1 doorway)
    (at-object cup1 table)
    (empty-hand agent1)
  )

  (:goal
    (and
      (at agent1 kitchen)
      (at-object cup1 counter)
    )
  )
)