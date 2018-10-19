#todo fix 'eSupportStructure_YEARMANUFACTU'
import arcpy,time

startTime = time.time()

# Poles use shape@ to create point feature for damage assessment
PoleFldsOrig = ['GLOBALID','SUBTYPE','OWNER','FACILITYID','POLESIZE','MATERIAL','COLOR','TREATMENTTYPE','YEARMANUFACTURED','STUBDATE','BILLINGGROUP','FEEDERIDS','INSTALL_NUM','UNIT_TYPE','STREETADDRESS','BACKBONEINDICATOR','SHAPE@']
PoleFldsDest = ['eSupportStructure_GLOBALID','eSupportStructure_SUBTYPE','eSupportStructure_OWNER','eSupportStructure_FACILITYID','eSupportStructure_POLESIZE','eSupportStructure_MATERIAL','eSupportStructure_COLOR','eSupportStructure_TREATMENTTYPE','eSupportStructure_YEARMANUFACTURED','eSupportStructure_STUBDATE','eSupportStructure_BILLINGGROUP','eSupportStructure_FEEDERIDS','eSupportStructure_INSTALLNUM','eSupportStructure_UNITTYPE','eSupportStructure_STREETADDRESS','eSupportStructure_BACKBONE','SHAPE@']

# feature classes that have 1:1 relationship with poles
CapBankFldsOrig = ['eSupportStructure_GLOBALID','DEVICEID','SUBTYPE','STRUCTUREID','GLOBALID']
CapBankFldsDest = ['eSupportStructure_GLOBALID','eCapacitorBank_DEVICEID','eCapacitorBank_SUBTYPE','eCapacitorBank_STRUCTUREID','eCapacitorBank_GLOBALID']
RecloserFldsOrig = ['eSupportStructure_GLOBALID','DEVICEID','FEEDERID','FEEDERID2','PHASEDESIGNATION','SUBTYPE','AMPRATING','BACKBONEPASSTHRU','CUSTOMERCOUNT','STRUCTUREID','INTERRUPTINGTYPE','INTERRUPTRATING','CONTROLLERTYPE','BACKBONEINDICATOR','GLOBALID']
RecloserFldsDest = ['eSupportStructure_GLOBALID','eRecloser_DEVICEID','eRecloser_FEEDERID','eRecloser_FEEDERID2','eRecloser_PHASE','eRecloser_SUBTYPE','eRecloser_AMPRATING','eRecloser_BACKBONEPASSTHRU','eRecloser_CUSTOMERCOUNT','eRecloser_STRUCTUREID','eRecloser_INTERRUPTINGTYPE','eRecloser_INTERRUPTRATING','eRecloser_CONTROLLERTYPE','eRecloser_BACKBONE','eRecloser_GLOBALID']
SectionalizerFldsOrig = ['eSupportStructure_GLOBALID','DEVICEID','FEEDERID','FEEDERID2','BACKBONEPASSTHRU','CUSTOMERCOUNT','STRUCTUREID','GLOBALID']
SectionalizerFldsDest = ['eSupportStructure_GLOBALID','eSectionalizer_DEVICEID','eSectionalizer_FEEDERID','eSectionalizer_FEEDERID2','eSectionalize_BACKBONEPASSTHRU','eSectionalizer_CUSTOMERCOUNT','eSectionalizer_STRUCTUREID','eSectionalizer_GLOBALID']
VoltRegBankFldsOrig = ['eSupportStructure_GLOBALID','DEVICEID','FEEDERID','STRUCTUREID','GLOBALID']
VoltRegBankFldsDest = ['eSupportStructure_GLOBALID','eVoltRegBank_DEVICEID','eVoltRegBank_FEEDERID','eVoltRegBank_STRUCTUREID','eVoltRegBank_GLOBALID']

