.. _usage:

==============
Usage Examples
==============

This page provides detailed usage examples for different analysis scenarios.

Basic eRMSF Analysis
--------------------

The simplest use case: computing the time-dependent RMSF for C-alpha atoms.

.. code-block:: python

   import MDAnalysis as mda
   from eRMSF import ermsfkit
   import numpy as np

   # Load system
   u = mda.Universe("topology.pdb", "trajectory.xtc")
   atoms = u.select_atoms("name CA")

   # Run with 100-frame segments
   ermsf = ermsfkit(atoms, skip=100, reference_frame=0)
   ermsf.run()

   # Results shape: (n_atoms, n_segments)
   print(ermsf.results.ermsf.shape)


Analyzing Specific Regions
--------------------------

You can focus the analysis on specific protein regions:

.. code-block:: python

   # Analyze a specific chain
   chain_A = u.select_atoms("name CA and segid A")
   ermsf_chainA = ermsfkit(chain_A, skip=100)
   ermsf_chainA.run()

   # Analyze a loop region (residues 50-70)
   loop = u.select_atoms("name CA and resid 50:70")
   ermsf_loop = ermsfkit(loop, skip=50)
   ermsf_loop.run()

   # Analyze the binding site
   binding_site = u.select_atoms("name CA and (resid 120:135 or resid 200:215)")
   ermsf_binding = ermsfkit(binding_site, skip=100)
   ermsf_binding.run()


Comparing Different Reference Frames
-------------------------------------

The choice of reference frame affects the analysis. Compare different references:

.. code-block:: python

   # Reference frame = first frame
   ermsf_first = ermsfkit(atoms, skip=100, reference_frame=0)
   ermsf_first.run()

   # Reference frame = middle of trajectory
   mid_frame = len(u.trajectory) // 2
   ermsf_mid = ermsfkit(atoms, skip=100, reference_frame=mid_frame)
   ermsf_mid.run()

   # Reference frame = last frame
   ermsf_last = ermsfkit(atoms, skip=100, reference_frame=-1)
   ermsf_last.run()


Visualization: Heatmap
-----------------------

Create a publication-quality heatmap of the eRMSF:

.. code-block:: python

   import matplotlib.pyplot as plt

   fig, ax = plt.subplots(figsize=(12, 6))

   resids = atoms.resids

   im = ax.imshow(
       ermsf.results.ermsf,
       aspect="auto",
       cmap="YlOrRd",
       origin="lower",
       interpolation="nearest",
   )

   ax.set_xlabel("Time Segment", fontsize=12)
   ax.set_ylabel("Residue ID", fontsize=12)
   ax.set_title("Time-Dependent eRMSF", fontsize=14)

   cbar = plt.colorbar(im, ax=ax)
   cbar.set_label("eRMSF (Angstrom)", fontsize=12)

   plt.tight_layout()
   plt.savefig("ermsf_heatmap.png", dpi=300, bbox_inches="tight")
   plt.show()


Visualization: Per-Residue Time Series
---------------------------------------

Plot the eRMSF time evolution for specific residues:

.. code-block:: python

   fig, ax = plt.subplots(figsize=(10, 5))

   residues_of_interest = [25, 50, 100, 150]
   results = ermsf.results.ermsf

   for res_idx, resid in enumerate(residues_of_interest):
       idx = np.where(atoms.resids == resid)[0]
       if len(idx) > 0:
           ax.plot(results[idx[0], :], label=f"Res {resid}")

   ax.set_xlabel("Time Segment")
   ax.set_ylabel("eRMSF (Angstrom)")
   ax.set_title("eRMSF Time Evolution for Selected Residues")
   ax.legend()
   plt.tight_layout()
   plt.show()


Visualization: Average eRMSF Profile
--------------------------------------

Compare the time-averaged eRMSF with standard RMSF:

.. code-block:: python

   avg_ermsf = np.mean(ermsf.results.ermsf, axis=1)
   std_ermsf = np.std(ermsf.results.ermsf, axis=1)

   fig, ax = plt.subplots(figsize=(12, 5))
   ax.plot(atoms.resids, avg_ermsf, "b-", label="Mean eRMSF")
   ax.fill_between(
       atoms.resids,
       avg_ermsf - std_ermsf,
       avg_ermsf + std_ermsf,
       alpha=0.3,
       color="blue",
       label="+/- 1 SD"
   )
   ax.set_xlabel("Residue ID")
   ax.set_ylabel("eRMSF (Angstrom)")
   ax.set_title("Average eRMSF Profile")
   ax.legend()
   plt.tight_layout()
   plt.show()


Choosing the Segment Size
--------------------------

The ``skip`` parameter controls the temporal resolution:

.. code-block:: python

   segment_sizes = [10, 50, 100, 200, 500]

   fig, axes = plt.subplots(1, len(segment_sizes), figsize=(20, 5), sharey=True)

   for ax, skip_val in zip(axes, segment_sizes):
       ermsf_test = ermsfkit(atoms, skip=skip_val, reference_frame=0)
       ermsf_test.run()

       im = ax.imshow(
           ermsf_test.results.ermsf,
           aspect="auto",
           cmap="hot",
           origin="lower"
       )
       ax.set_title(f"skip={skip_val}")
       ax.set_xlabel("Segment")

   axes[0].set_ylabel("Atom Index")
   plt.suptitle("Effect of Segment Size on eRMSF", fontsize=14)
   plt.tight_layout()
   plt.show()


Saving Results
--------------

Save the eRMSF results for further analysis:

.. code-block:: python

   # Save as NumPy array
   np.save("ermsf_results.npy", ermsf.results.ermsf)

   # Save as CSV
   np.savetxt(
       "ermsf_results.csv",
       ermsf.results.ermsf,
       delimiter=",",
       header="Columns are time segments, rows are atoms"
   )

   # Load previously saved results
   loaded_results = np.load("ermsf_results.npy")


Trajectory Pre-processing
--------------------------

Before running eRMSF, ensure your trajectory is properly prepared:

.. code-block:: python

   from MDAnalysis.analysis import align

   ref = mda.Universe("reference.pdb")
   u = mda.Universe("topology.pdb", "trajectory.xtc")

   alignment = align.AlignTraj(
       u,
       ref,
       select="backbone",
       filename="aligned_trajectory.xtc"
   )
   alignment.run()

   u_aligned = mda.Universe("topology.pdb", "aligned_trajectory.xtc")
   atoms = u_aligned.select_atoms("name CA")

   ermsf = ermsfkit(atoms, skip=100, reference_frame=0)
   ermsf.run()


Integration with B-factor Coloring
------------------------------------

Map eRMSF values onto the structure for visualization in molecular viewers:

.. code-block:: python

   avg_ermsf = np.mean(ermsf.results.ermsf, axis=1)

   u.trajectory[0]
   atoms.tempfactors = avg_ermsf

   atoms.write("ermsf_colored.pdb")
   # Open in PyMOL/VMD and color by B-factor to visualize flexibility
