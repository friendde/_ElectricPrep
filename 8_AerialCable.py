import arcpy

# fGDB variables
wksp = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb'
#fds = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\MIMS'
fds = wksp + '\MIMS'
#sourceFC = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\Electric\ePriOHElectricLineCond'
sourceFC = wksp + '\Electric\ePriOHElectricLineCond'
#destFC = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\MIMS\AerialCable'
destFC = wksp + '\MIMS\AerialCable'
removeFields = ['SHAPE','SHAPE_Length']

sr = arcpy.SpatialReference(2238)

whereSQL = "(CONDUCTORDESCRIPTION = '1/0 AER XLP' or CONDUCTORDESCRIPTION = '1000 AER XLP' or CONDUCTORDESCRIPTION = '2 AER XLP' or CONDUCTORDESCRIPTION = '397 AER XLP' or CONDUCTORDESCRIPTION = '4/0 AER XLP') AND (TEMPORARYFLAG <> 'H')"

def getRowCount(tbl,flds,whereSQL=None):
    rows = [row for row in arcpy.da.SearchCursor(tbl,flds,whereSQL)]
    if len(rows) > 1:
        print('Aerial Cable count: %i in %s') % (len(rows),tbl)
    return len(rows)

flds = [fld.name for fld in arcpy.ListFields(sourceFC)]
for fld in removeFields:
    flds.remove(fld)
flds.append('SHAPE@')

if not arcpy.Exists(destFC):
    print 'Creating:',destFC
    arcpy.CreateFeatureclass_management(fds,"AerialCable","POLYLINE",sourceFC,"SAME_AS_TEMPLATE","SAME_AS_TEMPLATE",sr)
    arcpy.AlterAliasName(destFC, 'Aerial Cable')
else:
    print ('{0} exists, truncating table').format(destFC)
    arcpy.TruncateTable_management(destFC)

with arcpy.da.Editor(wksp) as edit:
    ic = arcpy.da.InsertCursor(destFC,flds)
    print 'Inserting Aerial Cable...'
    with arcpy.da.SearchCursor(sourceFC,flds,whereSQL) as sc:
        for row in sc:
            ic.insertRow(row)

arcpy.RecalculateFeatureClassExtent_management(destFC)
getRowCount(destFC,["*"],whereSQL)
getRowCount(sourceFC,["*"],whereSQL)
#result = arcpy.GetCount_management(searchTable)
#print('ElectricSearch '),int(result.getOutput(0))
print 'finished'

# list comprehension
# rows = [row for row in arcpy.da.SearchCursor(r'Database Connections\MapEDPR_ArcFM.sde\mapedpr.ARCFM_ED.eFOREIGNATTACHMENT','ATTACHMENTZONE',where_clause="ATTACHMENTZONE = 'SUPPLY'")]
# len(rows)
