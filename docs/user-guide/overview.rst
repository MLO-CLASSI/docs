Instrument overview
===================

Purpose and scope
-----------------

CLASSI is a low-resolution, fiber-fed spectrograph for rapid optical
spectroscopy at Mount Laguna Observatory. The instrument combines a telescope
focal-plane fiber input, a compact bench spectrograph, a cooled scientific CMOS
detector, an instrument control system, and a common set of planning,
simulation, and reduction tools.

This page defines the system-level view used throughout the manual. Individual
component specifications are collected in :doc:`../hardware/index`; software
interfaces are documented under :doc:`../packages/index`.

System at a glance
------------------

The light and data paths are:

.. code-block:: text

   sky -> telescope -> focal-plane fiber bundle -> fiber run
        -> collimator -> optional order-blocking filter -> reflection grating
        -> camera lens -> science detector -> raw FITS exposure
        -> calibration and extraction -> one-dimensional spectra

The principal spectrograph components currently documented are:

.. list-table:: Principal optical and detector components
   :header-rows: 1
   :widths: 28 32 40

   * - Subsystem
     - Current component
     - System role
   * - Fiber feed
     - Thorlabs FG105LVA, 105 µm core
     - Samples the telescope focal plane and defines the entrance-aperture scale.
   * - Collimator
     - Thorlabs AC508-180-AB-ML, 180 mm EFL
     - Converts the diverging fiber output into the beam incident on the grating.
   * - Order blocking
     - Removable Thorlabs FGL400S
     - Suppresses blue second-order contamination when installed.
   * - Disperser
     - Newport 270R, master 1294, 300 grooves/mm
     - Produces the low-resolution spectrum in first order.
   * - Camera optic
     - Canon EF 100mm f/2 USM
     - Images the dispersed beam onto the detector.
   * - Science detector
     - FLI Aurora AR571, 6244 × 4168, 3.76 µm pixels
     - Records the two-dimensional fiber spectra.

These are component or configured values. Spectral coverage, resolution,
throughput, trace locations, focus, and limiting sensitivity are properties of
the assembled system and must ultimately be measured in commissioning.

Operational subsystems
----------------------

CLASSI operation spans several connected subsystems:

* the telescope and guide-side hardware, which place and hold the target on the
  fiber input;
* the fiber feed and bench spectrograph, which transport and disperse the light;
* the science camera and camera-lens controller, which set focus/aperture and
  acquire detector frames;
* the instrument control system (ICS), which presents status and acquisition
  controls and writes science FITS files; and
* the planning and reduction software, which predicts exposure performance and
  turns detector frames into calibrated spectra.

An observation is successful only when all of these layers are configured
consistently. For example, the filter state, grating geometry, camera mode,
detector temperature, and focus used at the telescope must agree with the
configuration assumed during planning and reduction.

Primary data products
---------------------

The raw science-camera FITS files are the authoritative record of an exposure.
Browser displays, quick-look plots, ETC results, and simulated frames are
derived or predictive products. A complete observing dataset should retain:

* raw science and calibration frames;
* the acquisition and instrument metadata written with those frames;
* observing notes and any configuration changes made during the night;
* reduction configuration and software versions; and
* extracted spectra together with their uncertainties and masks.

Where to go next
----------------

Read :doc:`architecture` for the boundaries between physical, control, and
software subsystems. Observers can then proceed to :doc:`planning` and
:doc:`observing`; instrument characterization belongs in
:doc:`../hardware/index` and the reference section.
