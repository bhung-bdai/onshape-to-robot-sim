# OnShape to Robot (SDF/URDF)

<p align="center">
<img src="docs/source/_static/img/main.png" />
</p>

This tool is based on the [OnShape API](https://dev-portal.onshape.com/) to retrieve
informations from an assembly and build an SDF or URDF model suitable for physics
simulation.

You will also need to install gazebo and sdformat to get this to work, unfortunately. You can do that by 
changing to this directory and then running:
```./install.sh```

### Using the package
Go into the `onshape_to_sim` folder, modify the appropriate values inside the `run_onshape_to_sim.py`, and then run
```python run_onshape_to_sim.py```

For a detailed explanation on how to use this, please see the Notion page on the BDAII page documenting the state of this package.
