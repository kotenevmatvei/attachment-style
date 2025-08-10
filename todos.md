- [x] test backend for ecr-r (simple click through)
- [x] calculate secure score from ecr-r scores for the dashboard graphs
- [x] let the database (backend) do the heavy lifting instead of the dashboard!
- [x] adjust assess others to 1-7 scale
- [x] generate test data for ecr-r

# backend
- [x] separate downloading image from showing the results!!! that's what takes so ultra long 
- [ ] provide total number of scores with and without test
- [ ] separate updating data from the db and filtering (include/exclude test, you/others)
      (then don't even need extra chaching)


# frontend
- [x] add scores legend to ecr-r graph (ugly for now)
    - [ ] center
    - [ ] color
    - [ ] font
- [ ] make slider ticks bigger
- [ ] add strongly disagree - neutral - strongly agree legend

- [ ] design new dashboard layout

# refactor
- [ ] separate callbacks
- [ ] separate database logic
