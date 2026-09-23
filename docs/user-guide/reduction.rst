Reducing spectrograms
=====================

The reduction pipeline turns calibrated or calibratable detector frames into
one-dimensional spectra for the individual fiber traces.

Core workflow
-------------

At a high level the pipeline performs:

#. detector calibration and masking;
#. trace localization;
#. extraction of each fiber spectrum;
#. wavelength calibration;
#. sky/background handling where an appropriate fiber or model is available;
#. optional combination of repeated exposures; and
#. production of spectra suitable for classification or subsequent analysis.

Masks and uncertainties
-----------------------

Bad or saturated pixels should be represented with masks rather than converted
to ``NaN`` simply to force downstream code to ignore them. The pipeline uses
CCD-style data containers so the data array, uncertainty, mask, and unit can
remain associated throughout processing.

When a masked pixel contributes no valid information to an extraction, the
output uncertainty/mask should communicate that fact. Avoid silently replacing
invalid measurements with apparently valid numerical values.

Trace extraction
----------------

The Level-1 extraction interface accepts known or measured trace centers and an
extraction half-width, together with detector gain and read-noise information
for uncertainty propagation. ``process_l1()`` currently performs boxcar
extraction. Horne/optimal extraction is available in the codebase but is not
currently selected by this Level-1 entry point; when enabled, it should use the
propagated variance rather than treating all spatial pixels equally.

Output rebinning and quicklooks
-------------------------------

Use the L1 ``--rebin N`` option when the stored spectra should combine ``N``
adjacent native dispersion pixels. Rebinning occurs after extraction: counts
are summed and uncertainties are combined in quadrature. Any incomplete group
at the trailing end of a trace is omitted, and the L1 FITS headers record both
the rebin factor and number of omitted pixels. This reduces the number of
stored samples but does not improve the instrument's spectral resolution.

Use ``--plot`` to write a quicklook PNG of all extracted traces beside the L1
FITS file. The plot reflects the data actually written to the product, including
any rebinning, and is intended for inspection rather than scientific analysis.

Multi-fiber products
--------------------

Keep per-fiber spectra distinct through the low-level reduction. A later stage
can decide which fibers represent target, sky, calibration, or other spatial
samples. This preserves the information required for a small integral-field
bundle and avoids hard-coding a permanent semantic role for a given fiber
number.

Validation with the simulator
-----------------------------

Synthetic detector images are valuable pipeline fixtures because their input
spectra and true trace geometry are known. Use them to verify extraction flux
conservation, wavelength mapping, trace separation, masking, and uncertainty
propagation before relying only on arc- or sky-lamp data.
