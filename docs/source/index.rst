.. ermsfkit documentation master file

==============================================================
eRMSF: Ensemble RMSF Analysis for Molecular Dynamics
==============================================================

.. image:: https://img.shields.io/pypi/v/ermsfkit.svg
   :target: https://pypi.org/project/ermsfkit/
   :alt: PyPI version

.. image:: https://github.com/pablo-arantes/ermsfkit/actions/workflows/gh-ci.yaml/badge.svg
   :target: https://github.com/pablo-arantes/ermsfkit/actions/workflows/gh-ci.yaml
   :alt: CI Status

.. image:: https://readthedocs.org/projects/ermsfkit/badge/?version=latest
   :target: https://ermsfkit.readthedocs.io/en/latest/
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-GPLv2-blue.svg
   :target: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
   :alt: License: GPL v2

.. image:: https://img.shields.io/badge/Powered%20by-MDAnalysis-orange.svg
   :target: https://www.mdanalysis.org
   :alt: Powered by MDAnalysis

**eRMSF** (ensemble Root Mean Square Fluctuation) is a Python package for
performing time-dependent and ensemble RMSF analysis on molecular dynamics
trajectories and structural ensembles.

Unlike the standard RMSF, which averages atomic fluctuations over an entire
trajectory relative to the mean structure, the eRMSF partitions the trajectory
into time segments and computes fluctuations relative to a user-defined
reference frame. This enables the study of how protein flexibility evolves
over simulation time or across ensemble members.

Key Features
------------

* **Time-resolved flexibility analysis** -- Partition trajectories into segments
  and track how RMSF evolves over simulation time.
* **Reference-frame flexibility** -- Compute fluctuations relative to any
  user-defined reference frame (not just the average structure).
* **MDAnalysis integration** -- Built on top of the `MDAnalysis
  <https://www.mdanalysis.org>`_ analysis framework for seamless integration
  with existing MD analysis workflows.
* **Numerically stable** -- Uses Welford's algorithm to maintain numerical
  stability during computation.
* **Flexible input** -- Works with any trajectory format supported by MDAnalysis
  (PDB, XTC, TRR, DCD, and many more).

Quick Example
-------------

.. code-block:: python

   import MDAnalysis as mda
   from eRMSF import ermsfkit

   # Load your trajectory
   u = mda.Universe("topology.pdb", "trajectory.xtc")

   # Select atoms of interest
   atoms = u.select_atoms("name CA")

   # Run eRMSF analysis with 100-frame segments
   ermsf = ermsfkit(atoms, skip=100, reference_frame=0)
   ermsf.run()

   # Access results (shape: n_atoms x n_segments)
   results = ermsf.results.ermsf

.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   getting_started
   usage
   theory
   api
   changelog
   contributing


Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
