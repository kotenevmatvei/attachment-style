To Do:
- test data
  <!-- - speed up test upload by uploading all objects at the end -->
  <!-- - create a more even distribution -->
- chart
  - finish the test-data (make it reflect all the expected distributions)
  - add the density plot
  - cluster analysis - normal 3d scatter plot
  - add the option include/exclude test data from the plot
  - embed it into layout as page
  - style
- translate
- add feedback survey - how and where to store?
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
    - fold navbar automatically on click
  - document special features
  - document what i learned
