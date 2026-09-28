Simulating detector data
========================

The simulator converts one or more input spectra into a synthetic detector
image. Its model is unit-aware through Astropy quantities and computes
important detector-space quantities from the physical spectrograph geometry.

Inputs and units
----------------

Wavelength and flux-density arrays should carry Astropy units. The simulator
internally converts wavelength to Angstrom and flux density to
``erg / (s cm2 Angstrom)`` before computing photon/electron counts.

For a multi-fiber simulation, supply a two-dimensional flux array with shape
``(fiber_count, n_wavelength)``. All fibers share the same wavelength grid, but
each row can contain a different spectrum.

Detector sampling
-----------------

Input spectra can be more coarsely sampled than the detector dispersion. Before
rendering, the simulator maps the supplied wavelengths to detector ``x``. If
adjacent samples are farther apart than ``render_sampling_px``, it constructs a
uniform detector-coordinate grid, maps that grid back to wavelength, and
linearly interpolates each spectrum while preserving the original samples as
breakpoints. This follows the nonlinear grating mapping across the detector and
prevents gaps in traces from sparsely sampled input spectra.

Optical geometry
----------------

The spectrograph model derives the central wavelength from

.. math::

   m\lambda = d(\sin\alpha + \sin\beta),

where ``m`` is the diffraction order, ``d`` the groove spacing, ``alpha`` the
incidence angle, and ``beta`` the diffraction angle.

The detector dispersion is derived from groove spacing, diffraction angle,
camera focal length, and detector pixel size. Fiber pitch and fiber image width
are likewise projected from physical dimensions through the
camera/collimator magnification.

Image formation
---------------

For each wavelength sample and fiber, the simulator:

#. multiplies the source flux by collecting area and the combined throughput;
#. converts energy flux to expected photoelectrons;
#. applies the scalar or per-fiber coupling efficiency;
#. maps wavelength to detector ``x`` through the grating geometry;
#. maps the fiber to the appropriate detector ``y`` trace;
#. deposits the counts with a two-dimensional Gaussian kernel; and
#. optionally applies a vignetting map.

The detector model combines source and dark-current charge, applies Poisson
noise, clips accumulated charge at full well, then adds read noise before gain
conversion and bias. Read noise is therefore not clipped by the physical
full-well capacity.

Use a fixed random seed when producing regression fixtures for the pipeline.
