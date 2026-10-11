Pipeline
========

Purpose
-------

The pipeline reduces raw or calibrated spectrograms into extracted spectra while
preserving detector masks, uncertainties, and per-fiber identity.

Installation and command line
-----------------------------

The distribution is ``classi-pipeline``, requires Python 3.12 or newer, and
uses the ``pipeline`` import namespace. Installation provides the
``classi-pipeline`` command:

.. code-block:: bash

   python -m pip install -e ./pipeline
   classi-pipeline l1 science_l0.fits science_l1.fits \
       --center 512.0 --spacing 25.7 \
       --gain 1.2 --read-noise 3.5 \
       --rebin 4 --plot

The dependency specification installs ``specreduce`` and ``specmangle``
directly from the ``main`` branches of their GitHub repositories and declares
``asdf`` explicitly for wavelength-calibration reference files. A reproducible
pipeline environment should record the resolved commits for both Git
dependencies as well as the CLASSI commit; installing this revision requires
Git and network access to GitHub.

Use ``--centers`` for an explicit comma-separated list, or ``--center`` and
``--spacing`` with the configurable ``--n-traces`` value. Bias, dark, and flat
masters can be supplied with ``--bias``, ``--dark``, and ``--flat``.

The L1 ``--unit`` option supplies the science-image unit when ``BUNIT`` is
absent or overrides the header value when explicitly supplied. It defaults to
``adu``.

The command reads the science image from the extension selected with
``--data-ext``. When the loaded image has no uncertainty, both ``--gain`` and
``--read-noise`` are required to construct the variance model. Library callers
can instead pass a ``CCDData`` object that already carries its uncertainty and
mask. ``--cal-data-ext`` independently selects the image extension used for
bias, dark, and flat masters.

``--rebin N`` sums groups of ``N`` adjacent dispersion pixels in each output
spectrum; the default of 1 preserves the native sampling. Counts are summed,
uncertainties are combined in quadrature, and the output ``PIXEL`` coordinate
is the mean of the contributing native coordinates. Only complete groups are
written, so as many as ``N - 1`` trailing native pixels can be omitted. The
``REBIN`` and ``NTRIM`` FITS keywords record these choices. ``N`` must be a
positive integer and cannot exceed the extracted spectrum length.

``--plot`` writes a quicklook PNG beside the L1 product, using the same stem as
the requested FITS output. It plots the final stored spectra, including any
requested rebinning.

Processing levels
-----------------

The code separates detector/image handling from Level-1 spectral extraction.
A typical instrument-specific script reads a FITS frame into a CCD-style object,
locates or supplies the trace centers, and calls the generic Level-1 processing
routines. Level 2 provides library machinery for arc-derived wavelength
solutions and per-exposure sky-line refinement; ``process_l2()`` and the final
Level-2 science-product interface remain placeholders. Level 3 provides
target-specific photometric anchoring for spectra that have already been
wavelength- and (preliminarily) flux-calibrated.

Level-2 wavelength calibration
------------------------------

``pipeline.l2`` exposes the following public wavelength-calibration interfaces:

``fit_arc_wavelength_solution(...)``
   Fit one trace from matched native-pixel positions and reference wavelengths.
   It returns an ``ArcWavelengthSolution`` containing a
   ``specreduce.wavesol1d.WavelengthSolution1D`` plus line identifiers,
   used/rejected flags, wavelength and pixel residuals, and RMS diagnostics.
   The default fit is a second-degree polynomial in Angstrom with vacuum
   wavelengths.

``write_wavesol(...)`` / ``read_wavesol(...)``
   Serialize or restore all trace solutions in one versioned ASDF reference
   file. The top-level ``classi_wavesol`` tree records the format version,
   creation time, wavelength unit and medium, native pixel convention, arc-file
   provenance, lamp names, and trace count. Each trace stores its GWCS
   transform and bounding box together with the matched-line arrays and fit
   diagnostics.

