To Do:
- create the chart
  - make subject dynamic
  - make choice of gender vs therapy_experience vs relationship_status dynamic
  - create the page
  - add dropdowns
  - setup the callback
- translate
- add feedback survey
- migrate to github
- migrate to koyeb with a docker image
  - move pie-chart and report.pdf to output folder
  - setup the docker image with crom job to clean up the output folder every day or hour
  - host the docker image on koyeb
  - setup continuous deployment with github actions
- refactor
  - clean up code
  - optimize question upddate
  - clean up dependencies (by creating a fresh env and adding what needed one by one)
  - style