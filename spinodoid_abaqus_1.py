# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

image_no = 3

for iteration in range(1, image_no + 1):

    # Read input file for current iteration
    input_file = 'C:\\Users\\bksan\\Downloads\\Im2mesh\\Im2mesh\\image_{}.inp'.format(iteration)

    # Create model from input file
    mdb.ModelFromInputFile(inputFileName=input_file, name='image_{}'.format(iteration))

    # Define materials and sections for the current model
    mdb.models['image_{}'.format(iteration)].Material(name='Material-1')
    mdb.models['image_{}'.format(iteration)].materials['Material-1'].Elastic(table=((110.0, 0.3), ))

    mdb.models['image_{}'.format(iteration)].sections['Section-1-SET-A'].setValues(
        material='Material-1', thickness=1.0)

    mdb.models['image_{}'.format(iteration)].Material(name='Material-2')
    mdb.models['image_{}'.format(iteration)].materials['Material-2'].Elastic(table=((1e-15, 0), ))

    mdb.models['image_{}'.format(iteration)].sections['Section-2-SET-B'].setValues(
        material='Material-2', thickness=1.0)

    # Create and define steps for the current model
    mdb.models['image_{}'.format(iteration)].StaticStep(
        initialInc=0.1, maxNumInc=1000, minInc=1e-10, name='Step-1', previous='Initial')

    # Apply boundary conditions
    # mdb.models['image_{}'.format(iteration)].DisplacementBC(amplitude=UNSET, 
    # createStepName='Step-1', distributionType=UNIFORM, fieldName='', fixed=OFF, 
    # localCsys=None, name='BC-1', region=mdb.models['image_{}'.format(iteration)].rootAssembly.sets['SET-A-XMIN'], u1=0.0, u2=UNSET, ur3=UNSET)

    mdb.models['image_{}'.format(iteration)].DisplacementBC(
        amplitude=UNSET, createStepName='Step-1', distributionType=UNIFORM, fieldName='', 
        fixed=OFF, localCsys=None, name='BC-2', 
        region=mdb.models['image_{}'.format(iteration)].rootAssembly.sets['SET-A-YMIN'], 
        u1=0, u2=0.0, ur3=0)

    mdb.models['image_{}'.format(iteration)].DisplacementBC(
        amplitude=UNSET, createStepName='Step-1', distributionType=UNIFORM, 
        fieldName='', fixed=OFF, localCsys=None, name='BC-3', 
        region=mdb.models['image_{}'.format(iteration)].rootAssembly.sets['SET-A-YMAX'], 
        u1=UNSET, u2=1000.0, ur3=UNSET)

    # Create and submit the job for the current iteration
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model='image_{}'.format(iteration), 
        modelPrint=OFF, multiprocessingMode=DEFAULT, 
        name='output_image_spino-{}'.format(iteration), 
        nodalOutputPrecision=SINGLE, numCpus=1, numGPUs=0, 
        numThreadsPerMpiProcess=1, queue=None, resultsFormat=ODB, scratch='', 
        type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)

    mdb.jobs['output_image_spino-{}'.format(iteration)].submit()
    mdb.jobs['output_image_spino-{}'.format(iteration)].waitForCompletion()
