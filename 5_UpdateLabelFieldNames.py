import arcpy

standardLabel = 'StandardLabel'
displayLabel = 'DisplayLabel'
simpleExpressions = {'eSupportStructure':[standardLabel,'FACILITYID'],'eRecloser':[standardLabel,'DEVICEID'],'eSectionalizer':[standardLabel,'DEVICEID'],'eCircuitBreaker':[standardLabel,'DEVICEID'],'eSecOHElectricLineCond':[standardLabel,'CONDUCTORDESCRIPTION'],'eSecUGElectricLineCond':[standardLabel,'CONDUCTORDESCRIPTION']}
txRatedKVAA = {'25 KVA':'75 KVA-ABC','37.5 KVA':'112.5 KVA-ABC','50 KVA':'150 KVA-ABC','75 KVA':'225 KVA-ABC','100 KVA':'300 KVA-ABC','167 KVA':'500 KVA-ABC','250 KVA':'750 KVA-ABC','333 KVA':'1000 KVA-ABC','500 KVA':'1500 KVA-ABC','667 KVA':'2000 KVA-ABC','833 KVA':'2500 KVA-ABC','1000 KVA':'3000 KVA-ABC','1250 KVA':'3750'}
wksp = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb'
fc = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\%s'

def getPhaseDesignation(phaseDesignation):
        if phaseDesignation is None:
                ph = 'Unk'
                return ph
        if phaseDesignation == 1:
                ph = '-C'
                return ph
        if phaseDesignation == 2:
                ph = '-B'
                return ph
        if phaseDesignation == 3:
                ph = '-BC'
                return ph
        if phaseDesignation == 4:
                ph = '-A'
                return ph
        if phaseDesignation == 5:
                ph = '-AC'
                return ph
        if phaseDesignation == 6:
                ph = '-AB'
                return ph
        if phaseDesignation == 7:
                ph = '-ABC'
                return ph

#try:
#with arcpy.da.Editor(wksp) as edit:
edit = arcpy.da.Editor(wksp)
edit.startEditing()
# Start an edit operation
edit.startOperation()

for k,v in simpleExpressions.iteritems():
        print 'Processing %-5s %s' % (k,v)
        with arcpy.da.UpdateCursor(fc%(k),v) as uc:
                for ucRow in uc:
                        ucRow[0] = ucRow[1]
                        uc.updateRow(ucRow)

# ServicePoint
#with arcpy.da.Editor(wksp) as edit:
print 'Processing %-5s %s' % ('eServicePoint',standardLabel)
with arcpy.da.UpdateCursor(wksp + '\eServicePoint',['StandardLabel','METERTYPE'],"METERTYPE = 'UGTRAF' OR METERTYPE = 'OHTRAF'") as svcpntuc:
       for svcpnt in svcpntuc:
               svcpnt[0] = 'Traffic'
               svcpntuc.updateRow(svcpnt)