# the following five feature classes have 1:n relationship with poles
# Fuse
FuseFldsOrig = ['eSupportStructure_GLOBALID','DEVICEID','FeederID','FeederID2','PhaseDesignation','SUBTYPE','RATING_A','RATING_B','RATING_C','LOADBREAK','BACKBONEEND','BACKBONEPASSTHRU','CUSTOMERCOUNT','STRUCTUREID','GLOBALID']
FuseFldsDest = ['eSupportStructure_GLOBALID','eFuse_DEVICEID','eFuse_FeederID','eFuse_FeederID2','eFuse_Phase','eFuse_SUBTYPE','eFuse_RATING_A','eFuse_RATING_B','eFuse_RATING_C','eFuse_LOADBREAK','eFuse_BACKBONEEND','eFuse_BACKBONEPASSTHRU','eFuse_CUSTOMERCOUNT','eFuse_STRUCTUREID','eFuse_GLOBALID']
FuseFldsDest2 = ['eSupportStructure_GLOBALID','eFuse_DEVICEID2','eFuse_FeederID_2','eFuse_FeederID22','eFuse_Phase2','eFuse_SUBTYPE2','eFuse_RATING_A2','eFuse_RATING_B2','eFuse_RATING_C2','eFuse_LOADBREAK2','eFuse_BACKBONEEND2','eFuse_BACKBONEPASSTHRU2','eFuse_CUSTOMERCOUNT2','eFuse_STRUCTUREID','eFuse_GLOBALID2']
FuseFldsDest3 = ['eSupportStructure_GLOBALID','eFuse_DEVICEID3','eFuse_FeederID3','eFuse_FeederID23','eFuse_Phase3','eFuse_SUBTYPE3','eFuse_RATING_A3','eFuse_RATING_B3','eFuse_RATING_C3','eFuse_LOADBREAK3','eFuse_BACKBONEEND3','eFuse_BACKBONEPASSTHRU3','eFuse_CUSTOMERCOUNT3','eFuse_STRUCTUREID','eFuse_GLOBALID3']
FuseFldsDest4 = ['eSupportStructure_GLOBALID','eFuse_DEVICEID4','eFuse_FeederID4','eFuse_FeederID24','eFuse_Phase4','eFuse_SUBTYPE4','eFuse_RATING_A4','eFuse_RATING_B4','eFuse_RATING_C4','eFuse_LOADBREAK4','eFuse_BACKBONEEND4','eFuse_BACKBONEPASSTHRU4','eFuse_CUSTOMERCOUNT4','eFuse_STRUCTUREID','eFuse_GLOBALID4']
FuseFldsDest5 = ['eSupportStructure_GLOBALID','eFuse_DEVICEID5','eFuse_FeederID5','eFuse_FeederID25','eFuse_Phase5','eFuse_SUBTYPE5','eFuse_RATING_A5','eFuse_RATING_B5','eFuse_RATING_C5','eFuse_LOADBREAK5','eFuse_BACKBONEEND5','eFuse_BACKBONEPASSTHRU5','eFuse_CUSTOMERCOUNT5','eFuse_STRUCTUREID','eFuse_GLOBALID5']
FuseFldsDest6 = ['eSupportStructure_GLOBALID','eFuse_DEVICEID6','eFuse_FeederID6','eFuse_FeederID26','eFuse_Phase6','eFuse_SUBTYPE6','eFuse_RATING_A6','eFuse_RATING_B6','eFuse_RATING_C6','eFuse_LOADBREAK6','eFuse_BACKBONEEND6','eFuse_BACKBONEPASSTHRU6','eFuse_CUSTOMERCOUNT6','eFuse_STRUCTUREID','eFuse_GLOBALID6']

