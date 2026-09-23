Observation lifecycle
=====================

The following sequence is the intended mental model for using the complete
instrument, from a proposed target to a calibrated spectrum. The detailed
operator sequence belongs in :doc:`observing`; this page emphasizes the
handoffs between planning, telescope operation, hardware, and reduction.

Before the night
----------------

#. Obtain a representative target or transient template spectrum.
#. Use the ETC to scale it to the expected target magnitude and estimate the
   exposure time needed in the diagnostic wavelength region.
#. Confirm that the ETC configuration represents the planned fiber, filter,
   grating, camera mode, focus/aperture assumptions, and sky conditions.
#. If the target is near a sensitivity limit or trace-overlap behavior matters,
   run the simulator with the same instrument geometry and exposure time.
#. Inspect the simulated detector frame and, when useful, run it through the
   pipeline as a pre-observation sanity check.

At the telescope
----------------

#. Start the ICS with the deployment configuration appropriate to the
   observatory host.
#. Verify science-camera, focus, guide-camera/stage, and telescope status.
#. Confirm the as-operated filter, grating, aperture, focus, detector, and fiber
   configuration, and ensure those states are recorded in the observing log or
   FITS metadata.
#. Acquire calibration data required by the pipeline configuration.
#. Acquire science exposures using the ETC result as the starting exposure
   time, adjusting for actual conditions when needed.
#. Inspect the current FITS frame in the ICS interface, but retain the original
   raw files as the authoritative data products.

After acquisition
-----------------

#. Process the detector calibrations.
#. Review the raw-frame metadata and observing log before assigning calibrations
   or combining exposures.
#. Trace and boxcar-extract every useful fiber with the current Level-1 path;
   use Horne/optimal extraction only when explicitly selecting that available
   implementation.
#. Apply wavelength calibration and propagate masks and uncertainties.
#. Perform sky/background subtraction at a stage that preserves the individual
   fiber measurements needed for quality control.
#. Combine exposures only after verifying trace registration and calibration
   consistency.
#. Export or analyze the final one-dimensional spectra.

Reproducibility
---------------

Record the versions (or Git commit hashes) of the ETC, simulator, pipeline, and
``classi-shared-data`` distribution used for an observation or simulation
campaign. A change to a throughput curve can alter both the ETC prediction and
the simulator even when no Python source code changes.

Also retain the deployed ICS version, the instrument configuration, and the
identity of the calibration products applied in reduction. Reproducibility
depends on the as-operated hardware state as well as the software stack.