# TransformerBank
#with arcpy.da.Editor(wksp) as edit:
print 'Processing %-5s %s' % ('eTransformerBank',standardLabel)
with arcpy.da.UpdateCursor(wksp + '\eTransformerBank',['StandardLabel','DeviceID','Subtype','RatedKVA_A','RatedKVA_B','RatedKVA_C','RatedKVA_Spare','PhaseDesignation','Purpose']) as txuc:
       for tx in txuc:
               if tx[7] is not None:
                       phase = getPhaseDesignation(tx[7])                          
               if tx[1] is not None and tx[1][:3].upper() not in ('NON','UNK',' '):
                       deviceID = tx[1]
               # OH 1PH
               if tx[2] == 1:
                       if tx[3] is not None and tx[3] != 'NONE':
                               tx[0] = tx[3] + phase
                               txuc.updateRow(tx)
                       if tx[4] is not None and tx[3] != 'NONE':
                               tx[0] = tx[4] + phase
                               txuc.updateRow(tx)
                       if tx[5] is not None and tx[3] != 'NONE':
                               tx[0] = tx[5] + phase
                               txuc.updateRow(tx)
                       if tx[6] is not None and tx[3] != 'NONE':
                               tx[0] = tx[6] + '-Spare'
                               txuc.updateRow(tx)
               # OH 2PH
               if tx[2] == 2:
                       # check OH 2PH BC
                       if tx[7] == 3:
                               tx[0] = tx[4] + ',' + tx[5] + phase
                               txuc.updateRow(tx)
                       # check OH 2PH AC
                       if tx[7] == 5:
                               tx[0] = tx[3] + ',' + tx[5] + phase
                               txuc.updateRow(tx)
                       # check OH 2PH AB
                       if tx[7] == 6:
                               tx[0] = tx[3] + ',' + tx[4] + phase
                               txuc.updateRow(tx)
                       # check OH 3PH
                       if tx[7] == 7:
                               tx[0] = tx[3] + ',' + tx[4] + ',' + tx[5] + phase
                               txuc.updateRow(tx)
               # OH 3PH
               if tx[2] == 3:
                       if tx[3] == tx[4] == tx[5]:
                               tx[0] = tx[3] + phase
                       else:
                               tx[0] = tx[3] + ',' + tx[4] + ',' + tx[5] + phase
                       txuc.updateRow(tx) 
               # UG 1PH
               if tx[2] == 4:
                       if tx[3] is not None and tx[3] != 'NONE':
                               tx[0] = deviceID + ' ' + tx[3] + phase
                               txuc.updateRow(tx)
                       if tx[4] is not None and tx[4] != 'NONE':
                               tx[0] = deviceID + ' ' + tx[4] + phase
                               txuc.updateRow(tx)
                       if tx[5] is not None and tx[5] != 'NONE':
                               tx[0] = deviceID + ' ' + tx[5] + phase
                               txuc.updateRow(tx)
                       if tx[6] is not None and tx[6] != 'NONE':
                               tx[0] = deviceID + ' ' + tx[6] + '-Spare'
                               txuc.updateRow(tx)
               # UG 3PH
               if tx[2] in [5,7,9]:
                       for k,v in txRatedKVAA.iteritems():
                               if tx[3] == k:
                                       tx[0] = deviceID + ' ' + v
                                       txuc.updateRow(tx)
# Fuse
#with arcpy.da.Editor(wksp) as edit:
print 'Processing %-5s %s' % ('eFuse',standardLabel)
with arcpy.da.UpdateCursor(wksp + '\eFuse',['StandardLabel','DeviceID','Subtype','Rating_A','Rating_B','Rating_C','PhaseDesignation','STATUS','FacilityID','DisplayLabel'],"STATUS = '1'") as fuseuc:
       for fuse in fuseuc:
               phase = ''
               deviceID = ''
               if fuse[6] is not None:
                       phase = getPhaseDesignation(fuse[6])
               if fuse[1][:3].upper() not in ['NON','UNK','']:
                       deviceID = fuse[1] + ' '
                       if fuse[6] == 1:
                               fuse[0] = deviceID + fuse[5] + phase
                               fuse[9] = fuse[8] + fuse[5] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 2:
                               fuse[0] = deviceID + fuse[4] + phase
                               fuse[9] = fuse[8] + fuse[4] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 3:
                               fuse[0] = deviceID + fuse[4] + phase
                               fuse[9] = fuse[8] + fuse[4] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 4:
                               fuse[0] = deviceID + fuse[3] + phase
                               fuse[9] = fuse[8] + fuse[3] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 5:
                               fuse[0] = deviceID + fuse[5] + phase
                               fuse[9] = fuse[8] + fuse[5] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 6:
                               fuse[0] = deviceID + fuse[3] + phase
                               fuse[9] = fuse[8] + fuse[3] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 7:
                               fuse[0] = deviceID + ',' + fuse[3] + phase
                               fuse[9] = fuse[8] + fuse[3] + phase
                               fuseuc.updateRow(fuse)
               else:
                       if fuse[6] == 1:
                               fuse[0] = fuse[5] + phase
                               fuse[9] = fuse[8] + fuse[5] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 2:
                               fuse[0] = fuse[4] + phase
                               fuse[9] = fuse[8] + fuse[4] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 3:
                               fuse[0] = fuse[5] + phase
                               fuse[9] = fuse[8] + fuse[5] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 4:
                               fuse[0] = fuse[3] + phase
                               fuse[9] = fuse[8] + fuse[3] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 5:
                               fuse[0] = fuse[5] + phase
                               fuse[9] = fuse[8] + fuse[5] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 6:
                               fuse[0] = fuse[3] + phase
                               fuse[9] = fuse[8] + fuse[3] + phase
                               fuseuc.updateRow(fuse)
                       if fuse[6] == 7:
                               fuse[0] = fuse[5] + phase
                               fuse[9] = fuse[8] + fuse[5] + phase
                               fuseuc.updateRow(fuse)
