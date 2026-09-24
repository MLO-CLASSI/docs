Data products
=============

Raw detector frames
-------------------

Raw FITS files from the ICS are the authoritative acquisition products. Keep
all original headers and do not overwrite the raw files during reduction.

ICS header conventions
----------------------

The ICS retains camera-provided cards where useful and organizes its additions
into provenance, instrument, sensor, target/pointing, observation, timing, and
file-metadata sections. Important conventions are:

* ``INSTRUME`` is ``CLASSI``; ``ORIGIN``, ``LOCATION``, ``TELESCOP``, and
  ``OBSERVER`` identify the facility and observer.
* ``CAMERAFL``, ``COLLIMFL``, ``NGROOVES``, ``GRATING``, ``FILTER``, and
  ``DISPERS`` record the configured optical setup. These values come from the
  deployment's ``config.ini``.
* ``DETECTOR`` and ``PIXSIZE`` describe the unbinned sensor. ``BINX``, ``BINY``,
  and ``BINNING`` record the active binning; camera-provided binning and pixel-
  size cards are retained when present. ``GAIN``, ``GAINMODE``, ``CCD-TEMP``,
  and ``TECPOWER`` describe the readout and thermal state.
* ``RA`` and ``DEC`` are sexagesimal target coordinates. ``RA_OBJ`` and
  ``DEC_OBJ`` contain the same target position in decimal degrees, while
  ``RA_TEL`` and ``DEC_TEL`` record the actual telescope pointing. ``AIRMASS``
  and ``GUIDED`` describe the state at the end of the exposure.
* ``IMAGETYP`` is one of ``light``, ``flat``, ``dark``, ``bias``, or ``arc``.
  ``USERCMNT`` stores an optional observer comment; ``STAGEX``, ``STAGEY``,
  ``STAGEZ``, ``TELFOCUS``, ``CAMFOCUS``, and ``CAMAPER`` record mechanism
  positions where available.
* ``REQEXPT`` is the requested duration, whereas ``EXPTIME`` is the duration
  reported by the camera. ``TIMESYS`` is ``UTC``; ``DATE-OBS``, ``MJD-OBS``,
  ``DATE-END``, and ``SIDEREAL`` describe exposure timing. ``FILENAME`` and
  ``DATE`` identify the written product and its last modification time.

Do not infer a requested exposure from ``EXPTIME`` when ``REQEXPT`` is present,
and do not substitute target coordinates for the separately recorded telescope
pointing.

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