# Lights
LightFldsOrig = ['eSupportStructure_GLOBALID','SUBTYPE','LAMP','COLOR','ARMDIRECTION','ARMLENGTH','STRUCTUREID','GLOBALID']
LightFldsDest = ['eSupportStructure_GLOBALID','eLight_SUBTYPE','eLIGHT_LAMP','eLight_COLOR','eLight_ARMDIRECTION','eLight_ARMLENGTH','eLight_STRUCTUREID','eLight_GLOBALID']
LightFldsDest2 = ['eSupportStructure_GLOBALID','eLight_SUBTYPE2','eLIGHT_LAMP2','eLight_COLOR2','eLight_ARMDIRECTION2','eLight_ARMLENGTH2','eLight_STRUCTUREID','eLight_GLOBALID2']
LightFldsDest3 = ['eSupportStructure_GLOBALID','eLight_SUBTYPE3','eLIGHT_LAMP3','eLight_COLOR3','eLight_ARMDIRECTION3','eLight_ARMLENGTH3','eLight_STRUCTUREID','eLight_GLOBALID3']
LightFldsDest4 = ['eSupportStructure_GLOBALID','eLight_SUBTYPE4','eLIGHT_LAMP4','eLight_COLOR4','eLight_ARMDIRECTION4','eLight_ARMLENGTH4','eLight_STRUCTUREID','eLight_GLOBALID4']

# Service Point
ServicePointFldsOrig = ['eSupportStructure_GLOBALID','SUBTYPE','FEEDERID','METERTYPE','PHASEDESIGNATION','CUSTOMERCOUNT','STREETADDRESS','PRIORITYREASON','GLOBALID']
ServicePointFldsDest = ['eSupportStructure_GLOBALID','eServicePoint_SUBTYPE','eServicePoint_FEEDERID','eServicePoint_METERTYPE','eServicePoint_PHASE','eServicePoint_CUSTOMERCOUNT','eServicePoint_STREETADDRESS','eServicePoint_PRIORITYREASON','eServicePoint_GLOBALID']
ServicePointFldsDest2 = ['eSupportStructure_GLOBALID','eServicePoint_SUBTYPE2','eServicePoint_FEEDERID_2','eServicePoint_METERTYPE2','eServicePoint_PHASE2','eServicePoint_CUSTOMERCOUNT2','eServicePoint_STREETADDRESS2','eServicePoint_PRIORITYREASON2','eServicePoint_GLOBALID2']
ServicePointFldsDest3 = ['eSupportStructure_GLOBALID','eServicePoint_SUBTYPE3','eServicePoint_FEEDERID3','eServicePoint_METERTYPE3','eServicePoint_PHASE3','eServicePoint_CUSTOMERCOUNT3','eServicePoint_STREETADDRESS3','eServicePoint_PRIORITYREASON3','eServicePoint_GLOBALID3']
ServicePointFldsDest4 = ['eSupportStructure_GLOBALID','eServicePoint_SUBTYPE4','eServicePoint_FEEDERID4','eServicePoint_METERTYPE4','eServicePoint_PHASE4','eServicePoint_CUSTOMERCOUNT4','eServicePoint_STREETADDRESS4','eServicePoint_PRIORITYREASON4','eServicePoint_GLOBALID4']

# Switch
SwitchFldsOrig = ['eSupportStructure_GLOBALID','DEVICEID','FEEDERID','FEEDERID2','PHASEDESIGNATION','SUBTYPE','GANGOPERATED','LOADBREAK','STRUCTUREID','CUSTOMERCOUNT','AUTOTRANSFER','CONTROLLERTYPE','MOTOROPERATED','BACKBONEINDICATOR','BYPASSINDICATOR','GLOBALID']
SwitchFldsDest = ['eSupportStructure_GLOBALID','eSwitch_DEVICEID','eSwitch_FEEDERID','eSwitch_FEEDERID2','eSwitch_PHASE','eSwitch_SUBTYPE','eSwitch_GANGOPERATED','eSwitch_LOADBREAK','eSwitch_STRUCTUREID','eSwitch_CUSTOMERCOUNT','eSwitch_AUTOTRANSFER','eSwitch_CONTROLLERTYPE','eSwitch_MOTOROPERATED','eSwitch_BACKBONE','eSwitch_BYPASS','eSwitch_GLOBALID']
SwitchFldsDest2 = ['eSupportStructure_GLOBALID','eSwitch_DEVICEID2','eSwitch_FEEDERID_2','eSwitch_FEEDERID22','eSwitch_PHASE2','eSwitch_SUBTYPE2','eSwitch_GANGOPERATED2','eSwitch_LOADBREAK2','eSwitch_STRUCTUREID','eSwitch_CUSTOMERCOUNT2','eSwitch_AUTOTRANSFER2','eSwitch_CONTROLLERTYPE2','eSwitch_MOTOROPERATED2','eSwitch_BACKBONE2','eSwitch_BYPASS2','eSwitch_GLOBALID2']
SwitchFldsDest3 = ['eSupportStructure_GLOBALID','eSwitch_DEVICEID3','eSwitch_FEEDERID3','eSwitch_FEEDERID23','eSwitch_PHASE3','eSwitch_SUBTYPE3','eSwitch_GANGOPERATED3','eSwitch_LOADBREAK3','eSwitch_STRUCTUREID','eSwitch_CUSTOMERCOUNT3','eSwitch_AUTOTRANSFER3','eSwitch_CONTROLLERTYPE3','eSwitch_MOTOROPERATED3','eSwitch_BACKBONE3','eSwitch_BYPASS3','eSwitch_GLOBALID3']