# Switch CapacitorBank
#with arcpy.da.Editor(wksp) as edit:
devices = ['\eSwitch','\eCapacitorBank']
for device in devices:
       print 'Processing %-5s %s' % (device,standardLabel)
       with arcpy.da.UpdateCursor(wksp + device,['StandardLabel','DeviceID']) as equipmentuc:
               for equipment in equipmentuc:
                       if equipment[1] is None:
                              pass
                       else:
                               if equipment[1][:3].upper() not in ['NON','UNK','']:
                                       equipment[0] = equipment[1]
                                       equipmentuc.updateRow(equipment)
# Cabinet Pad
#with arcpy.da.Editor(wksp) as edit:
structures = ['\eCabinetStructure','\eSurfaceStructure']
for structure in structures:
       print 'Processing %-5s %s' % (structure,standardLabel)
       with arcpy.da.UpdateCursor(wksp + structure,['StandardLabel','FacilityID']) as structureuc:
               for structurerow in structureuc:
                       if structurerow[1][:3].upper() not in ['NON','UNK','TEL','PVT','']:
                               structurerow[0] = structurerow[1]
                               structureuc.updateRow(structurerow)
# VoltRegBank
#with arcpy.da.Editor(wksp) as edit:
print 'Processing %-5s %s' % ('eVoltageRegulatorBank',standardLabel)
with arcpy.da.UpdateCursor(wksp + '\eVoltageRegulatorBank',['StandardLabel','DeviceID','RATEDKVA']) as regbankuc:
       for regbank in regbankuc:
               if regbank[1][:3].upper() not in ['NON','UNK','']:
                       regbank[0] = regbank[1] + ' ' + regbank[2]
                       regbankuc.updateRow(regbank)

# Light
#with arcpy.da.Editor(wksp) as edit:
print 'Processing %-5s %s' % ('eLight',standardLabel)
with arcpy.da.UpdateCursor(wksp + '\eLight',[standardLabel,'Unit_Type']) as lightuc:
        for light in lightuc:
                if light[1] is None or light[1].upper() == 'UNMATCHED':
                        pass
                else:
                        light[0] = light[1].split('_',2)[2]
                        lightuc.updateRow(light)
print 'Processing %-5s %s' % ('eLight',displayLabel)
with arcpy.da.UpdateCursor(wksp + '\eLight',[displayLabel,'FacilityID','Unit_Type']) as lightuc:
       for light in lightuc:
               if light[1] is None or light[2] is None or light[2].upper() == 'UNMATCHED':
                       pass
               else:
                       light[0] = light[1] + ' - ' + light[2].split('_',2)[2]
                       lightuc.updateRow(light)
# OH Primary
#with arcpy.da.Editor(wksp) as edit:
print 'Processing %-5s %s' % ('ePriOHElectricLineCond',standardLabel)
with arcpy.da.UpdateCursor(wksp + '\ePriOHElectricLineCond',['StandardLabel','FeederID','PhaseDesignation']) as ohpuc:
       for ohp in ohpuc:
               if ohp[1] is None:
                       feederID = 'Unk'
               else:
                       feederID = ohp[1]                       
               ohp[0] = feederID + getPhaseDesignation(ohp[2])
               ohpuc.updateRow(ohp)

