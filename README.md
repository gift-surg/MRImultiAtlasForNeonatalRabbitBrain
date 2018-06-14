
<p align="center"> 
<img src="https://github.com/gift-surg/MRImultiAtlasForNeonatalRabbitBrain/blob/master/docs/annotated_slice.jpg" width="400">
</p>


# A Magnetic Resonance Multi-Atlas For Neonatal Rabbit Brain (nrBrain)

[Repository][this_repository] with the Python code for the benchmarking and validation of the Neonatal Rabbit brain Multi-Atlas
proposed in the [Neuroimage paper][paperlink]. Dataset can be found [here][multiatlasonzenodo]. 

## How to use 

+ Requirements
    - Python 2 (**Python 2 only** for the current release)
    - Install [SPOT-A-NeonatalRabbit][spotaneonatalrabbit] and related dependencies
    - Download the data from the zenodo repository [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1289776.svg)](https://doi.org/10.5281/zenodo.1289776)
    
+ Setup
    - After downloading the dataset, set the path in 
    the python module `./path manager.py` as indicated in the comments. In this module you will find the only 
    paths that you will need to change.
    - As a research software, sometimes important indications are annotated into comments inside the code.

+ Usage
    - We suggest to install the required libraries in a [virtual-environment][virtualenvironment].
    - Each module in the project structure can be run independently from command line.


## Code testing
The core methods are in the external libraries. Run the tests of 
[LABelsToolkit][labelstoolkit] and [SPOT-A-NeonatalRabbit][spotaneonatalrabbit] before starting.

## Support and contribution
Please see the [contribution guideline][contributionguideline] for bugs report,
feature requests, code re-factoring and re-styling.


## Authors and Acknowledgments

+ The MRI Neonatal Rabbit Multi-Atlas and related code is developed within the [GIFT-surg research project][giftsurg], a 
 collaborative project between the Univeristy College London (UK) and Katolische Universitat Leuven (Belgium).
+ This work was supported by Wellcome / Engineering and Physical Sciences Research Council (EPSRC) [WT101957; NS/A000027/1; 203145Z/16/Z]. 
+ The full list of authors and acknowledgments can be found in the [Neuroimage paper][paperlink], please use the same reference
to cite the dataset and the code if you find it useful for your research.



[this_repository]: https://github.com/gift-surg/MRImultiAtlasForNeonatalRabbitBrain
[paperlink]: https://doi.org/10.1016/j.neuroimage.2018.06.029
[multiatlasonzenodo]: https://doi.org/10.5281/zenodo.1289776
[spotaneonatalrabbit]: https://github.com/gift-surg/SPOT-A-NeonatalRabbit
[giftsurg]: http://www.gift-surg.ac.uk
[niftyreg]: http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftyReg
[niftyseg]: http://cmictig.cs.ucl.ac.uk/research/software/software-nifty/niftyseg
[niftk]: http://cmictig.cs.ucl.ac.uk/research/software/software-nifty/niftyview
[labelstoolkit]: https://github.com/SebastianoF/LABelsToolkit
[requirementstxt]: https://github.com/gift-surg/SPOT-A-NeonatalRabbit/blob/master/requirements.txt
[examplesfolder]: https://github.com/gift-surg/SPOT-A-NeonatalRabbit/blob/master/examples
[testingfolder]: https://github.com/gift-surg/SPOT-A-NeonatalRabbit/blob/master/tests
[contributionguideline]: https://github.com/gift-surg/MRImultiAtlasForNeonatalRabbitBrain/blob/master/CONTRIBUTE.md
[mrira]: https://github.com/gift-surg/MRImultiAtlasForNeonatalRabbitBrain
[licence]: https://github.com/gift-surg/SPOT-A-NeonatalRabbit/blob/master/LICENCE.txt
[nosetest]: http://pythontesting.net/framework/nose/nose-introduction/
[virtualenvironment]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[wikipage]: https://github.com/gift-surg/SPOT-A-NeonatalRabbit/wiki