# Transformer Bank
TXFldsOrig = ['eSupportStructure_GLOBALID','DEVICEID','FEEDERID','FEEDERID2','PHASEDESIGNATION','SUBTYPE','RATEDKVA_A','RATEDKVA_B','RATEDKVA_C','CUSTOMERCOUNT','STRUCTUREID','PURPOSE','GLOBALID']
TXFldsDest = ['eSupportStructure_GLOBALID','eTX_DEVICEID','eTX_FEEDERID','eTX_FEEDERID2','eTX_PHASE','eTX_SUBTYPE','eTX_RATEDKVA_A','eTX_RATEDKVA_B','eTX_RATEDKVA_C','eTX_CUSTOMERCOUNT','eTX_STRUCTUREID','eTX_PURPOSE','eTX_GLOBALID']
TXFldsDest2 = ['eSupportStructure_GLOBALID','eTX_DEVICEID2','eTX_FEEDERID_2','eTX_FEEDERID22','eTX_PHASE2','eTX_SUBTYPE2','eTX_RATEDKVA_A2','eTX_RATEDKVA_B2','eTX_RATEDKVA_C2','eTX_CUSTOMERCOUNT2','eTX_STRUCTUREID','eTX_PURPOSE2','eTX_GLOBALID2']

# place list of fields above into another list for loop processing below
fldsOrig = [CapBankFldsOrig,RecloserFldsOrig,SectionalizerFldsOrig,VoltRegBankFldsOrig]
fldsDest = [CapBankFldsDest,RecloserFldsDest,SectionalizerFldsDest,VoltRegBankFldsDest]
fldsDestFuse = [FuseFldsDest,FuseFldsDest2,FuseFldsDest3,FuseFldsDest4,FuseFldsDest5,FuseFldsDest6]
fldsDestLight = [LightFldsDest,LightFldsDest2,LightFldsDest3,LightFldsDest4]
fldsDestServicePoint = [ServicePointFldsDest,ServicePointFldsDest2,ServicePointFldsDest3,ServicePointFldsDest4]
fldsDestSwitch = [SwitchFldsDest,SwitchFldsDest2,SwitchFldsDest3]
fldsDestTX = [TXFldsDest,TXFldsDest2]

# SDE variables
#unitTable = r'Database Connections\grucwgisdv01_MapEDPR_OSAuth.sde\mapedpr.ARCFM_ED.Inspection\mapedpr.ARCFM_ED.MM_eDamageAssessment'
#truncTable = r'Database Connections\grucwgisdv01_MapEDPR_ArcFM.sde\mapedpr.ARCFM_ED.Inspection\mapedpr.ARCFM_ED.MM_eDamageAssessment'
#connectionRoot = r'Database Connections\grucwgisdv01_MapEDPR_OSAuth.sde\mapedpr.ARCFM_ED.Electric\mapedpr.ARCFM_ED.%s'
#workspace = r'Database Connections\grucwgisdv01_MapEDPR_OSAuth.sde'

