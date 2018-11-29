import arcpy

# fGDB variables
lights = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\Electric\eLight'
ocLights = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\MIMS\MM_OrangeCappedLights'
workspace = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb'
lightFlds = ['SUBTYPE', 'LAMP', 'MOUNTHEIGHT', 'COLOR', 'ARMLENGTH', 'ARMDIRECTION', 'OWNER', 'BILLINGGROUP', 'INSTALLATIONDATE', 'SUPPORTSTRUCTUREOBJECTID', 'SYMBOLROTATION', 'STATUS','INSTALL_NUM', 'UNIT_TYPE', 'AGREEMENT', 'STREETADDRESS', 'GRUGISID', 'GLOBALID', 'STRUCTUREID', 'FACILITYID', 'StockNumber', 'StockNumber_Arm', 'eSupportStructure_GLOBALID', 'StandardLabel', 'DisplayLabel', 'SHAPE@']

def getRowCount(tbl,flds,whereSQL=None):
    rows = [row for row in arcpy.da.SearchCursor(tbl,flds,whereSQL)]
    if len(rows) > 1:
        print('Found %i in %s') % (len(rows),tbl)
    return len(rows)

if arcpy.Exists(ocLights):
     print 'Truncating...',ocLights
     arcpy.TruncateTable_management(ocLights)

# Start Main
with arcpy.da.Editor(workspace) as edit:
    ic = arcpy.da.InsertCursor(ocLights,lightFlds)
    with arcpy.da.SearchCursor(lights,lightFlds,where_clause="STATUS='OC'") as sc:
        for scrow in sc:
            ic.insertRow(scrow)
        
arcpy.RecalculateFeatureClassExtent_management(ocLights)
result = arcpy.GetCount_management(ocLights)
print('Orange Cappped Lights '),int(result.getOutput(0))
print 'finished'
               
