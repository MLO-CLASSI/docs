ETC
===

Purpose
-------

The exposure-time calculator estimates detected source counts, sky counts, and
signal-to-noise in wavelength bins for the spectrograph. It can also invert the
calculation to find the AB magnitude that reaches a requested S/N in each bin.
It contains a reusable calculation layer and a Tk-based desktop interface.

Installation and launch
-----------------------

The distribution is ``classi-etc`` and its import namespace is ``etc``.
Installation provides the ``classi-etc`` command for launching the desktop
interface.

Primary interface
-----------------

``ETCCalculator`` is the scientific core. The most important methods and
properties are:

``get_SNR_from_spectrum(...)``
   Calculate counts and S/N for one or more wavelength bins. The default
   configuration uses the FLI Aurora AR571 camera, Newport 1294 grating, dark-sky
   background, and a fiber-coupling efficiency of 1.0.

``get_limiting_magnitudes_from_spectrum(...)``
   Calculate the source AB magnitude that reaches ``target_snr`` in each
   wavelength bin for a fixed exposure time. The selected LSST ``g``, ``r``,
   or ``i`` band defines the reported magnitude, while the input spectrum
   supplies the spectral shape. Its absolute normalization does not affect the
   result.

``load_spectrum(spectrum_file)``
   Load a two-column reference spectrum whose wavelength grid is already in
   the observer frame.

``scale_spectrum_to_magnitude(...)``
   Scale a template spectrum to a target LSST ``g``, ``r``, or ``i`` AB
   magnitude.

``get_throughput_components(...)``
   Return atmosphere, fiber, miscellaneous-loss, collimator, grating, detector
   window, detector-QE, and total-throughput arrays on a supplied wavelength
   grid.

``available_camera_models`` / ``available_gratings`` / ``available_sky_backgrounds`` / ``available_magnitude_bands``
   Enumerate the camera, grating, ``dark``, ``grey``, or ``bright`` sky, and
   LSST ``g``, ``r``, or ``i`` magnitude-band configurations represented by
   the installed reference data.

The ETC interprets input-spectrum wavelengths, ``wave_centers``, and
``binsize`` in the observer frame. It does not apply a redshift correction; a
rest-frame template must be transformed to the observer frame before it is
passed to the calculator.

Each bin extends from ``wave_center - binsize / 2`` through
``wave_center + binsize / 2``. The source spectrum must cover both boundaries
of every requested bin. The ETC linearly interpolates source and sky flux
densities at the exact boundaries before integrating, rather than integrating
only the samples that happen to fall inside the bin.

Desktop GUI
-----------

The desktop interface supports both calculation directions. **Compute SNR**
uses the target magnitude and magnitude-band fields to evaluate a source of
known brightness. **Compute limiting magnitude(s)** instead uses the
limiting-magnitude SNR and band fields to report the AB magnitude that reaches
that S/N in each requested wavelength bin. The exposure time, spectral shape,
instrument configuration, sky background, and fiber-coupling efficiency are
shared by both calculations.

Result structure
----------------

Both calculation methods return a mapping containing:

``bins``
   A sequence of ``SNRBinResult`` objects. Each result contains
   ``wave_center_nm``, ``source_counts``, ``sky_counts``, ``snr``, mean
   ``component_averages``, and the bin-specific ``n_wave_pixels``,
   ``n_total_pixels``, ``read_noise_var``, and ``dark_counts`` values.
   ``limiting_magnitude`` is ``None`` for a forward S/N calculation and is
   populated for each inverse limiting-magnitude result. In the inverse result,
   ``source_counts`` is the source count level required to reach ``target_snr``.

``meta``
   Resolved detector/instrument values such as read noise, dispersion,
   ``extraction_aperture_pix``, ``extraction_fraction``, grating, airmass,
   ``fiber_coupling_efficiency``, ``sky_background``, and any spectrum-scaling
   factor. ``detector_temperature_c`` records the fixed -20 °C operating
   assumption used to select each camera's dark current. Pixel counts and their
   associated read-noise and dark-current terms vary by wavelength bin and are
   therefore stored on each ``SNRBinResult``, not in ``meta``. An inverse
   calculation also records ``target_snr``, ``limiting_magnitude_band``, and the
   input spectrum's ``reference_magnitude`` in ``meta``.

``throughput_plot``
   Wavelength and component arrays suitable for plotting the response used in
   the calculation.

Example
-------

.. code-block:: python

   from etc import ETCCalculator, get_default_spectrum_file

   calc = ETCCalculator(fiber_length_m=10.0)
   result = calc.get_SNR_from_spectrum(
       exp_time=1800.0,
       spectrum_file=get_default_spectrum_file(),
       wave_centers=[550.0, 650.0, 750.0],
       binsize=5.0,
       sky_background="grey",
       camera_model="Aurora",
       grating_id=1294,
       airmass=1.3,
       fiber_coupling_efficiency=0.75,
       target_magnitude=17.5,
       magnitude_band="g",
   )

   for bin_result in result["bins"]:
       print(bin_result.wave_center_nm, bin_result.snr)

To solve for the per-bin limiting magnitude at a fixed exposure time:

.. code-block:: python

   limits = calc.get_limiting_magnitudes_from_spectrum(
       exp_time=600.0,
       spectrum_file=get_default_spectrum_file(),
       wave_centers=[450.0, 550.0, 650.0, 750.0],
       binsize=5.0,
       target_snr=5.0,
       magnitude_band="r",
       sky_background="dark",
       camera_model="Aurora",
       grating_id=1294,
       airmass=1.3,
       fiber_coupling_efficiency=0.75,
   )

   for bin_result in limits["bins"]:
       print(bin_result.wave_center_nm, bin_result.limiting_magnitude)

The coupling efficiency is a fraction from 0 to 1 and reduces source counts
only. The selected line-resolved DESI sky spectrum is integrated over the
fiber's circular on-sky area independently of that coupling loss. Source and sky
counts are both multiplied by the Gaussian-profile fraction enclosed by a
spatial extraction box one fiber pitch wide. Dark-current and read-noise
variance use the pixel count in that same extraction box.

Data dependency
---------------

The ETC depends on ``classi-sim`` for the physical instrument, detector,
atmospheric-extinction, throughput, and photon-flux models. Reference curves
and spectra come from ``classi-shared-data`` through the ``shared_data``
resource dictionaries. The default fiber-throughput term uses the CeramOptec
UVNS attenuation curve. This keeps ETC predictions consistent with detector
simulations and makes reference-data changes explicit package changes.
