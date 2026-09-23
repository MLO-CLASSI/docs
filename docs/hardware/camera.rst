Camera: FLI Aurora AR571
========================

The current modeled science-camera baseline and ETC default is the FLI Aurora
``AR571``, which uses a Sony ``IMX571`` CMOS sensor. The sensor format and pixel
size are central inputs to the simulator, ETC, and pipeline geometry. Other
camera models, including the earlier Kepler configuration, remain selectable
in the ETC for comparison.

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
on readout and operating mode. The ETC currently models 1 e⁻ read noise and
0.002 e⁻ pixel⁻¹ s⁻¹ dark current at -20 °C.

Vendor resources
----------------

* `FLI AR571 product page <https://www.flicamera.com/models/ar571>`_
* `FLI Aurora camera family <https://www.flicamera.com/product/aurora-cmos-camera>`_