# fGDB variables
unitTable = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\MIMS\mmPoleEquipment'
#unitTableSDE = r'Database Connections\grucwgisdv01_MapEDPR_OSAuth.sde\mapedpr.ARCFM_ED.MM_PoleEquipment'
connectionRoot = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\%s'
workspace = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb'


# feature classes
#MM_POLEEQUIPMENT_XML = "C:/arcdata/MIMSMobile/MIMS_DATASET.XML"
MM_POLEEQUIPMENT_XML = "C:/arcdata/MIMSMobile/MIMS_DATASET_20181019.xml"
origFC = ['eCapacitorBank','eRecloser','eSectionalizer','eVoltageRegulatorBank']
fuseFC = 'eFuse'
lightFC = 'eLight'
poleFC = 'eSupportStructure'
servicepointFC = 'eServicePoint'
switchFC = 'eSwitch'
transformerFC = 'eTransformerBank'

# default field values
stormName = 'NoName'
sapNetwork = 0000

def updateUnits(connection,origFlds,destFlds,whereSQL=None):
    uc = arcpy.da.UpdateCursor(unitTable,destFlds)
    with arcpy.da.SearchCursor(connection,origFlds,whereSQL) as sc:
         for scrow in sc:
             uc.updateRow(scrow)
    del uc
    del sc

def insertPoles(connection,origFlds,destFlds,whereSQL=None):
    ic = arcpy.da.InsertCursor(unitTable,destFlds)
    with arcpy.da.SearchCursor(connection,origFlds,whereSQL) as sc:
         for scrow in sc:
              ic.insertRow(scrow)
    del ic
    del sc

def getRowCount(tbl,flds,whereSQL=None):
    rows = [row for row in arcpy.da.SearchCursor(tbl,flds,whereSQL)]
    if len(rows) > 1:
        print('Found %i in %s') % (len(rows),tbl)
    return len(rows)

def updateRelatedUnits(row,destFlds,guid):
    with arcpy.da.UpdateCursor(unitTable,destFlds,where_clause="eSupportStructure_GLOBALID = " + "'" + guid + "'") as uc:
        for ucrow in uc:
            ucrow = row
            #print('updating destflds %s') % x
            uc.updateRow(ucrow)
            # break and return out of the for loop so we dont update the entire row with same cursor object
            break
        return
    del uc
        
# prep unitTable
if not arcpy.Exists(unitTable):
    arcpy.ImportXMLWorkspaceDocument_management(workspace, MM_POLEEQUIPMENT_XML, "Schema_Only")
    #print('Setting default value: %s) % (stormName)
    arcpy.AssignDefaultToField_management(unitTable,"StormName",stormName)
    #print('Setting default value: %i) % (sapNetwork)
    #arcpy.AssignDefaultToField_management(unitTable,"SAPNetwork",sapNetwork)
else:
    print 'Truncating...',unitTable
    arcpy.TruncateTable_management(unitTable)
#print 'Checking for index eSupportStructure_GLOABLID...'
#indexes = arcpy.ListIndexes(unitTable)
#indexNames = []
#for index in indexes:
#    print index.name
#    indexNames.append(index.name)
#if "IDX_poleGUID" not in indexNames:
#    print'You need to add the Index' #arcpy.AddIndex_management (truncTable, "eSupportStructure_GLOBALID", "IDX_poleGUID", "UNIQUE", "ASCENDING")



