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
remain the hand-off between instrument operation and reduction. Instrument-side
devices such as the science camera and focus controller use INDI-backed
interfaces. Telescope-side ACE devices are translated to ASCOM Alpaca by a
bridge on the TCS computer, allowing the ICS host to use ordinary HTTP clients
without the vendor ACE package.

Scientific data flow
--------------------

The software supporting that physical system has three layers:

#. **Reference data** -- throughput curves, atmospheric extinction, detector
   response data, and template spectra.
#. **Scientific modeling and reduction** -- ETC, simulator, and pipeline.
#. **Instrument operation** -- the ICS and hardware-specific adapters.

The ``classi-shared-data`` distribution (imported as ``shared_data``) is
the common reference-data dependency at the bottom of the scientific stack.
The ETC imports the physical and throughput models from ``classi-sim``, keeping
the ETC and simulator consistent.

Instrument model
----------------

The simulator describes the spectrograph from physical inputs rather than asking
callers to enter derived detector quantities. Important inputs include detector
pixel size, grating groove density, incidence and diffraction angles, collimator
and camera focal lengths, fiber core diameter, fiber pitch, and diffraction
order.

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
can use mock devices, while deployment can use INDI for the science camera and
camera-lens controller and Alpyca clients for telescope-side devices.

The ACE Alpaca bridge is a separate TCS-hosted service. It owns the vendor
bindings, ACE credentials, and ACE device names; the ICS owns the Alpaca network
address and device-number mapping. The bridge supports telescope pointing and
slewing, telescope focus, and guide-camera acquisition. Guide-stage X/Y motion
is not exposed by the bridge, and the ICS rejects an ``alpaca`` stage
configuration. Telescope Focuser 0 represents telescope focus, not a stage
axis. A network stage interface should be implemented and verified on both
sides before deployment; the bridge should not be treated as a generic
remote-execution API.

Configuration ownership
-----------------------

The same instrument constant should not be maintained independently in several
packages. Shared reference curves belong in ``classi-shared-data``; physical
geometry belongs in the simulator's instrument model; observing-host addresses,
device names, and credentials belong in deployment configuration; and
night-specific choices belong in FITS metadata and observing notes.

When a value is duplicated for practical reasons, record which source is
authoritative and add a consistency check where possible.
