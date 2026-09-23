Instrument and software architecture
====================================

Physical signal path
--------------------

The instrument begins at the telescope focal plane, where the fiber bundle
samples the target and nearby sky. The fiber run carries the light to the bench
spectrograph. There, the collimator forms the beam incident on the optional
order-blocking filter and reflection grating; the camera lens then images the
dispersed fiber traces onto the science detector.

This physical path sets the boundaries between several kinds of configuration:

* telescope pointing, guiding, and focal-plane acquisition;
* fiber geometry and transmission;
* spectrograph alignment, filter state, grating geometry, focus, and aperture;
* detector readout, cooling, exposure, and FITS metadata; and
* reduction calibration and extraction choices.

The same configuration must be represented consistently in the instrument,
ETC, simulator, ICS metadata, and pipeline. Catalog values describe components;
as-built and measured values should replace them in the system model when they
become available.

Control and data boundaries
---------------------------

The ICS coordinates status and acquisition but does not replace the native
device interfaces or make quick-look products authoritative. Raw FITS frames
remain the hand-off between instrument operation and reduction. Telescope-side
state may arrive through ACE Connector interfaces, while instrument-side
devices such as the science camera and focus controller can use INDI-backed
interfaces.

Scientific data flow
--------------------

The software supporting that physical system has three layers:

#. **Reference data** -- throughput curves, atmospheric extinction, detector
   response data, and template spectra.
#. **Scientific modeling and reduction** -- ETC, simulator, and pipeline.
#. **Instrument operation** -- the ICS and hardware-specific adapters.

The ``classi-shared-data`` distribution (imported as ``shared_data``) is
the common reference-data dependency at the bottom of the scientific stack.
The ETC also reuses the physical and throughput models from
``classi-sim`` instead of maintaining a parallel implementation. Together
these dependencies prevent the ETC and simulator from silently diverging.

Instrument model
----------------

The current simulator describes the spectrograph from physical inputs rather
than asking callers to enter derived detector quantities. Important inputs
include detector pixel size, grating groove density, incidence and diffraction
angles, collimator and camera focal lengths, fiber core diameter, fiber pitch,
and diffraction order.

From these, the model derives quantities such as:

* central wavelength from the grating equation;
* wavelength dispersion at the detector;
* camera/collimator magnification;
* anamorphic factor;
* projected fiber pitch in detector pixels; and
* spatial and spectral fiber widths in detector pixels.

This is important for consistency: changing a physical element of the
instrument should automatically change all dependent detector-space quantities.

Fiber geometry
--------------

The instrument is modeled as a linear multi-fiber input/output. The simulator
supports one input spectrum per fiber and lays the traces out according to the
physical fiber pitch projected through the spectrograph. The software should not
assume that the present fiber count is immutable; the count is a model
parameter.

Hardware-control boundary
-------------------------

The ICS isolates device-specific interfaces behind backend objects. Development
can use mock devices, while the instrument-side deployment can use INDI for the
science camera/focus hardware and ACE Connector-backed interfaces for telescope
and guide-side devices.

A separate read-only ACE bridge is useful where the vendor Python bindings only
run on a particular x86 Python installation. That bridge should be treated as a
narrow compatibility service, not as a general remote-execution API.

Configuration ownership
-----------------------

Avoid maintaining the same instrument constant independently in several
packages. Shared reference curves belong in ``classi-shared-data``; physical
geometry belongs in the simulator's instrument model; observing-host addresses,
device names, and credentials belong in deployment configuration; and
night-specific choices belong in FITS metadata and observing notes.

When a value is duplicated for practical reasons, record which source is
authoritative and add a consistency check where possible.
