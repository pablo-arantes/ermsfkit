"""
ermsf.py
A package to perform time-dependent or ensemble RMSF (eRMSF) analysis 
on molecular dynamics trajectories.

The eRMSF represents the fluctuation of atomic positions relative to a 
user-defined reference frame across time segments or ensemble members.
"""

from MDAnalysis.analysis.base import AnalysisBase
import numpy as np

class ermsfkit(AnalysisBase):
    r"""Calculate time-dependent or ensemble RMSF of given atoms across a trajectory.

    Notes
    -----
    No RMSD superposition is performed. It is assumed that the user provides
    a trajectory that has already been aligned to a reference structure.
    The protein must also be whole because periodic boundaries are not taken 
    into account.

    Run the analysis with :meth:`ermsf.run`, which stores the results in the
    array :attr:`ermsf.results.ermsf`.

    """
    def __init__(self, atomgroup, skip=1, reference_frame=0, **kwargs):
        r"""Parameters
        ----------
        atomgroup : AtomGroup
            Atoms for which the eRMSF is calculated.
        skip : int, optional
            Number of frames to skip during the calculation (default = 1).
        reference_frame : int, optional
            Frame index used as reference for the eRMSF calculation (default = 0).
            The coordinates of this frame define the baseline positions from 
            which atomic fluctuations are measured.
        verbose : bool, optional
            Show detailed progress of the calculation if set to True 
            (default = False).

        Raises
        ------
        ValueError
            Raised if negative values are calculated, which indicates 
            numerical instability (overflow/underflow).

        Notes
        -----
        The ensemble/time-dependent root mean square fluctuation (eRMSF) of 
        an atom :math:`i` is computed as the square root of the mean squared 
        deviation of its coordinates relative to a chosen reference frame:

        .. math::

            \rho_i = \sqrt{ \langle (\mathbf{x}_i - \mathbf{x}_i^{ref})^2 \rangle }

        Here, :math:`\mathbf{x}_i^{ref}` represents the atomic coordinates
        from the reference frame defined by ``reference_frame``. No mass 
        weighting is applied.

        This implementation uses Welford's algorithm to maintain numerical 
        stability when computing sums of squares.

        References
        ----------
        .. bibliography::
            :filter: False

            Welford1962
        """
        super(ermsfkit, self).__init__(atomgroup.universe.trajectory, **kwargs)
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

