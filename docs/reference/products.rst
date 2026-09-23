Data products
=============

Raw detector frames
-------------------

Raw FITS files from the ICS are the authoritative acquisition products. Keep
all original headers and do not overwrite the raw files during reduction.

Calibrated detector frames
--------------------------

Pipeline calibration products should preserve data, unit, mask, and uncertainty
information together. The exact serialization can evolve, but the scientific
meaning of those components should remain explicit.

Extracted spectra
-----------------

The pipeline should retain one product per extracted fiber through the low-level
processing stages. A final science product can then associate fiber spectra with
roles or spatial positions according to the observation metadata.

The current L1 FITS product contains a primary HDU followed by one binary-table
HDU per trace. Each trace table contains ``PIXEL``, ``COUNTS``, ``SIGMA``, and
``MASK`` columns. ``PIXEL`` is the zero-based detector dispersion coordinate;
for rebinned products it is the mean native coordinate of each contributing
group. ``COUNTS`` is summed when rebinned and ``SIGMA`` is propagated in
quadrature.

The primary and trace headers record ``REBIN``, the number of native dispersion
pixels per output bin. Each trace header also records ``NTRIM``, the number of
trailing native pixels omitted because they did not form a complete bin, and
``EXTRACT=BOXCAR`` for the current Level-1 extraction path. A rebinned sample is
masked if any contributing native sample was masked.

Simulation products
-------------------

Synthetic detector frames should record enough simulator configuration to be
reproduced: physical spectrograph parameters, detector model, throughput data
versions, exposure time, random seed, and input-spectrum provenance.
