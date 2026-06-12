.. _theory:

======================
Theoretical Background
======================

This section provides the mathematical foundations of the eRMSF method.

Standard RMSF
-------------

The standard Root Mean Square Fluctuation (RMSF) of atom :math:`i` over a
trajectory is defined as:

.. math::

   \text{RMSF}_i = \sqrt{ \frac{1}{T} \sum_{t=1}^{T}
   \left( \mathbf{x}_i(t) - \langle \mathbf{x}_i \rangle \right)^2 }

where:

* :math:`\mathbf{x}_i(t)` is the position vector of atom :math:`i` at time :math:`t`
* :math:`\langle \mathbf{x}_i \rangle = \frac{1}{T} \sum_{t=1}^{T} \mathbf{x}_i(t)`
  is the time-averaged position
* :math:`T` is the total number of frames

The standard RMSF provides a single value per atom that represents the overall
flexibility averaged over the entire trajectory. It loses all temporal information.


Ensemble RMSF (eRMSF)
----------------------

The ensemble or time-dependent RMSF (eRMSF) extends the standard RMSF by
computing fluctuations over temporal segments relative to a user-defined
reference frame.

For atom :math:`i` in time segment :math:`s`, the eRMSF is:

.. math::

   \rho_i^{(s)} = \sqrt{ \frac{1}{N_s} \sum_{t \in s}
   \left( \mathbf{x}_i(t) - \mathbf{x}_i^{\text{ref}} \right)^2 }

where:

* :math:`\mathbf{x}_i^{\text{ref}}` is the position of atom :math:`i` in the
  reference frame
* :math:`N_s` is the number of frames in segment :math:`s`
* The sum runs over all frames :math:`t` belonging to segment :math:`s`

The squared deviation is computed component-wise:

.. math::

   \left( \mathbf{x}_i(t) - \mathbf{x}_i^{\text{ref}} \right)^2 =
   \sum_{\alpha \in \{x,y,z\}} \left( x_{i,\alpha}(t) - x_{i,\alpha}^{\text{ref}} \right)^2


Trajectory Segmentation
-----------------------

Given a trajectory with :math:`T` total frames and a segment size (``skip``)
of :math:`S` frames, the trajectory is divided into :math:`\lceil T/S \rceil`
segments:

.. math::

   \text{Segment } s = \{ t : (s-1) \cdot S \leq t < s \cdot S \}

The last segment may contain fewer than :math:`S` frames if :math:`T` is not
evenly divisible by :math:`S`.


Output Structure
----------------

The eRMSF analysis produces a 2D array with dimensions:

* **Rows**: Atoms (size = number of selected atoms :math:`N`)
* **Columns**: Time segments (size = :math:`\lceil T/S \rceil`)

.. math::

   \mathbf{R} \in \mathbb{R}^{N \times M}

where :math:`M = \lceil T/S \rceil` is the number of segments.


Relationship to Standard RMSF
------------------------------

The eRMSF reduces to a standard RMSF-like quantity when:

* ``skip`` = total number of frames (single segment)
* ``reference_frame`` is set to a representative structure

However, unlike standard RMSF which uses the **time-averaged** position as
reference, eRMSF uses a **specific frame** as reference. This makes it
particularly suitable for:

* Detecting conformational transitions
* Identifying time-dependent changes in flexibility
* Comparing flexibility across different simulation conditions


Numerical Stability
-------------------

The implementation uses a numerically stable accumulation scheme for computing
sums of squares. Rather than computing the mean first and then the variance,
coordinates are accumulated incrementally to minimize floating-point errors
that can arise with large datasets.

If any computed eRMSF value is negative (which indicates numerical
overflow or underflow), a :class:`ValueError` is raised to alert the user.


Interpretation Guidelines
--------------------------

* **High eRMSF values**: Indicate large atomic fluctuations relative to the
  reference frame. These regions are flexible or undergo large conformational
  changes.

* **Low eRMSF values**: Indicate atoms that remain close to their positions
  in the reference frame. These regions are structurally rigid.

* **Temporal variation in eRMSF**: If a residue shows increasing eRMSF over
  time segments, it suggests progressive structural deviation (e.g.,
  conformational drift or unfolding).

* **Sudden changes in eRMSF**: May indicate conformational transitions,
  ligand binding/unbinding events, or domain movements.


References
----------

.. [Welford1962] Welford, B. P. (1962). Note on a Method for Calculating
   Corrected Sums of Squares and Products. *Technometrics*, 4(3), 419-420.
   doi:10.1080/00401706.1962.10490022

.. [MDAnalysis2016] Michaud-Agrawal, N., Denning, E. J., Woolf, T. B., &
   Beckstein, O. (2011). MDAnalysis: A toolkit for the analysis of molecular
   dynamics simulations. *J. Comput. Chem.*, 32(10), 2319-2327.
   doi:10.1002/jcc.21787
