Conventions
===========

Units
-----

New scientific code should prefer Astropy quantities for physical inputs and
outputs. This is particularly important in the simulator, where focal lengths,
fiber diameters, groove densities, wavelengths, detector pixel sizes, gain, and
noise terms otherwise have easy-to-miss implicit units.

Common conventions are:

.. list-table:: Scientific quantities
   :header-rows: 1

   * - Quantity
     - Preferred representation
   * - wavelength
     - Astropy length quantity; Angstrom is the common internal spectral unit
   * - input ``f_lambda``
     - ``erg / (s cm2 Angstrom)``
   * - detector charge
     - electrons
   * - detector output
     - ADU after gain/bias application
   * - gain
     - electrons / ADU
   * - read noise
     - electrons per pixel
   * - dark current
     - electrons / second per pixel
   * - detector locations/widths
     - pixels

Array orientation
-----------------

Detector images follow NumPy convention ``image[y, x]`` with shape
``(ny, nx)``. The dispersion direction is represented by the detector ``x``
coordinate in the current simulator, while the individual fiber traces are
separated along ``y``.

Spectral arrays
---------------

A single spectrum uses one wavelength array and one flux-density array of the
same length. A multi-fiber simulator input uses one common wavelength array and
a flux-density matrix shaped ``(fiber_count, n_wavelength)``.

For the ETC, the wavelengths in a two-column input spectrum are observer-frame
quantities. Requested wavelength-bin centers and bin sizes are also specified
in the observer frame. The ETC does not apply a redshift correction, so
rest-frame templates must be transformed before they are supplied to the
calculator.

Wavelength direction
--------------------

Whether wavelength increases toward larger or smaller detector ``x`` should not
be inferred from the sign of a hand-entered dispersion. The physical simulator
has an explicit ``wavelength_increases_with_x`` choice and computes the
wavelength mapping from the grating geometry.

Masks
-----

Masks indicate data that should not contribute as valid measurements. ``NaN``
should not be used as a substitute for a mask when the underlying CCD container
already supports a mask and uncertainty.
