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
output uncertainty/mask should communicate that fact. The pipeline should not
silently replace invalid measurements with apparently valid numerical values.

Trace extraction
----------------

The Level-1 extraction interface accepts known or measured trace centers and an
extraction half-width, together with detector gain and read-noise information
for uncertainty propagation. ``process_l1()`` performs boxcar extraction.

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

Wavelength calibration
----------------------

The Level-2 library represents the baseline wavelength calibration as one
versioned ASDF reference file containing a ``WavelengthSolution1D`` for every
fiber trace. A maintainer supplies matched arc-line pixels and wavelengths to
``fit_arc_wavelength_solution()``, reviews the stored residuals and RMS
diagnostics, and writes the accepted trace set with ``write_wavesol()``.

All calibration pixels use zero-based native detector coordinates. This remains
true for rebinned Level-1 spectra because their ``PIXEL`` column stores the mean
native coordinate of each output sample. The ASDF metadata explicitly records
the wavelength unit and whether wavelengths are in air or vacuum; vacuum is the
fit default.

For a science exposure, ``fit_sky_refinement()`` can align measured night-sky
line centroids with a baseline arc solution. One line constrains a shift; two or
more can constrain a shift and dispersion stretch. Sky-line detection and
centroiding are separate responsibilities so the reduction workflow can choose
an appropriate sky fiber or combined sky spectrum.

These functions provide the calibration-reference and fitting machinery.
``process_l2()`` does not apply them to Level-1 files, and no Level-2 science
FITS format or command-line workflow is defined.

Multi-fiber products
--------------------

Keep per-fiber spectra distinct through the low-level reduction. A later stage
can decide which fibers represent target, sky, calibration, or other spatial
samples. This preserves the information required for a small integral-field
bundle and avoids hard-coding a permanent semantic role for a given fiber
number.

Target photometric anchoring
----------------------------

After wavelength and spectrophotometric calibration, the optional Level-3
library interface can anchor a target spectrum to external broadband
photometry. Pass a calibrated ``specutils.Spectrum`` and an
``astropy.table.Table`` with ``band`` and AB-magnitude ``mag`` columns;
``mag_err`` is optional. Band names normally use SVO Filter Profile Service
identifiers, while custom response curves can be supplied as ``Bandpass``
objects.

``pipeline.l3.mangle()`` delegates to ``specmangle`` and fits a positive
natural-cubic-spline correction in log wavelength and log flux scale. It
returns the corrected spectrum together with passband coverage and residual
diagnostics. The corrected per-sample statistical uncertainty remains separate
from the correlated uncertainty in the fitted correction. See the
:doc:`pipeline package reference <../packages/pipeline>` for the current public
interface and authoritative upstream links. L3 has no FITS or command-line
wrapper until the L2 product format is defined.

Validation with the simulator
-----------------------------

Synthetic detector images are valuable pipeline fixtures because their input
spectra and true trace geometry are known. Use them to verify extraction flux
conservation, wavelength mapping, trace separation, masking, and uncertainty
propagation before relying only on arc- or sky-lamp data.
