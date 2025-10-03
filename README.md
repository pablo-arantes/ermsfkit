eRMSF: A Python Package for Ensemble RMSF Analysis of Molecular Dynamics and Structural Ensembles
==============================

[//]: # (Badges)

| **Status**         | [![GH Actions Status][badge_actions]][url_actions]|
| :----------------- | :------- |
| **Community**      | [![License: GPL v2][badge_license]][url_license]  [![Powered by MDAnalysis][badge_mda]][url_mda]|

[badge_actions]: https://github.com/pablo-arantes/ermsfkit/actions/workflows/gh-ci.yaml/badge.svg
[badge_codecov]: https://codecov.io/gh/pablo-arantes/ermsfkit/branch/main/graph/badge.svg
[badge_commits_since]: https://img.shields.io/github/commits-since/pablo-arantes/ermsfkit/latest
[badge_docs]: https://readthedocs.org/projects/ermsfkit/badge/?version=latest
[badge_license]: https://img.shields.io/badge/License-GPLv2-blue.svg
[badge_mda]: https://img.shields.io/badge/powered%20by-MDAnalysis-orange.svg?logoWidth=16&logo=data:image/x-icon;base64,AAABAAEAEBAAAAEAIAAoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJD+XwCY/fEAkf3uAJf97wGT/a+HfHaoiIWE7n9/f+6Hh4fvgICAjwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACT/yYAlP//AJ///wCg//8JjvOchXly1oaGhv+Ghob/j4+P/39/f3IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJH8aQCY/8wAkv2kfY+elJ6al/yVlZX7iIiI8H9/f7h/f38UAAAAAAAAAAAAAAAAAAAAAAAAAAB/f38egYF/noqAebF8gYaagnx3oFpUUtZpaWr/WFhY8zo6OmT///8BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgICAn46Ojv+Hh4b/jouJ/4iGhfcAAADnAAAA/wAAAP8AAADIAAAAAwCj/zIAnf2VAJD/PAAAAAAAAAAAAAAAAICAgNGHh4f/gICA/4SEhP+Xl5f/AwMD/wAAAP8AAAD/AAAA/wAAAB8Aov9/ALr//wCS/Z0AAAAAAAAAAAAAAACBgYGOjo6O/4mJif+Pj4//iYmJ/wAAAOAAAAD+AAAA/wAAAP8AAABhAP7+FgCi/38Axf4fAAAAAAAAAAAAAAAAiIiID4GBgYKCgoKogoB+fYSEgZhgYGDZXl5e/m9vb/9ISEjpEBAQxw8AAFQAAAAAAAAANQAAADcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjo6Mb5iYmP+cnJz/jY2N95CQkO4pKSn/AAAA7gAAAP0AAAD7AAAAhgAAAAEAAAAAAAAAAACL/gsAkv2uAJX/QQAAAAB9fX3egoKC/4CAgP+NjY3/c3Nz+wAAAP8AAAD/AAAA/wAAAPUAAAAcAAAAAAAAAAAAnP4NAJL9rgCR/0YAAAAAfX19w4ODg/98fHz/i4uL/4qKivwAAAD/AAAA/wAAAP8AAAD1AAAAGwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALGxsVyqqqr/mpqa/6mpqf9KSUn/AAAA5QAAAPkAAAD5AAAAhQAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADkUFBSuZ2dn/3V1df8uLi7bAAAATgBGfyQAAAA2AAAAMwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB0AAADoAAAA/wAAAP8AAAD/AAAAWgC3/2AAnv3eAJ/+dgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9AAAA/wAAAP8AAAD/AAAA/wAKDzEAnP3WAKn//wCS/OgAf/8MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIQAAANwAAADtAAAA7QAAAMAAABUMAJn9gwCe/e0Aj/2LAP//AQAAAAAAAAAA
[badge_release]: https://img.shields.io/github/release-pre/pablo-arantes/ermsfkit.svg
[url_actions]: https://github.com/pablo-arantes/ermsfkit/actions?query=branch%3Amain+workflow%3Agh-ci
[url_codecov]: https://codecov.io/gh/pablo-arantes/ermsfkit/branch/main
[url_docs]: https://ermsfkit.readthedocs.io/en/latest/?badge=latest
[url_latest_release]: https://github.com/pablo-arantes/ermsfkit/releases
[url_license]: https://www.gnu.org/licenses/gpl-2.0
[url_mda]: https://www.mdanalysis.org

Here, we introduce eRMSF, a fast and user-friendly Python package built with MDKit from MD-Analysis, designed to perform ensemble-based Root Mean Square Fluctuation (RMSF) analyses. Users can easily customize atom, residue, or region selections, tailoring analyses to specific research questions. This approach delivers high-resolution insights into localized motions, complements global stability assessments, and reveals dynamic regions often overlooked by single-method analyses.

eRMSF is bound by a [Code of Conduct](https://github.com/pablo-arantes/ermsfkit/blob/main/CODE_OF_CONDUCT.md).

![alt text](https://github.com/pablo-arantes/ermsfkit/blob/main/TOC_eRMSF.png)


### Installation

Below we provide instructions both for `pip`.

#### With pip

To build the package from source, run:

```
pip install git+https://github.com/pablo-arantes/ermsfkit.git

or

git clone https://github.com/pablo-arantes/ermsfkit.git
pip install ermsfkit/
```
#### Usage
Below we provide an example of use:

```
from eRMSF import ermsfkit
import MDAnalysis as mda
import matplotlib.pyplot as plt
from MDAnalysis.tests.datafiles import PSF, DCD
from MDAnalysis.analysis import align

# Load the trajectory
u = mda.Universe(PSF, DCD)

# Align to the first frame (or average structure)
average = align.AverageStructure(u, u, select='protein and name CA',
                                 ref_frame=0).run()
ref = average.results.universe
align.AlignTraj(u, ref,
                select='protein and name CA',
                in_memory=True).run()

# Select the protein backbone (Cα atoms)
protein = u.select_atoms('protein and name CA')

# Initialize the eRMSF analysis
ermsf_analysis = ermsfkit(protein, skip=1, reference_frame=0)

# Run the analysis
ermsf_analysis.run()

# Extract results
results = ermsf_analysis.results.ermsf
```

### Copyright

The eRMSF source code is hosted at https://github.com/pablo-arantes/ermsfkit
and is available under the GNU General Public License, version 2 (see the file [LICENSE](https://github.com/pablo-arantes/ermsfkit/blob/main/LICENSE)).

Copyright (c) 2025, Pablo Arantes


#### Acknowledgements
 
Project based on the 
[MDAnalysis Cookiecutter](https://github.com/MDAnalysis/cookiecutter-mda) version 0.1.
Please cite [MDAnalysis](https://github.com/MDAnalysis/mdanalysis#citation) when using eRMSF in published work.
