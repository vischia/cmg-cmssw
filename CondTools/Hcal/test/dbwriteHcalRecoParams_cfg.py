import FWCore.ParameterSet.Config as cms

process = cms.Process("TEST")

process.MessageLogger=cms.Service("MessageLogger",
                              destinations=cms.untracked.vstring("cout"),
                              cout=cms.untracked.PSet(
                              threshold=cms.untracked.string("INFO")
                              )
)

process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.CondDBCommon.connect = cms.string('sqlite_file:testExample.db')
process.CondDBCommon.DBParameters.authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')

process.source = cms.Source("EmptyIOVSource",
    timetype = cms.string('runnumber'),
    firstValue = cms.uint64(1),
    lastValue = cms.uint64(1),
    interval = cms.uint64(1)
)

process.es_ascii = cms.ESSource("HcalTextCalibrations",
    input = cms.VPSet(cms.PSet(
        object = cms.string('RecoParams'),
        file = cms.FileInPath('CondTools/Hcal/test/testdata/RecoParams2011-run153943.txt')
    ))
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    process.CondDBCommon,
    timetype = cms.untracked.string('runnumber'),
    logconnect= cms.untracked.string('sqlite_file:log.db'),
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('HcalRecoParamsRcd'),
        tag = cms.string('hcal_recoparams_v1.00_test')
         ))
)

process.mytest = cms.EDAnalyzer("HcalRecoParamsPopConAnalyzer",
    record = cms.string('HcalRecoParamsRcd'),
    loggingOn= cms.untracked.bool(True),
    SinceAppendMode=cms.bool(True),
    Source=cms.PSet(
#    firstSince=cms.untracked.double(300) 
    IOVRun=cms.untracked.uint32(1)
    )
)

process.p = cms.Path(process.mytest)
