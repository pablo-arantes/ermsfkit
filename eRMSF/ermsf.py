"""
ermsf.py
A package to perform time-dependent RMSF analysis on molecular dynamics data.

All code and documentation are modeled after the RMSF analysis class from the MDAnalysis Python package.
"""

from MDAnalysis.analysis.base import AnalysisBase
import numpy as np

class ermsf(AnalysisBase):
    r"""Calculate time-dependent RMSF of given atoms across a trajectory.

    Note
    ----
    No RMSD-superposition is performed; it is assumed that the user is
    providing a trajectory where the protein of interest has been structurally
    aligned to a reference structure. The protein also has be whole because
    periodic boundaries are not taken into account.

    Run the analysis with :meth:`ermsf.run`, which stores the results in the
    array :attr:`ermsf.results.ermsf`.

    """
    def __init__(self, atomgroup, skip=1, reference_frame=0, **kwargs):
        r"""Parameters
        ----------
        atomgroup : AtomGroup
            Atoms for which ermsf is calculated
        skip : int (optional)
            Number of frames to skip during the calculation, default is 1.
        reference_frame : int (optional)
            Frame number to use as reference for RMSF calculation, default is 0.
        verbose : bool (optional)
             Show detailed progress of the calculation if set to ``True``; the
             default is ``False``.

        Raises
        ------
        ValueError
             raised if negative values are calculated, which indicates that a
             numerical overflow or underflow occurred

        Notes
        -----
        The time-dependent root mean square fluctuation of an atom :math:`i` is computed as the
        time average over segments of the trajectory.

        .. math::

          \rho_i = \sqrt{\left\langle (\mathbf{x}_i - \langle\mathbf{x}_i\rangle)^2 \right\rangle}

        No mass weighting is performed. 
        
        This method implements an algorithm for computing sums of squares while
        avoiding overflows and underflows :cite:p:`Welford1962`.

        References
        ----------
        .. bibliography::
            :filter: False

            Welford1962

        """
        super(ermsf, self).__init__(atomgroup.universe.trajectory, **kwargs)
        self.atomgroup = atomgroup
        self.skip = skip
        self.reference_frame = reference_frame

    def _prepare(self):
        n_frames = len(self._trajectory[::self.skip])
        self.results.ermsf = np.zeros((n_frames, self.atomgroup.n_atoms))

        # Set the reference positions
        self._trajectory[self.reference_frame]
        self.reference_positions = self.atomgroup.positions.copy()

    def _single_frame(self):
        seg_num = self._frame_index // self.skip
        frame_index = self._frame_index % self.skip

        if frame_index == 0:
            self.avg_coordinates = np.zeros((self.atomgroup.n_atoms, 3))
            self.seg_length = 0

        # Accumulate coordinates for averaging
        self.avg_coordinates += (self.atomgroup.positions - self.reference_positions)**2
        self.seg_length += 1

        # At the end of a segment, calculate the RMSF
        if (frame_index + 1) == self.skip or self._frame_index == (len(self._trajectory) - 1):
            avg_coordinates = self.avg_coordinates / self.seg_length
            # diff = self.reference_positions - avg_coordinates
            rmsf = np.sqrt(np.sum(avg_coordinates, axis=1))
            self.results.ermsf[seg_num] = rmsf

    def _conclude(self):
        if not (self.results.ermsf >= 0).all():
            raise ValueError("Some RMSF values negative; overflow or underflow occurred")
        else:
            self.results.ermsf = self.results.ermsf.T

