
import arcpy

# fGDB variables
mimsTiePoints = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\MIMS\mmTiePoints'
mimsFDS = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\MIMS\%s'
electricFDS = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\Electric\%s'
workspace = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb'

# feature classes and fields
#MM_TIEPOINTS_XML = "C:/arcdata/MIMSMobile/MIMS_DATASET.XML"
MM_TIEPOINTS_XML = "C:/arcdata/MIMSMobile/MIMS_DATASET_20181019.xml"
fcTiePoints = ['eFuse','eSwitch']
origFldsTiePoint = ['SHAPE@','DEVICEID','FEEDERID','FEEDERID2','STREETADDRESS','GLOBALID','STRUCTUREID','FACILITYID','StockNumber','StandardLabel','DisplayLabel']
destFldsTiePoint = ['SHAPE@','DEVICEID','FEEDERID','FEEDERID2','STREETADDRESS','GLOBALID','STRUCTUREID','FACILITYID','StockNumber','StandardLabel','DisplayLabel','FacilityType']

def getRowCount(tbl,flds,whereSQL=None):
    rows = [row for row in arcpy.da.SearchCursor(tbl,flds,whereSQL)]
    if len(rows) > 1:
        print('Found %i in %s') % (len(rows),tbl)
    return len(rows)

def changeAliasName(fcName):
    if fcName == 'eCabinetStructure':
        aliasName = 'UG Device'
        return aliasName
    if fcName == 'eLight':
        aliasName = 'Light'
        return aliasName
    if fcName == 'eSupportStructure':
        aliasName = 'Pole'
        return aliasName
    if fcName == 'eSurfaceStructure':
        aliasName = 'UG Device'
        return aliasName
    if fcName == 'eCapacitorBank':
        aliasName = 'Capacitor Bank'
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
        aliasName = 'Voltage Regulator Bank'
        return aliasName

def checkValue(val):
    #print val
    if val is None:
        return ''
    elif val == '':
        return ''
    else:
        return val

if arcpy.Exists(mimsTiePoints):
    result = arcpy.GetCount_management(mimsTiePoints)
    if (int(result.getOutput(0))) > 0:
        print 'Truncating...',mimsTiePoints
        arcpy.TruncateTable_management(mimsTiePoints)
else:
     arcpy.ImportXMLWorkspaceDocument_management(workspace, MM_TIEPOINTS_XML, "Schema_Only")


# Start Main
with arcpy.da.Editor(workspace) as edit:
    ic = arcpy.da.InsertCursor(mimsTiePoints,destFldsTiePoint)
    for fc in fcTiePoints:
        print 'Inserting...',changeAliasName(fc)
        with arcpy.da.SearchCursor(electricFDS%(fc),origFldsTiePoint,where_clause="FEEDERID IS NOT NULL AND FEEDERID2 IS NOT NULL") as sc:
            for scrow in sc:
                row = (scrow[0],(checkValue(scrow[1])),(checkValue(scrow[2])),(checkValue(scrow[3])),(checkValue(scrow[4])),scrow[5],checkValue(scrow[6]),(checkValue(scrow[7])),(checkValue(scrow[8])),(scrow[2] + '//' + scrow[3]),(checkValue(scrow[9])+'-'+(scrow[2] + '-' + scrow[3])),changeAliasName(fc))
		#row = (scrow[0],(checkValue(scrow[1])),(checkValue(scrow[2])),(checkValue(scrow[3])),(checkValue(scrow[4])),scrow[5],checkValue(scrow[6]),(checkValue(scrow[7])),(checkValue(scrow[8])),(checkValue(scrow[9])),(checkValue(scrow[9])),changeAliasName(fc))
                ic.insertRow(row)
    del ic
arcpy.RecalculateFeatureClassExtent_management(mimsTiePoints)
result = arcpy.GetCount_management(mimsTiePoints)
print('Total Tie Points '),int(result.getOutput(0))
print 'finished'

# list comprehension
# rows = [row for row in arcpy.da.SearchCursor(someFC,someFields,someQuery)] 
# print len(rows)
#rows = [row for row in arcpy.da.SearchCursor(electricFDS%(fc),fldsTiePoint,where_clause="FEEDERID IS NOT NULL AND FEEDERID2 IS NOT NULL")]
#print(str(len(rows)) + changeAliasName(fc) + 'Tie Points')
