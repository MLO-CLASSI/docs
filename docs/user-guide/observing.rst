Operating the instrument
========================

The instrument control system provides the observing interface while keeping
hardware-specific details behind backend classes. This chapter is the framework
for the CLASSI operator procedure; commissioning should replace the remaining
configuration-dependent guidance with verified values, screenshots, and
recovery steps.

Before the night
----------------

#. Review the target list, visibility, acquisition information, and requested
   signal-to-noise or exposure limits.
#. Use the ETC as the starting point for science exposure times and note which
   target spectrum, magnitude, sky state, and instrument configuration were
   assumed.
#. Decide which detector, wavelength, flat-field, and spectrophotometric
   calibrations are required for the planned reductions.
#. Confirm that the observing host has sufficient writable storage and that the
   intended data root is unambiguous.
#. Record the deployed ICS, pipeline, simulator, ETC, and shared-data versions.

Startup and health check
------------------------

#. Power and connect the instrument according to the observatory's approved
   hardware sequence.
#. Start the required device services and then the ICS using the deployment
   configuration for the observatory host.
#. Verify communication with the telescope/guide interfaces, science camera,
   and camera-lens controller before moving hardware or beginning an exposure.
#. Confirm that the deployment's ``config.ini`` names the installed optical
   components and contains the correct instrument geometry and data root.
#. Confirm detector cooling and readout mode, focus position, lens aperture,
   filter state, grating configuration, and writable data destination.
#. Acquire a short test exposure and verify that the FITS file is readable,
   correctly timestamped, and populated with the expected instrument metadata.

Exact service names, ports, device identifiers, and nominal telemetry ranges
belong in the deployment runbook because they can change independently of the
software API.

Development versus deployment
------------------------------

Use mock backends for UI and workflow development. Hardware deployment can use
INDI for instrument-side devices such as the science camera and camera-lens
focus controller. Telescope-side devices are reached through the TCS-hosted ACE
Alpaca bridge, so the ICS host needs only Alpyca and network access to the
bridge; it does not need the vendor ACE Connector package.

This split lets most of the web application and acquisition logic be tested
without physical hardware.

Science exposures
-----------------

The ICS stores completed exposures under its configured data root and exposes
the most recent science FITS image to the web interface for display. The UI can
use JS9 to inspect the current frame without converting the scientific FITS file
to a lossy preview format.

For science operations, preserve the raw FITS files and their metadata. Treat
browser display state as a convenience layer only.

A normal acquisition loop is:

#. Acquire and center the target on the intended fiber using the guide-side
   acquisition system.
#. Confirm guiding and record any offsets or nonstandard fiber selection.
#. Enter the observer name, target, image type, exposure time, binning, and any
   useful comment; verify the active instrument configuration before starting
   the exposure.
#. Acquire the science frame, then inspect the detector image for saturation,
   clipping, unexpected background, trace motion, and obvious focus changes.
#. Repeat or adjust the exposure only after preserving the original frame and
   recording the reason for the change.

Calibrations
------------

The final calibration plan must be established during commissioning and tied to
the pipeline's actual requirements. The observing sequence should nevertheless
distinguish the purpose of each calibration:

* **bias or zero-exposure frames** characterize electronic offsets when the
  selected camera mode requires them;
* **dark frames** characterize exposure-dependent detector signal when it is
  significant and not otherwise modeled;
* **continuum or flat-field frames** locate the fiber traces and characterize
  pixel/fiber response;
* **comparison-lamp or other wavelength references** establish the wavelength
  solution; and
* **spectrophotometric standards** measure the end-to-end response and monitor
  telluric and transparency effects.

Record the camera mode, exposure time, temperature, focus, aperture, filter,
grating configuration, and illumination source needed to associate each
calibration with its science frames.

Focus and alignment checks
--------------------------

A successful camera connection should not be treated as evidence that the
spectrograph is in focus or aligned. Use an appropriate continuum or line
source to inspect trace width, separation, spectral-line width, and field
dependence. Preserve the focus metric and controller position rather than
relying only on a visual assessment. Recheck focus after meaningful temperature
changes or any mechanical intervention.

End of night
------------

#. Complete any required closing calibrations before changing the optical
   configuration.
#. Verify that all expected files are present, readable, and copied to the
   observatory's normal data-protection location.
#. Record failed exposures, configuration changes, anomalies, and hardware
   interventions in the observing log.
#. Return mechanisms and the detector to their approved safe state, then stop
   services and power down according to the deployment runbook.

Fault handling
--------------

If a device disconnects or telemetry becomes implausible, stop the affected
operation and preserve the current data and log state. Power should not be
repeatedly cycled, and mechanisms or the camera should not be reinitialized,
without first checking the hardware-specific procedure. The completed manual
should include verified recovery steps for at least camera communication,
cooling, focus control, guide/telescope telemetry, failed FITS writes, and
interrupted exposures.

ACE Alpaca bridge
-----------------

The ACE Alpaca bridge should be running on the TCS-side computer before the ICS
``tcs`` or ``guide_camera`` backend is set to ``alpaca``. Confirm that Alpaca
discovery reports Telescope 0, Focuser 0, and Camera 0, then test only the
devices required for that observing mode.
The bridge provides explicit telescope, focus, and guide-camera control
operations; it is not a generic ACE remote-execution service.

The current bridge does not expose the guide-camera X/Y stage. The ICS supports
only the mock stage backend and explicitly rejects ``stage = alpaca``; the
setting should remain ``mock`` until the native stage has a verified network
mapping. The guide/acquisition camera can independently use
``guide_camera = alpaca`` with Camera 0.

Operational caution
-------------------

Hardware configuration, device names, ports, and credentials are deployment
configuration, not library defaults. Credentials should be kept out of the
repository and supplied through the deployment ``config.ini`` or
secret-management system.
