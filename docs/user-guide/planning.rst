Planning an observation
=======================

The exposure-time calculator is the first scientific tool in the normal
workflow. It predicts the signal-to-noise ratio in user-selected wavelength bins
for a source spectrum and instrument configuration.

Inputs
------

The core calculation accepts a reference or target spectrum whose wavelengths
are in the observer frame, together with:

* exposure time;
* observer-frame wavelength-bin centers and bin size;
* sky background (``dark``, ``grey``, or ``bright``);
* detector/camera model;
* grating choice;
* numerical airmass;
* fiber length;
* fiber-coupling efficiency; and
* optional target AB magnitude plus LSST magnitude band for flux scaling.

The ETC currently supports scaling a template spectrum to LSST ``g``, ``r``,
or ``i`` photometry in the AB system. This is useful when the spectral
shape is known or assumed but only broadband target photometry is available.

The ETC does not apply a redshift correction. If a template is in the rest
frame, transform it to the observer frame before supplying it to the ETC. The
requested wavelength-bin centers and bin size must likewise describe the
observer frame.

Fiber-coupling efficiency is a fraction from 0 to 1 representing point-source
light lost before entering the fiber. It reduces source counts but not sky
counts. The default of 1.0 assumes perfect coupling.

Detector sampling, fiber pitch, extraction fraction, read noise, telescope
collecting area, and the component throughput model are derived from the
selected camera and the shared ``classi-sim`` instrument model rather
than entered as independent GUI parameters. The default instrument
configuration is the FLI Kepler camera with the Newport 1294 grating.

Throughput accounting
---------------------

The calculation keeps the major throughput terms separate before multiplying
them into the total response. This makes it possible to inspect detector,
grating, fiber, atmosphere, and lens contributions individually and to disable a
term for diagnostic comparisons.

The ``dark``, ``grey``, and ``bright`` choices select line-resolved DESI sky
spectra. Each sky spectrum is integrated on its own finely sampled wavelength
grid over the fiber's circular on-sky area, preserving narrow airglow lines.
Because these spectra represent surface brightness at the observatory,
atmospheric extinction is not applied to them again.

The spatial extraction box is one fiber pitch wide, extending halfway toward
the centerline of each neighboring trace. Source and sky counts are multiplied
by the fraction of the assumed Gaussian fiber profile enclosed by that box.
Fiber coupling is then applied only to the source. Dark-current and read-noise
variance use the same extraction-box pixel count. The detector temperature is
not a user input: the ETC uses each camera's fixed dark-current value at -20 °C
and records that assumption in the result metadata.

Source and sky spectra are linearly interpolated at the exact requested bin
boundaries before integration, so an input spectrum must cover every complete
bin. For the default detector configuration, the spectral width of each bin is
computed from the nonlinear ``SpectrographModel.wavelength_to_x()`` mapping
rather than from ``binsize / dispersion``. Consequently, the spectral and total
pixel counts and their read-noise and dark-current contributions are reported
separately on each bin result.

The reported result for each wavelength bin also includes source counts, sky
counts, S/N, and mean component throughputs.

Recommended workflow
--------------------

#. Choose a representative template spectrum covering the wavelength region of
   interest.
#. If it is a rest-frame template, transform it to the observer frame before
   supplying it to the ETC. If needed, scale it to the target's measured LSST
   ``g``, ``r``, or ``i`` AB magnitude.
#. Select the expected camera/grating configuration, airmass, and dark, grey,
   or bright sky background.
#. Estimate the point-source fiber-coupling efficiency for the observing setup.
#. Evaluate several wavelength bins, especially the region containing the
   diagnostic spectral feature that drives the observation.
#. Adjust exposure time until the limiting bin reaches the desired S/N.
#. Check the component-throughput plot if the result is unexpectedly poor.

The ETC answer is a planning estimate, not a substitute for the simulator when
pixel-level effects, trace overlap, saturation morphology, or extraction
behavior matter.
