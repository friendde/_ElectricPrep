import arcpy,os,sys,traceback

# *** Start editing your parameters here ***

# field name to add to feature classes
standardLabel = 'StandardLabel'
displayLabel = 'DisplayLabel'
fieldSize = 100

# set database connections
wksp = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb'
dsNames = ['Electric']

# exclude geomteric networks
#geoNet = ['mapedpr.ARCFM_ED.Electric_Net','mapedpr.ARCFM_ED.Gas_Net','mapcompr.ARCFM_GC.FiberDataset_Net','mapwwpr.ARCFM_WWW.Reclaimed_Net','mapwwpr.ARCFM_WWW.Sewer_Net','mapwwpr.ARCFM_WWW.Water_Net']
geoNet = ['Electric_Net','Gas_Net','FiberDataset_Net','Reclaimed_Net','Sewer_Net','Water_Net']

# End editing your parameters here

# *** Do Not Edit Below This Line ***

print 'Starting ' + sys.argv[0]
logFile = ('{0}.log').format(sys.argv[0].split('.')[0])
if logFile == '.log':
    logFile = 'c:\\temp\\AddLabelstandardLabels_fgdb.log'
print logFile

def listFCInGDB(gdb, fdsName,datasetType='',fcsName='',featureType=''):
#  list Feature Classes in GDB with Feature Class ID
    arcpy.env.workspace = gdb
    print 'listFCInGDB ', arcpy.env.workspace
    fcs = {}
    # to list feature datsets read http://pro.arcgis.com/en/pro-app/arcpy/functions/listdatasets.htm
    for ds in arcpy.ListDatasets(fdsName,datasetType) + ['']:
    # to list feature classes http://pro.arcgis.com/en/pro-app/arcpy/functions/listfeatureclasses.htm
        for fc in arcpy.ListFeatureClasses(fcsName,featureType,ds):
            fcs[os.path.join(ds, fc)] = arcpy.Describe(fc).DSID;
    return fcs


try:
    # the workspace 
    arcpy.env.workspace = wksp
    for dsName in dsNames:
        fcList = listFCInGDB(wksp,dsName,'','','')
        #log = open(logFile,'w')
        # More than one way to order results, read comments below regarding order of k and v
        # Order by Feature Dataset Name \ Feature Class Name \ Feature Class ID
        #fcListSort = [(k,v) for k,v in fcList.iteritems()]
        # Order by Feature Class ID \ Feature Dataset Name \ Feature Class Name
        fcListSort = [(v,k) for k,v in fcList.iteritems()]
        # Sort A to Z, or reverse = True for Z to A
        fcListSort.sort(reverse=False)
        for k,v in fcListSort:
            if len(arcpy.ListFields(v,"StandardLabel"))==0:
                print "%s \t adding %s to %s" % (k,standardLabel,v)
                arcpy.AddField_management(v,standardLabel,'TEXT','','',fieldSize,'','NULLABLE','NON_REQUIRED','')
            if len(arcpy.ListFields(v,"DisplayLabel"))==0:
                print "%s \t adding %s to %s" % (k,displayLabel,v)
                arcpy.AddField_management(v,displayLabel,'TEXT','','',fieldSize,'','NULLABLE','NON_REQUIRED','')
            #log.write('Added %s to FeatureClassID: %s \t FeatureClassName: %s' % (standardLabel,k,v) + '\n')
            
except Exception as err:  
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    arcpymsg = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print pymsg
    print arcpymsg
    #log.write(pymsg)
    #log.write(arcpymsg)
finally:
    #log.write("Script completed")
    # Allow the database to begin accepting connections again
    print("Script completed")
    #log.close()
    # Open log file in Notepad
    #os.system('start notepad.exe ' + logFile)
    #exit()
