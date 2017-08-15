# viz

Dependencies: Docker

This directory has all the artifacts for re-generating graphs. We use Python
Notebooks to visualize the results, which are in `../experiments`. 

```
./jupyter.sh
```

This will pull a Docker container with Jupyter, the packages for running Python
Notebooks. When it is running, point your browser at `localhost:81` and open the file
`visualize/viz-nano.ipynb`.