# UG Primary
#with arcpy.da.Editor(wksp) as edit:
print 'Processing %-5s %s' % ('ePriUGElectricLineCond',standardLabel)
with arcpy.da.UpdateCursor(wksp + '\ePriUGElectricLineCond',['StandardLabel','FeederID','PhaseDesignation','SegmentID']) as ugpuc:
       for ugp in ugpuc:
               if ugp[1] is None:
                       feederID = 'Unk'
               else:
                       feederID = ugp[1]
               if ugp[3] is None:
                       segmentID = 'Unk'
               else:
                       segmentID = ugp[3]
               if segmentID.upper() not in ['0','0000','xxxx','']:
                       ugp[0] = feederID + getPhaseDesignation(ugp[2]) + ' ' + segmentID
                       ugpuc.updateRow(ugp)
               elif segmentID.upper() in ['0','0000','xxxx','']:
                       ugp[0] = feederID + getPhaseDesignation(ugp[2]) + ' ' + segmentID
                       ugpuc.updateRow(ugp)
##except:
### Stop the edit operation.
##edit.stopOperation()
### Stop the edit session and save the changes
##edit.stopEditing(False)
##print 'Something failed'
##exit
##finally:
# Stop the edit operation.
edit.stopOperation()
# Stop the edit session and save the changes
edit.stopEditing(True)


# wksp = 'Database Connections/grucwgisdv01_MapED_OSAuth.sde'

# with arcpy.da.Editor(wksp) as edit:
        # # GRUAddressPoints
        # print 'Processing %-5s %s' % ('GRUAddressPoints', standardLabel)
        # with arcpy.da.UpdateCursor('Database Connections/grucwgisdv01_MapED_OSAuth.sde/mapedpr.ARCFM_ED.Cartographic/mapedpr.ARCFM_ED.GRUAddressPoints',['StandardLabel','STREETNUMBER','UNITNUMBER']) as addressuc:
                # for address in addressuc:
                        # if address[2] is not None and address[2] != '':
                                # address[0] = address[1] + '-' + address[2]
                                # addressuc.updateRow(address)
                        # else:
                                # address[0] = address[1]
                                # addressuc.updateRow(address)
    # # LBF108 LBF408
    # with arcpy.da.UpdateCursor(r'C:\arcdata\ED_Extract.gdb\Electric\eFuse',["StockCode"],"Subtype = 3 AND PHASEDESIGNATION IN (4,2,1,7) AND (RATING_A = '8' OR RATING_B = '8' OR RATING_C = '8')") as uc:
        # for ucRow in uc:
            # ucRow[0] = 611034
            # uc.updateRow(ucRow)
    # # LBF112 LBF412
    # with arcpy.da.UpdateCursor(r'C:\arcdata\ED_Extract.gdb\Electric\eFuse',["StockCode"],"Subtype = 3 AND PHASEDESIGNATION IN (4,2,1,7) AND (RATING_A = '12' OR RATING_B = '12' OR RATING_C = '12')") as uc:
        # for ucRow in uc:
            # ucRow[0] = 611085
            # uc.updateRow(ucRow)
    # # LBF118 LBF418
    # with arcpy.da.UpdateCursor(r'C:\arcdata\ED_Extract.gdb\Electric\eFuse',["StockCode"],"Subtype = 3 AND PHASEDESIGNATION IN (4,2,1,7) AND (RATING_A = '18' OR RATING_B = '18' OR RATING_C = '18')") as uc:
        # for ucRow in uc:
            # ucRow[0] = 611131
            # uc.updateRow(ucRow)
    # # LBF130 LBF430
    # with arcpy.da.UpdateCursor(r'C:\arcdata\ED_Extract.gdb\Electric\eFuse',["StockCode"],"Subtype = 3 AND PHASEDESIGNATION IN (4,2,1,7) AND (RATING_A = '30' OR RATING_B = '30' OR RATING_C = '30')") as uc:
        # for ucRow in uc:
            # ucRow[0] = 611182
            # uc.updateRow(ucRow)
    # # CTA
    # with arcpy.da.UpdateCursor(r'C:\arcdata\ED_Extract.gdb\Electric\eFuse',["StockCode"],"Subtype = 1 AND PHASEDESIGNATION IN (4,2,1,7) AND (RATING_A = '100' OR RATING_B = '100' OR RATING_C = '100')") as uc:
        # for ucRow in uc:
            # ucRow[0] = 703435
            # uc.updateRow(ucRow)

        



        
