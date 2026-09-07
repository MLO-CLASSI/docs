ETC
===

Purpose
-------

The exposure-time calculator estimates detected source counts, sky counts, and
signal-to-noise in wavelength bins for the spectrograph. It contains a reusable
calculation layer and a Tk-based desktop interface.

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
   configuration uses the FLI Kepler camera, Newport 1294 grating, dark-sky
   background, and a fiber-coupling efficiency of 1.0.

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

``available_camera_models`` / ``available_gratings`` / ``available_sky_backgrounds``
   Enumerate the camera, grating, and ``dark``, ``grey``, or ``bright`` sky
   configurations represented by the installed reference data.

The ETC interprets input-spectrum wavelengths, ``wave_centers``, and
``binsize`` in the observer frame. It does not apply a redshift correction; a
rest-frame template must be transformed to the observer frame before it is
passed to the calculator.

Result structure
----------------

``get_SNR_from_spectrum`` returns a mapping containing:

``bins``
   A sequence of ``SNRBinResult`` objects with wavelength center, source counts,
   sky counts, S/N, and mean component throughputs.

``meta``
   Resolved detector/instrument values such as read noise, dispersion,
   ``extraction_aperture_pix``, ``extraction_fraction``, grating, airmass,
   ``fiber_coupling_efficiency``, ``sky_background``, and any spectrum-scaling
   factor. ``detector_temperature_c`` records the fixed -20 °C operating
   assumption used to select each camera's dark current.

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
       camera_model="Kepler",
       grating_id=1294,
       airmass=1.3,
       fiber_coupling_efficiency=0.75,
       target_magnitude=17.5,
       magnitude_band="g",
   )

   for bin_result in result["bins"]:
       print(bin_result.wave_center_nm, bin_result.snr)

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
resource dictionaries. This keeps ETC predictions consistent with detector
simulations and makes reference-data changes explicit package changes.