``fit_sky_refinement(...)``
   Fit measured science-exposure sky-line centroids against a baseline arc
   solution. ``mode="auto"`` fits a pixel shift from one line and an affine
   shift plus stretch from two or more lines. Optional centroid uncertainties
   weight the fit. Every reference wavelength must map to a finite master pixel
   within the baseline solution's lower-inclusive, upper-exclusive pixel bounds;
   inputs outside those bounds raise ``ValueError``. The returned
   ``SkyRefinement`` can compose the correction with the baseline through
   ``refined_solution(...)`` without refitting its higher-order shape.

Wavelength-solution pixel coordinates are zero-based native detector
coordinates along array axis 1. ``pix_bounds`` uses a lower-inclusive,
upper-exclusive pair. This convention also applies to rebinned Level-1 spectra:
their ``PIXEL`` values remain means of native detector coordinates rather than
indices into the shorter output table.

Automatic arc-line matching, automatic sky-line selection and centroiding,
application to a Level-1 product, and Level-2 FITS output are outside these
interfaces. Callers supply the matched arc lines or measured sky centroids.
The pipeline repository's `Level-2 reference`_ is authoritative for the ASDF
tree and mathematical refinement model.

.. _Level-2 reference:
   https://github.com/MLO-CLASSI/pipeline#l2---physical-spectral-calibration

Level-3 photometric anchoring
-----------------------------

The ``pipeline.l3`` module re-exports ``specmangle.mangle``, ``Bandpass``, and
``MangleResult``. ``mangle`` accepts a wavelength- and flux-calibrated
``specutils.Spectrum`` plus an ``astropy.table.Table`` containing ``band`` and
``mag`` columns and, optionally, ``mag_err``. Magnitudes are currently AB.
Band names are normally SVO Filter Profile Service identifiers; callers can
instead supply custom response curves as ``Bandpass`` objects.

The correction is a natural cubic spline in log wavelength and log flux scale,
with one anchor for each usable unique passband and constant extrapolation
beyond the edge anchors. By default, a passband is excluded when less than 98%
of its AB-reference signal falls within valid spectrum samples. ``MangleResult``
contains the corrected spectrum, correction, photometric diagnostics, and fit
covariance. The input statistical uncertainty is scaled with the correction;
uncertainty in the fitted correction remains separate because it is correlated
across wavelength. L3 has no FITS or command-line wrapper because the L2
science-product format is not defined.

The pipeline repository's `Level-3 reference`_ describes the supported input
schema and re-exported interface. The `specmangle reference`_ is authoritative
for model options, coverage diagnostics, custom bandpasses, and result fields.

.. _Level-3 reference:
   https://github.com/MLO-CLASSI/pipeline#l3---photometric-calibration
.. _specmangle reference:
   https://github.com/cgobat/specmangle

Primary extraction interface
----------------------------

``process_l1(...)`` is the main entry point used by instrument-specific
extraction scripts. Its extraction configuration includes trace centers,
extraction half-width, detector gain, and read noise. The function uses boxcar
extraction for the requested traces and returns one spectrum per trace.

A representative pattern is:

.. code-block:: python

   spectra = process_l1(
       ccd,
       centers=trace_centers,
       half_width=8,
       gain=detector_gain,
       read_noise=detector_read_noise,
   )

Keep detector-specific constants in the instrument adapter or configuration
layer rather than baking them into the reusable extraction algorithm.

Masks and variance
------------------

The pipeline should treat saturation and other invalid detector pixels as masks.
A mask is not the same thing as replacing a value with ``NaN``: the underlying
value can remain available while the extraction/combination logic knows that it
must not contribute as a valid measurement.

Propagated variance should include the appropriate detector noise terms and
remain consistent with the CCD data unit. It is retained in the Level-1
products. The command-line variance model includes Poisson and read-noise terms
but excludes uncertainty from the master calibration frames.

Per-fiber outputs
-----------------

Return every extracted fiber independently. Higher-level processing can label
fibers as science, sky, or calibration based on the observing configuration,
but the low-level extraction code should not assume a permanent semantic role
for a fixed fiber number.
