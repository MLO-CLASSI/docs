Data products
=============

Raw detector frames
-------------------

Raw FITS files from the ICS are the authoritative acquisition products. All
original headers should be retained, and raw files should not be overwritten
during reduction.

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
* ``DETECTOR`` identifies the sensor. Camera-provided ``PIXSIZE1`` and
  ``PIXSIZE2`` cards are retained when present; the ICS does not synthesize the
  former generic ``PIXSIZE`` card. ``BINNING`` records the requested setting,
  while camera-provided ``XBINNING``, ``YBINNING``, ``XPIXSZ``, and ``YPIXSZ``
  cards preserve the reported detector state. The ICS no longer adds parallel
  ``BINX`` or ``BINY`` cards. ``GAIN`` and ``GAINMODE`` describe the readout
  state; ``SET-TEMP``, ``CCD-TEMP``, and ``TECPOWER`` record the sensor setpoint,
  measured temperature, and cooler power.
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

The requested exposure should not be inferred from ``EXPTIME`` when ``REQEXPT``
is present, and target coordinates should not be substituted for the separately
recorded telescope pointing.

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
