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
   A throughput curve derived from the adopted site extinction data and an
   airmass.

``DetectorModel``
   Detector dimensions, pixel size, gain, read noise, dark current, bias, and
   optional full-well level. ``apply_noise`` converts an ideal electron image
   into a noisy ADU image.

   Reusable ``FLI_KL400``, ``FLI_AR571``, and ``QHY_268M`` detector models are
   defined in ``simulator.components.cameras``. The top-level
   ``simulator.DetectorModel`` import remains available for custom models. The
   repository example notebook now uses ``FLI_AR571`` for the current Aurora
   baseline. That preset currently leaves ``gain`` unspecified and therefore
   inherits the generic 1 e⁻/ADU default; a measured value for the deployed
   readout mode should be supplied before quantitative use.

``SpectrographModel``
   Physical optical geometry. It derives central wavelength, dispersion,
   magnification, anamorphic factor, projected fiber pitch, and spatial/spectral
   widths rather than requiring those quantities as independent inputs.

``InstrumentSimulator``
   Combines the spectrograph model with throughput curves, renders expected
   electrons, resamples coarse input spectra as needed, and optionally applies
   the detector noise model.

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
       throughputs=[],
   )

The numeric values above illustrate the interface; use the instrument's current
measured/configured values for production simulations.

Multi-fiber spectra
-------------------

For ``fiber_count > 1``, ``flux_density`` must contain one spectrum per fiber.
The current linear-bundle use case therefore supplies an array shaped
``(fiber_count, n_wavelength)``. The simulator projects the physical fiber pitch
to the detector automatically.

``render_electrons`` and ``simulate`` accept ``fiber_coupling_efficiency`` as
either one dimensionless fraction for every fiber or one fraction per fiber.
Every value must lie between 0 and 1; the factor scales the expected source
electrons before the traces are deposited on the detector. The default is 1.0.
