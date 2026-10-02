Simulator
=========

Purpose
-------

The simulator is a forward model from physical spectrograph configuration and
input spectra to a synthetic detector image.

Core objects
------------

``ThroughputCurve``
   A wavelength-dependent dimensionless transmission/efficiency curve. The
   wavelength axis carries Astropy units, and CSV curves can be loaded with a
   declared wavelength unit.

``AtmosphericExtinction``
   A throughput curve derived from the LSST v1.9 standard-atmosphere profile
   distributed by ``classi-shared-data``. The profile includes aerosol,
   telluric, and line-absorption structure from 300 to 1150 nm. It represents
   nominal airmass 1.0; the simulator evaluates a selected airmass ``X`` as
   ``T(wavelength)**X``. The selected value is available as the object's
   ``airmass`` attribute, and wavelengths outside the tabulated range have zero
   throughput by default.

``DetectorModel``
   Detector dimensions, pixel size, gain, read noise, dark current, bias, and
   optional full-well level for the native physical sensor.
   ``apply_noise`` converts an ideal electron image into a noisy ADU image.

   Reusable ``FLI_KL400``, ``FLI_AR571``, and ``QHY_268M`` detector models are
   defined in ``simulator.components.cameras``. Custom models can import
   ``DetectorModel`` from ``simulator``. The repository example notebook uses
   ``FLI_AR571`` for the Aurora baseline. That native-sensor preset leaves
   ``gain`` unspecified and therefore inherits the generic 1 e⁻/ADU default; a
   measured value for the deployed readout mode should be supplied before
   quantitative use.

``DetectorReadout``
   The output-grid view of a native detector for an integer square-binning
   factor. Simulator instances expose this as ``readout``.

``SkySpectrum``
   A line-resolved sky surface-brightness spectrum. ``DESI_SKY_DARK``,
   ``DESI_SKY_GREY``, and ``DESI_SKY_BRIGHT`` are reusable presets backed by
   ``classi-shared-data``.

``SpectrographModel``
   Physical optical geometry. It derives central wavelength, dispersion,
   magnification, anamorphic factor, projected fiber pitch, and spatial/spectral
   widths rather than requiring those quantities as independent inputs.

``InstrumentSimulator``
   Combines the spectrograph, telescope, atmosphere, optional sky, and readout
   binning; renders expected electrons; resamples coarse input spectra as
   needed; and optionally applies the detector noise model.

The simulator repository's `README example`_ is the authoritative compact
inventory of the component-based CLASSI configuration.

.. _README example: https://github.com/MLO-CLASSI/sim#classi-spectrograph-instrument-simulator

Example configuration
---------------------

.. code-block:: python

   import astropy.units as u

   from simulator import DetectorModel, InstrumentSimulator, SpectrographModel

   detector = DetectorModel(
       nx=2048,
       ny=2048,
       pixel_size=5.4 * u.um,
       gain=0.37 * u.electron / u.adu,
       read_noise=9.3 * u.electron,
   )

   spectrograph = SpectrographModel(
       detector=detector,
       groove_density=600 / u.mm,
       incidence_angle=32 * u.deg,
       diffraction_angle=20 * u.deg,
       collimator_focal_length=100 * u.mm,
       camera_focal_length=85 * u.mm,
       fiber_core_diameter=105 * u.um,
       fiber_count=7,
       fiber_pitch=250 * u.um,
   )

   simulator = InstrumentSimulator(
       spectrograph=spectrograph,
       binning=2,
       throughputs=[],
   )

The numeric values above illustrate the interface; use the instrument's current
measured/configured values for production simulations.

Reference-spectrum reader
-------------------------

``read_reference_spectrum(path)`` is the public convenience loader used by the
repository example. It recognizes two input conventions:

* a filename containing ``SNIFS`` is read as the three-column SNIFS ASCII
  convention (wavelength, flux, and uncertainty) and returned as a FITS binary
  table HDU with units and parsed header metadata; and
* an ``.ecsv`` file is returned as an Astropy table whose ``header`` property
  aliases ``meta``. The loader maps ``TARGETID`` to ``OBJECT`` when needed and
  expands an Astropy ``coordinates`` entry into numeric ``RA`` and ``DEC``
  metadata.

Other filename and format conventions are unsupported; callers should verify
that the return value is not ``None`` before passing it to the renderer. The
shared-data `reference-spectrum inventory`_ is the authoritative list of
available inputs.

.. _reference-spectrum inventory:
   https://github.com/MLO-CLASSI/shared-data/blob/main/reference_spectra/README.md

Detector binning
----------------

``DetectorModel`` always describes the native sensor. ``binning`` is selected
when constructing ``InstrumentSimulator`` and should be a positive integer that
evenly divides both detector dimensions. For a square ``b`` × ``b`` readout,
``simulator.readout`` exposes dimensions divided by ``b``, effective pixel size
multiplied by ``b``, dark current multiplied by ``b**2``, and read noise
multiplied by ``b``.

Optical signal, dark charge, full-well saturation, and read noise are evaluated
on native pixels before each block is summed. Gain and the output bias are then
applied to the binned image. ``simulator.readout_spectrograph`` supplies the
wavelength/pixel geometry in output coordinates, while
``simulator.spectrograph`` retains native coordinates.

Component-based throughput and sky
----------------------------------

``SpectrographModel.from_components`` accepts detector, grating, collimator,
camera-lens, fiber, and optional passive-optics objects. Their associated
throughput curves are assembled automatically; an atmosphere can be added by
``InstrumentSimulator``. The component catalog lives in
``simulator.components`` and keeps hardware geometry next to the corresponding
``classi-shared-data`` resource keys.

When a DESI sky preset is supplied through ``sky=``, the simulator scales its
surface brightness by the circular fiber sky area and applies downstream
instrument throughput. Those spectra already represent the sky at the
observatory, so atmospheric extinction is excluded from the sky path rather
than applied twice. ``render_sky_electrons`` returns the sky-only image.

Multi-fiber spectra
-------------------

For ``fiber_count > 1``, ``flux_density`` must contain one spectrum per fiber.
CLASSI's linear bundle therefore uses an array shaped
``(fiber_count, n_wavelength)``. The simulator projects the physical fiber pitch
to the detector automatically.

``render_electrons`` and ``simulate`` accept ``fiber_coupling_efficiency`` as
either one dimensionless fraction for every fiber or one fraction per fiber.
Every value must lie between 0 and 1; the factor scales the expected source
electrons before the traces are deposited on the detector. The default is 1.0.
