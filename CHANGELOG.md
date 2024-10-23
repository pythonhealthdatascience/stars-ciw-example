# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Dates formatted as YYYY-MM-DD as per [ISO standard](https://www.iso.org/iso-8601-date-and-time-format.html).

Consistent identifier (represents all versions, resolves to latest): [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10055168.svg)](https://doi.org/10.5281/zenodo.10055168)

## Unreleased

Improvements and corrections to the app and documentation. Updated some packages in environment.

### Added

* Created and backdated changelog

### Changed

* Update packages for app in environments (i.e. `shiny`, `shinyswatch`, `shinywidgets`, `rsconnect0python`, `faicons`)
* Modifications to the app including:
    * Modified code to be compatible with new package versions
    * Add modal with some context about STARS
    * Add STARS logo and buttons to link to GitHub and docs
    * Simplified appearance of inputs, add tooltips, and increased default replications
    * Improved display of results by removing columns, adding titles with tooltips, using full metric names, and adding axis titles to the graph
    * Add model summary with logic diagram to "About" page, and corrected links
* Minor tweaks to documentation including:
    * Correcting links (eg. to fix BinderHub link, and correcting to new repo and application names)
    * Spelling and grammar
    * Import `environment.yml` to display exact software versions in docs
    * Add GitHub action to automatically build book

## [v1.0.1](https://github.com/pythonhealthdatascience/stars-ciw-example/releases/tag/v1.0.1) - 2023-10-29 - [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10051495.svg)](https://doi.org/10.5281/zenodo.10051495)

Updated `README.md`.

### Added

* PATCH: added description of case study model to README.md

## [v1.0.0](https://github.com/pythonhealthdatascience/stars-ciw-example/releases/tag/v1.0.0) - 2023-10-29

Release created for submission to Journal of Simulation.

### Added

* CIW model (`ciw_model.py`)
* CIW model documentation (`mysite/`)
* CIW model application (`app.py` and associated files e.g. `rsconnect-python/`)
* Environments (`requirements.txt`, `environment.yml`) with support for binder