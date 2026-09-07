Pipeline
========

Purpose
-------

The pipeline reduces raw or calibrated spectrograms into extracted spectra while
preserving detector masks, uncertainties, and per-fiber identity.

Installation and command line
-----------------------------

The distribution is ``classi-pipeline`` and its import namespace is
``pipeline``. Installation provides the ``classi-pipeline`` command:

.. code-block:: bash

   python -m pip install -e ./pipeline
   classi-pipeline l1 science_l0.fits science_l1.fits \
       --center 512.0 --spacing 25.7 \
       --gain 1.2 --read-noise 3.5

Use ``--centers`` for an explicit comma-separated list, or ``--center`` and
``--spacing`` with the configurable ``--n-traces`` value. Bias, dark, and flat
masters can be supplied with ``--bias``, ``--dark``, and ``--flat``.

The L1 ``--unit`` option supplies the science-image unit when ``BUNIT`` is
absent or overrides the header value when explicitly supplied. It defaults to
``adu``.

Processing levels
-----------------

The current code separates detector/image handling from the Level-1 spectral
extraction. A typical instrument-specific script reads a FITS frame into a
CCD-style object, locates or supplies the trace centers, and calls the generic
Level-1 processing routines. Level 2 is currently a placeholder and does not
yet perform wavelength or spectrophotometric calibration.

Primary extraction interface
----------------------------

``process_l1(...)`` is the main entry point used by instrument-specific
extraction scripts. Its extraction configuration includes trace centers,
extraction half-width, detector gain, and read noise. The function currently
uses boxcar extraction for the requested traces and returns one spectrum per
trace. Horne/optimal-extraction code is present, but ``process_l1()`` does not
currently select it.

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
products and will also support optimal extraction when that path is selected.

Per-fiber outputs
-----------------

Return every extracted fiber independently. Higher-level processing can label
fibers as science, sky, or calibration based on the observing configuration,
but the low-level extraction code should not assume a permanent semantic role
for a fixed fiber number.
