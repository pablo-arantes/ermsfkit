.. _getting_started:

===============
Getting Started
===============

This guide will walk you through the basic usage of eRMSF for analyzing
the time-dependent flexibility of molecular dynamics trajectories.

Prerequisites
-------------

Before using eRMSF, make sure you have:

1. A molecular dynamics trajectory (e.g., ``.xtc``, ``.trr``, ``.dcd``)
2. A topology file (e.g., ``.pdb``, ``.gro``, ``.psf``)
3. The trajectory should be **aligned** to a reference structure (eRMSF does
   not perform RMSD superposition internally)
4. The protein should be **whole** (no broken molecules across periodic boundaries)

.. note::

   If your trajectory is not yet aligned, you can use MDAnalysis''s
   :class:`~MDAnalysis.analysis.align.AlignTraj` to perform the alignment
   before running eRMSF.


Basic Workflow
--------------

Step 1: Load your system
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import MDAnalysis as mda
   from eRMSF import ermsfkit

   # Load topology and trajectory
   u = mda.Universe("topology.pdb", "trajectory.xtc")

Step 2: Select atoms
~~~~~~~~~~~~~~~~~~~~

Select the atoms for which you want to calculate the eRMSF. Common selections
include C-alpha atoms or backbone atoms:

.. code-block:: python

   # C-alpha atoms only
   atoms = u.select_atoms("name CA")

   # Or backbone atoms
   atoms = u.select_atoms("backbone")

   # Or all protein atoms
   atoms = u.select_atoms("protein")

Step 3: Run the analysis
~~~~~~~~~~~~~~~~~~~~~~~~

Create an ``ermsfkit`` instance and run the analysis:

.. code-block:: python

   # Create the analysis object
   # skip=100 means each segment contains 100 frames
   # reference_frame=0 uses the first frame as reference
   ermsf = ermsfkit(atoms, skip=100, reference_frame=0)

   # Run the analysis
   ermsf.run()

Step 4: Access results
~~~~~~~~~~~~~~~~~~~~~~

The results are stored in ``ermsf.results.ermsf`` as a 2D NumPy array with
shape ``(n_atoms, n_segments)``:

.. code-block:: python

   import numpy as np

   # Get the eRMSF results
   results = ermsf.results.ermsf

   print(f"Shape: {results.shape}")
   print(f"Number of atoms: {results.shape[0]}")
   print(f"Number of time segments: {results.shape[1]}")

Step 5: Visualize results
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt

   fig, ax = plt.subplots(figsize=(10, 6))

   # Plot as a heatmap
   im = ax.imshow(
       results,
       aspect="auto",
       cmap="hot",
       origin="lower"
   )

   ax.set_xlabel("Time Segment")
   ax.set_ylabel("Residue Index")
   ax.set_title("eRMSF Over Time")
   plt.colorbar(im, ax=ax, label="eRMSF (Angstrom)")
   plt.tight_layout()
   plt.savefig("ermsf_heatmap.png", dpi=300)
   plt.show()


Understanding the Parameters
-----------------------------

``skip`` parameter
~~~~~~~~~~~~~~~~~~

The ``skip`` parameter determines the number of frames in each time segment.
This controls the temporal resolution of the analysis:

* **Small skip values** (e.g., 10-50): Higher temporal resolution, noisier results
* **Large skip values** (e.g., 500-1000): Lower temporal resolution, smoother results

Choose ``skip`` based on your trajectory length and the timescale of the
dynamics you want to capture.

``reference_frame`` parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``reference_frame`` parameter specifies which frame is used as the
reference for computing fluctuations:

* **reference_frame=0** (default): Uses the first frame as reference
* **Any integer**: Uses the specified frame index as reference

The choice of reference frame can significantly affect the results. Common
choices include:

* The first frame (initial structure)
* A frame representing the equilibrated state
* A representative frame from clustering


Next Steps
----------

* See :ref:`usage` for advanced examples and visualization techniques
* See :ref:`theory` for the mathematical background
* See :ref:`api` for the complete API reference
