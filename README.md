# MRImultiAtlasForNeonatalRabbitBrain (MRIrb)

Code for the benchmarking and validation of the Neonatal Rabbit brain Multi-Atlas 
(downloadable [here][multiatlasonzenodo] - coming soon) and to reproduce the
figures of the [documentation][paperlink] - (coming soon)

## How to use 

+ Requirements
    - Python 2 (**Python 2 only** for the current release)
    - Install [SPOT-A-NeonatalRabbit][spotaneonatalrabbit] and related dependencies
    - Download the data from [here][multiatlasonzenodo] - coming soon 
    
+ Installation
    - We recommend to install the software in development mode, inside a python [virtual-environment][virtualenvironment] with the following commands.
        ```
        cd <folder where to clone the code>
        git clone https://github.com/SebastianoF/MRImultiAtlasForNeonatalRabbitBrain.git
        cd MRImultiAtlasForNeonatalRabbitBrain
        source <virual-env with the required libraries>/bin/activate
        pip install -e .
        ```
+ Setup
    - After downloading the dataset - coming soon - set the path in 
    the python module `./path manager.py` as indicated in the comments.

## Code testing
The core methods are in the external libraries. Run the tests of 
[LABelsToolkit][labelstoolkit] and [SPOT-A-NeonatalRabbit][spotaneonatalrabbit] before starting.

## Support and contribution
Please see the [contribution guideline][contributionguideline] for bugs report,
feature requests, code re-factoring and re-styling.


## Authors and Acknowledgments

+ The MRI Neonatal Rabbit Multi-Atlas and related code is developed within the [gift-SURG research project][giftsurg] in collaboration with KU Leuven (Belgium) and UCL (UK).
+ This work was supported by Wellcome / Engineering and Physical Sciences Research Council (EPSRC) [WT101957; NS/A000027/1; 203145Z/16/Z]. 
+ The upcomging documentation with provide the full list of authors and acknowledgments.



[paperlink]: coming_soon
[multiatlasonzenodo]: coming_soon
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