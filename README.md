# Heterogeneous Z Correction
ImageJ plugin to correct intensity attenuation in confocal images heterogeneously.
<img src="https://raw.githubusercontent.com/alexandrebastien/heterogeneous-z-correction/main/gui.png" align="right" width="200" >

## Notes
  * Please use Sphere_Builder.txt to generate a valid region image for testing
  * Your region should be painted in a z-stack with one unique integer value per region.
  * You need to provide the rational coefficients for each region, including the mounting media.
  * Coefficients should be guess from z-stack's intensities drop. They varie according to your objective specs, pinhole size, mounting media and cell's refractive index.
  
## Installation
  * This plugin could be installed by copying *.py and *.ijm to ./Plugins/Scripts/ in your [Fiji/ImageJ](https://imagej.net/Fiji)
  * You can also use [ImageJ Update Site](https://imagej.net/Update_Sites) : https://sites.imagej.net/Abastien/ (soon...)
  
## Citations
  * An article is in redaction at the moment. If you use this plugin in your work for publication, please contact the author to cite properly.

## License
Heterogeneous Z Correction is licensed under MIT opensource license. See https://opensource.org/licenses/MIT
