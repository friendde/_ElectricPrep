import arcpy

# # place list of fields above into another list for loop processing below
# fldsOrig = [CapBankFldsOrig,RecloserFldsOrig,SectionalizerFldsOrig,VoltRegBankFldsOrig]
# fldsDest = [CapBankFldsDest,RecloserFldsDest,SectionalizerFldsDest,VoltRegBankFldsDest]
# fldsDestFuse = [FuseFldsDest,FuseFldsDest2,FuseFldsDest3,FuseFldsDest4,FuseFldsDest5,FuseFldsDest6]
# fldsDestLight = [LightFldsDest,LightFldsDest2,LightFldsDest3,LightFldsDest4]
# fldsDestServicePoint = [ServicePointFldsDest,ServicePointFldsDest2,ServicePointFldsDest3,ServicePointFldsDest4]
# fldsDestSwitch = [SwitchFldsDest,SwitchFldsDest2,SwitchFldsDest3]
# fldsDestTX = [TXFldsDest,TXFldsDest2]


# fGDB variables
searchTable = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\MIMS\mmDeviceSearch'
connectionRoot = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\Electric\%s'
workspace = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb'


# feature classes and fields
#MM_ELECTRICSEARCH_XML = "C:/arcdata/MIMSMobile/MIMS_DATASET.XML"
MM_DEVICESEARCH_XML = "C:/arcdata/MIMSMobile/MIMS_DATASET_20181019.xml"
fcFeederIDs = ['eCabinetStructure','eSurfaceStructure']
fldsFeederIDs = ['FACILITYID','STREETADDRESS','FEEDERIDS','SHAPE@']
#fcFacilityID = ['eLight']
#fldsFacilityID = ['FACILITYID','STREETADDRESS','SHAPE@']
fcFeederID = ['eCapacitorBank','eFuse','eRecloser','eSectionalizer','eSwitch','eTransformerBank','eVoltageRegulatorBank']
fldsFeederID = ['DEVICEID','STREETADDRESS','FEEDERID','FEEDERID2','SHAPE@']
elecFldsDest = ['FACILITYID','FACILITYTYPE','NEARADDRESS','FEEDERIDS','TIEPOINT','DisplayLabel','SHAPE@']

def getRowCount(tbl,flds,whereSQL=None):
    rows = [row for row in arcpy.da.SearchCursor(tbl,flds,whereSQL)]
    if len(rows) > 1:
        print('Found %i in %s') % (len(rows),tbl)
    return len(rows)

def changeAliasName(fcName):
    if fcName == 'eCabinetStructure':
        aliasName = 'Cabinet'
        return aliasName
    if fcName == 'eLight':
        aliasName = 'Light'
        return aliasName
    if fcName == 'eSupportStructure':
        aliasName = 'Pole'
        return aliasName
    if fcName == 'eSurfaceStructure':
        aliasName = 'Pad'
        return aliasName
    if fcName == 'eCapacitorBank':
        aliasName = 'Capacitor'
        return aliasName
    if fcName == 'eFuse':
        aliasName = 'Fuse'
        return aliasName
    if fcName == 'eRecloser':
        aliasName = 'Recloser'
        return aliasName
    if fcName == 'eSectionalizer':
        aliasName = 'Sectionalizer'
        return aliasName
    if fcName == 'eSwitch':
        aliasName = 'Switch'
        return aliasName
    if fcName == 'eTransformerBank':
        aliasName = 'Transformer'
        return aliasName
    if fcName == 'eVoltageRegulatorBank':
        aliasName = 'Regulator'
        return aliasName

def checkValue(val):
    #print val
    if val is None:
        return ''
    elif val == '':
        return ''
    else:
        return val

def checkCkt(ckt):
    #print val
    if ckt is None:
        return ''
    elif ckt == '':
        return ''
    else:
        return ckt + ','

def isTiePoint(ckts):
    if len(ckts.split(',')) > 2:
        tiePnt = 'Y'
        return tiePnt

if arcpy.Exists(searchTable):
     print 'Truncating...',searchTable
     arcpy.TruncateTable_management(searchTable)
else:
     arcpy.ImportXMLWorkspaceDocument_management(workspace, MM_DEVICESEARCH_XML, "Schema_Only")

# Start Main
with arcpy.da.Editor(workspace) as edit:
    # for fc in fcFacilityID:
        # ic = arcpy.da.InsertCursor(searchTable,elecFldsDest)
        # print 'Inserting...',changeAliasName(fc)
        # with arcpy.da.SearchCursor(connectionRoot%(fc),fldsFacilityID) as sc:
            # for scrow in sc:
                # row = ((checkValue(scrow[0]),changeAliasName(fc),checkValue(scrow[1]),None,None,scrow[2]))
                # ic.insertRow(row)
        # del sc
        # del ic
    for fc in fcFeederID:
        ic = arcpy.da.InsertCursor(searchTable,elecFldsDest)
        print 'Inserting...',changeAliasName(fc)
        with arcpy.da.SearchCursor(connectionRoot%(fc),fldsFeederID) as sc:
            for scrow in sc:
                feeders = checkCkt(scrow[2]) + checkCkt(scrow[3])
                tiepoint = None
                tiePoint = isTiePoint(feeders)
                #print tiePoint
                row = ((checkValue(scrow[0]),changeAliasName(fc),checkValue(scrow[1]),feeders,tiePoint,changeAliasName(fc)+'-'+checkValue(scrow[0]),scrow[4]))
                ic.insertRow(row)
        del sc
        del ic
    for fc in fcFeederIDs:
        ic = arcpy.da.InsertCursor(searchTable,elecFldsDest)
        print 'Inserting...',changeAliasName(fc)
        with arcpy.da.SearchCursor(connectionRoot%(fc),fldsFeederIDs) as sc:
            for scrow in sc:
                row = ((checkValue(scrow[0]),changeAliasName(fc),checkValue(scrow[1]),scrow[2],None,changeAliasName(fc)+'-'+checkValue(scrow[0]),scrow[3]))
                ic.insertRow(row)
        del sc
        del ic

arcpy.RecalculateFeatureClassExtent_management(searchTable)
result = arcpy.GetCount_management(searchTable)
print('DeviceSearch '),int(result.getOutput(0))
print 'finished'
               
