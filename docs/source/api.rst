.. _api:

=============
API Reference
=============

This section contains the full API documentation for eRMSF, automatically
generated from the source code docstrings.

Main Module
-----------

.. module:: eRMSF

The ``eRMSF`` package provides tools for time-dependent and ensemble RMSF
analysis of molecular dynamics trajectories.

ermsfkit Class
~~~~~~~~~~~~~~

.. autoclass:: eRMSF.ermsfkit
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:

   .. rubric:: Methods

   .. automethod:: __init__
   .. automethod:: run

   .. rubric:: Results

   After calling :meth:`run`, the results are accessible via:

   .. attribute:: results.ermsf

      A 2D NumPy array of shape ``(n_atoms, n_segments)`` containing the
      eRMSF values. Each row corresponds to an atom in the input
      :class:`~MDAnalysis.core.groups.AtomGroup`, and each column corresponds
      to a time segment.


Data Module
-----------

.. module:: eRMSF.data

The data subpackage provides access to bundled data files for testing.

.. automodule:: eRMSF.data.files
   :members:
   :undoc-members:
