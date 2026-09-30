Camera: FLI Aurora AR571
========================

The FLI Aurora ``AR571``, which uses a Sony ``IMX571`` CMOS sensor, is the
modeled science-camera baseline and ETC default. The sensor format and pixel
size are central inputs to the simulator, ETC, and pipeline geometry. The ETC
also supports other camera models for comparison.

.. list-table:: Key catalog and configured properties
   :header-rows: 1
   :widths: 40 60

   * - Property
     - Value
   * - Sensor
     - Sony IMX571
   * - Active pixels
     - 6244 × 4168
   * - Pixel size
     - 3.76 µm × 3.76 µm
   * - Active area
     - 28.2 mm diagonal
   * - Digitization
     - 16 bit
   * - Read noise
     - Approximately 1 e⁻
   * - Dark current
     - Approximately 0.002 e⁻ pixel⁻¹ s⁻¹ at -20 °C
   * - Full well
     - Approximately 50,000 e⁻
   * - Peak quantum efficiency
     - Approximately 91%
   * - Interface
     - USB 3 / QSFP
   * - Shutter
     - Rolling
   * - Maximum frame rate
     - 7 frames s⁻¹

Read noise, dark current, frame rate, full well, and cooling performance depend
on readout and operating mode. The ETC models 1 e⁻ read noise and
0.002 e⁻ pixel⁻¹ s⁻¹ dark current at -20 °C.

The table gives native-sensor properties, which are also what the simulator's
``FLI_AR571`` preset stores. Readout binning is selected on each
``InstrumentSimulator`` instance. For example, ``binning=2`` produces 3122 ×
2084 output samples with an effective 7.52 µm sampling while retaining the
native detector definition for charge and saturation calculations.

Vendor resources
----------------

* `FLI AR571 product page <https://www.flicamera.com/models/ar571>`_
* `FLI Aurora camera family <https://www.flicamera.com/product/aurora-cmos-camera>`_
