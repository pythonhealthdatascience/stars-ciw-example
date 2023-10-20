[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pythonhealthdatascience/stars-ciw-examplar/HEAD)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Read the Docs](https://readthedocs.org/projects/pip/badge/?version=latest)](https://pythonhealthdatascience.github.io/stars-ciw-examplar/)
[![License: MIT](https://img.shields.io/badge/ORCID-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0001-5274-5037)
[![License: MIT](https://img.shields.io/badge/ORCID-0000--0003--2631--4481-brightgreen)](https://orcid.org/0000-0003-2631-4481)

#   Towards Sharing Tools and Artifacts for Reuable Simulation: a `ciw` model examplar

## Overview

The materials and methods in this repository support work towards developing the S.T.A.R.S healthcare framework (**S**haring **T**ools and **A**rtifacts for **R**eusable **S**imulations in healthcare).  The code and written materials here demonstrate the application of S.T.A.R.S' version 1 to sharing a `ciw` discrete-event simuilation model and associated research artifacts.  

* All artifacts in this repository are linked to study researchers via ORCIDs;
* Model code is made available under a GNU Public License version 3;
* Python dependencies are managed through `conda`;`
* The code builds a Shiny for Python web application that can be used to run the model (web app);
* The python code itself can be viewed and executed in Jupyter notebooks via [Binder](https://mybinder.org); 
* The model is documented and explained in a quarto website served up by GitHub pages;
* The materials are deposited and made citatable using Zenodo;
* The models are sharable with other researchers and the NHS without the need to install software.

## Author ORCIDs

[![ORCID: Harper](https://img.shields.io/badge/ORCID-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0001-5274-5037)
[![ORCID: Monks](https://img.shields.io/badge/ORCID-0000--0003--2631--4481-brightgreen)](https://orcid.org/0000-0003-2631-4481)

## Funding

This code is part of independent research supported by the National Institute for Health Research Applied Research Collaboration South West Peninsula. The views expressed in this publication are those of the author(s) and not necessarily those of the National Institute for Health Research or the Department of Health and Social Care.

## Shiny web app

The `ciw` model has been given a Shiny for Python interface.  This allows users to easily experiment with the simulation model.  The web app is hosted on a free tier of shinyapps.io.  The app can be access at [https://pythonhealthdatascience.shinyapps.io/stars-ciw-examplar](https://pythonhealthdatascience.shinyapps.io/stars-ciw-examplar)

> This is a free service. If the app has not been used for a while it will be "asleep" to save resources. Please be patient while the app "wakes up".  This will be a short time.

## Online Notebooks via Binder

The python code for the model has been setup to run online in Jupyter notebooks via binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pythonhealthdatascience/stars-ciw-examplar/HEAD)

> Binder is a free service.  If it has not been used in a while Binder will need to re-containerise the code repository, and push to binderhub. This will take several minutes. After that the online environment will be quick to load.

## Online documentation produced by Quarto

[![Read the Docs](https://readthedocs.org/projects/pip/badge/?version=latest)](https://pythonhealthdatascience.github.io/stars-ciw-examplar/)

* Visit our [quarto website](https://pythonhealthdatascience.github.io/stars-ciw-examplar/) for detailed overview of the project, and code: https://pythonhealthdatascience.github.io/stars-ciw-examplar

## How to run the model locally

Alternatively you may wish to run the Shiny App locally on your own machine.  

### Downloading the code

Either clone the repository using git or click on the green "code" button and select "Download Zip".

```bash
git clone https://github.com/pythonhealthdatascience/stars-ciw-examplar
```

### Installing dependencies

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

All dependencies can be found in [`binder/environment.yml`]() and are pulled from conda-forge.  To run the code locally, we recommend install [mini-conda](https://docs.conda.io/en/latest/miniconda.html); navigating your terminal (or cmd prompt) to the directory containing the repo and issuing the following command:

```bash
conda env create -f binder/environment.yml
```

To activate the environment issue the following command:

```bash
conda activate stars_pyshiny`
```

### Launching the Shiny Interface

In the directory (folder) containing the code issue the following command via the terminal (or cmd prompt/powershell on windows)

```bash
shiny run app.py
```

The app will run locally on port 8000 and can be accessed using the following URL

```
http://127.0.0.1:8000
```

