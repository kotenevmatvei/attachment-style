- make links on home page work
- add personal questions such as age, gender, profession, etc.
- update models
- create the chart
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