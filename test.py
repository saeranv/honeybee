# coding=utf-8
from honeybee.radiance.parameters.rfluxmtx import RfluxmtxParameters
from honeybee.radiance.command.rfluxmtx import Rfluxmtx
from honeybee.radiance.command.epw2wea import Epw2wea
from honeybee.radiance.command.gendaymtx import Gendaymtx
from honeybee.radiance.command.rmtxop import Rmtxop,RmtxopParameters


import os

os.chdir(r'tests\room')

#Step1: Create annual daylight vectors through epw2wea and gendaymtx.
weaFile = Epw2wea(epwFile='test.epw')
weaFile.execute()

genday = Gendaymtx(weaFile='test.wea',outputName='day.smx')
genday.execute()

#Step2: Generate daylight coefficients using rfluxmtx.
rfluxPara = RfluxmtxParameters()
rfluxPara.aa = 0.1
rfluxPara.ad= 2048
rfluxPara.ab = 5

rflux = Rfluxmtx()
rflux.sender = '-'
skyFile = rflux.defaultSkyGround('rfluxSky.rad')
rflux.receiverFile = skyFile
rflux.rfluxmtxParameters = rfluxPara
rflux.radFiles = [r"room.mat",
                  r"room.rad"]

rflux.pointsFile = r"indoor_points.pts"
rflux.outputMatrix = r"dayCoeff.dc"
print(rflux.toRadString())
rflux.execute()


mtx1 = Rmtxop(matrixFiles=(os.path.abspath(r'dayCoeff.dc'),os.path.abspath(r'day.smx')),
              outputFile=r'illuminance.tmp')
mtx1.execute()


mtx2Param = RmtxopParameters()
mtx2Param.outputFormat = 'a'
mtx2Param.combineValues = (47.4,119.9,11.6)
mtx2Param.transposeMatrix = True
mtx2 = Rmtxop(matrixFiles=['illuminance.tmp'],outputFile='illuminance.ill')
mtx2.rmtxopParameters = mtx2Param
mtx2.execute()

with open('illuminance.ill') as illFile:
    for lines in illFile:
        try:
            print(map(float,lines.split()))
        except ValueError:
            pass