print 'Processing...you gotta wait now'
# Start Main
with arcpy.da.Editor(workspace) as edit:
    #print 'Inserting...',poleFC
    ic = arcpy.da.InsertCursor(unitTable,PoleFldsDest)
    with arcpy.da.SearchCursor(connectionRoot%(poleFC),PoleFldsOrig) as sc:
        for scrow in sc:
            ic.insertRow(scrow)
    del ic
    del sc
    print 'Updating Storm Name: ',stormName
    with arcpy.da.UpdateCursor(unitTable,'StormName') as uc:
        for row in uc:
            row[0] = stormName
            uc.updateRow(row)
    del uc
    idx = -1
    for fc in origFC:
        idx +=1
        #print 'Updating...',fc
        with arcpy.da.SearchCursor(connectionRoot%(fc),fldsOrig[idx],where_clause="eSupportStructure_GLOBALID IS NOT NULL",sql_clause=(None,"ORDER BY eSupportStructure_GLOBALID")) as sCur:
            for sCurRow in sCur:
                with arcpy.da.UpdateCursor(unitTable,fldsDest[idx],where_clause="eSupportStructure_GLOBALID = " + "'" + sCurRow[0] + "'",sql_clause=(None,"ORDER BY eSupportStructure_GLOBALID")) as uCur:
                    for uCurRow in uCur:
                        uCur.updateRow(sCurRow)
    idx = -1
    count = 0
    with arcpy.da.SearchCursor(unitTable,['eSupportStructure_GLOBALID'],sql_clause=(None,"ORDER BY eSupportStructure_GLOBALID")) as unitCur:
        for unit in unitCur:
            count +=1
            #print(count)
            with arcpy.da.SearchCursor(connectionRoot%(lightFC),LightFldsOrig,where_clause="eSupportStructure_GLOBALID = '"  + unit[0] + "'") as lghtCur:
                for lght in lghtCur:
                    #print 'Updating...',lightFC
                    idx +=1
                    updateRelatedUnits(lght,fldsDestLight[idx],lght[0])
                idx = -1
            idx = -1
            with arcpy.da.SearchCursor(connectionRoot%(fuseFC),FuseFldsOrig,where_clause="eSupportStructure_GLOBALID = '"  + unit[0] + "'") as fxCur:
                for fx in fxCur:
                    #print 'Updating...',fuseFC
                    idx +=1
                    updateRelatedUnits(fx,fldsDestFuse[idx],fx[0])
                idx = -1
            idx = -1
            with arcpy.da.SearchCursor(connectionRoot%(transformerFC),TXFldsOrig,where_clause="eSupportStructure_GLOBALID = '"  + unit[0] + "'") as xfrCur:
                for xfr in xfrCur:
                    #print 'Updating...',transformerFC
                    idx +=1
                    updateRelatedUnits(xfr,fldsDestTX[idx],xfr[0])
                idx = -1
            idx = -1
            with arcpy.da.SearchCursor(connectionRoot%(switchFC),SwitchFldsOrig,where_clause="eSupportStructure_GLOBALID = '"  + unit[0] + "' AND SUBTYPE IN (1,2,3,4)") as swtCur:
                for swt in swtCur:
                    #print 'Updating...',switchFC
                    idx +=1
                    updateRelatedUnits(swt,fldsDestSwitch[idx],swt[0])
                idx = -1
            idx = -1
            with arcpy.da.SearchCursor(connectionRoot%(servicepointFC),ServicePointFldsOrig,where_clause="eSupportStructure_GLOBALID = '"  + unit[0] + "'") as svcCur:
                for svc in svcCur:
                    #print 'Updating...',servicepointFC
                    idx +=1
                    updateRelatedUnits(svc,fldsDestServicePoint[idx],svc[0])
                idx = -1
##with arcpy.da.Editor(workspace) as edit:
##    print 'Inserting SDE MM_PoleEquipment...'
##    ic = arcpy.da.InsertCursor(unitTableSDE,"*")
##    with arcpy.da.SearchCursor(unitTable,"*") as sc:
##        for scrow in sc:
##            ic.insertRow(scrow)
##    del ic
##    del sc
result = arcpy.GetCount_management (r'C:\arcdata\MIMS_Electric_Extract.gdb\eSupportStructure')
print('fGDB Pole Count '),int(result.getOutput(0))
result = arcpy.GetCount_management (unitTable)
print('fGDB PoleEquipment Count '),int(result.getOutput(0))
#result = arcpy.GetCount_management (unitTableSDE)
#print('SDE PoleEquipment Count '),int(result.getOutput(0))

print ('finished - elapsed time: '),str((time.time() - startTime)/3600)           
