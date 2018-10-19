#todo add Try Except and error trapping
#todo add arcpy messages
import arcpy, sys

# scratchWksp = arcpy.env.scratchWorkspace
scratchWksp = 'C:\\Users\\friendde\\Documents\\ArcGIS\\Default.gdb'
arcpy.env.workspace = scratchWksp
arcpy.env.overwriteOutput = True
curvyFC = []
passFlds = ['OBJECTID','GLOBALID','GlobalID','SHAPE','Shape','SHAPE.STLength()','Shape.STLength()','SHAPE_Length','SHAPE.STArea()']
whereCurvyOID = ''
curveList = []
#mxd = arcpy.mapping.MapDocument("CURRENT")
mxd = arcpy.mapping.MapDocument("C:/arcdata/MIMSMobile/mxElectricPrep.mxd")
fGDB = "C:/arcdata/transfer/MIMS_Electric_Extract.gdb"


fixTrueCurves = True

def getCurvy(lyrName,appendOIDList,firstOID):
     global whereCurvyOID
     whereCurvyOID = ''
     global curveList
     curveList = []
     with arcpy.da.SearchCursor(lyrName,["SHAPE@JSON","OID@"]) as cur:
          for row in cur:
               if 'curvePaths' in row[0]:
                    curveList.append(row[1])
                    if appendOIDList:
                         #print("Processing true curves in {0}...".format(lyrName))
                         ic = arcpy.da.InsertCursor("CurveOIDS",["FCName","OIDList"])
                         ic.insertRow((lyrName,row[1]))
                         whereCurvyOID = 'OBJECTID IN ' + str(tuple(curveList))
     if len(curveList) > 0:
          return whereCurvyOID,curveList
     else:
          return False

def getShapeType(mxdLayer):
     featureType = arcpy.Describe(mxdLayer).shapeType
     return featureType

def fixCurves(fc):
     arcpy.env.overwriteOutput = True
     print("\tProcessing true curves in {0}... this will take awhile to complete").format(fc.name)
     whereOID,cntSource = getCurvy(fc.dataSource,True,False)
     if len(cntSource) == 1:
          whereOID = whereOID.replace(',','')
     #arcpy.SelectLayerByAttribute_management(fc,"NEW_SELECTION",whereOID)
     #arcpy.CopyFeatures_management(fc,"curvy_" + fc.name.replace(" ","_"))
     arcpy.Select_analysis(fc.dataSource,"curvy_" + fc.name.replace(" ","_"),whereOID)
     expression,cntCopy = getCurvy(scratchWksp + "\curvy_" + fc.name.replace(" ","_"),False,False)
     arcpy.Densify_edit(scratchWksp + "\curvy_" + fc.name.replace(" ","_"), "ANGLE", "200 Feet", "2 Feet", "10")
     arcpy.FeatureVerticesToPoints_management(scratchWksp + "\curvy_" + fc.name.replace(" ","_"), scratchWksp + "\curvy_" + fc.name.replace(" ","_") + "_Pnts", "ALL")
     arcpy.PointsToLine_management(scratchWksp + "\curvy_" + fc.name.replace(" ","_") + "_Pnts", scratchWksp + "\\notCurvy_" + fc.name.replace(" ","_"),"ORIG_FID")
     if getCurvy(scratchWksp + "\\notCurvy_" + fc.name.replace(" ","_"),False,False):
          print("Something went horribly wrong! {0}").format(fc.name)
     flds = arcpy.ListFields(fc.dataSource)
     # use python list comprehension, removing list objects in a loop will return an error
     fldsList = [fld for fld in flds if fld.name not in passFlds]
     # a feature class may have only passFlds and script fails
     if fldsList:
          fldNames = []
          cnt = 1
          for f in fldsList:
               if cnt < len(fldsList):
                    fldNames.append(f.name)
               elif cnt == len(fldsList):
                    fldNames.append(f.name)
               cnt = cnt + 1
          fldNames = ';'.join(map(str, fldNames))
          if getShapeType(fc) == "Polyline":
               arcpy.TransferAttributes_edit(scratchWksp + "\curvy_" + fc.name.replace(" ","_"), scratchWksp + "\\notCurvy_" + fc.name.replace(" ","_"), fldNames, "1 Feet", "", "attTransfer" + fc.name.replace(" ","_"))
               if fixTrueCurves:
                    # delete coincident lines first due to ArcFM Feeder Mananger messages
                    # append after delete or ArcFM Feeder Manager will present excessive messages
                    arcpy.SelectLayerByAttribute_management(fc,"NEW_SELECTION",whereOID)
                    arcpy.DeleteFeatures_management(fc)
                    arcpy.Append_management(scratchWksp + "\\notCurvy_" + fc.name.replace(" ","_"),fc.dataSource,"NO_TEST")
                    #pass
               else:
                    pass
     print("{0}: {1} Copied: {2} notCurvy: {3}".format(fc.name,len(cntSource),len(cntCopy),len(curveList)))


if arcpy.Exists("CurveOIDS"):
    arcpy.TruncateTable_management("CurveOIDS")
else:
    arcpy.CreateTable_management(scratchWksp,"CurveOIDS")
    arcpy.AddField_management("CurveOIDS","FCName","TEXT")
    arcpy.AddField_management("CurveOIDS","OIDList","DOUBLE")

for df in arcpy.mapping.ListDataFrames(mxd):
     for lyr in arcpy.mapping.ListLayers(mxd,"curvy*",df):
          arcpy.mapping.RemoveLayer(df,lyr)
     for lyr in arcpy.mapping.ListLayers(mxd,"notCurvy*",df):
          arcpy.mapping.RemoveLayer(df,lyr)

for lyr in arcpy.mapping.ListLayers(mxd):
     print("Checking {0} in {1}...").format(lyr,lyr.datasetName)
     arcpy.AddMessage("Checking {0}...".format(lyr))
     if lyr.supports("DATASOURCE"):
          if getShapeType(lyr) in ["Polyline","Polygon"]:
               if arcpy.Describe(lyr).FIDSet:
                    arcpy.SelectLayerByAttribute_management(lyr,"CLEAR_SELECTION")
               if getCurvy(lyr.dataSource,False,True):
                    print("\t{0} has true curves").format(lyr.name)
                    curvyFC.append(lyr)
                    fixCurves(lyr)
               else:
                    print("\t{0} did not have true curves").format(lyr.name)
                    pass
exit


##
##for df in arcpy.mapping.ListDataFrames(mxd):
##    for lyr in arcpy.mapping.ListLayers(mxd,"*",df):
##        if lyr.isGroupLayer:
##             print("Group Layers are not supported in RTC: {0}").format(lyr.name)
##             refLyr = lyr
##             arcpy.mapping.MoveLayer(df,refLyr,lyr,"BEFORE")

##for fc in curvyFC:
##     print("Processing true curves {0}... \nthis will take awhile to complete").format(curvyFC)
##     whereOID,cntSource = getCurvy(fc,True,False)
##     if len(cntSource) == 1:
##          whereOID = whereOID.replace(',','')
##     arcpy.SelectLayerByAttribute_management(fc,"NEW_SELECTION",whereOID)
##     arcpy.CopyFeatures_management(fc,"curvy_" + fc.name.replace(" ","_"))
##     expression,cntCopy = getCurvy("curvy_" + fc.name.replace(" ","_"),False,False)
##     arcpy.Densify_edit("curvy_" + fc.name.replace(" ","_"), "ANGLE", "200 Feet", "2 Feet", "10")
##     arcpy.FeatureVerticesToPoints_management("curvy_" + fc.name.replace(" ","_"), "curvy_" + fc.name.replace(" ","_") + "_Pnts", "ALL")
##     arcpy.PointsToLine_management("curvy_" + fc.name.replace(" ","_") + "_Pnts","notCurvy_" + fc.name.replace(" ","_"),"ORIG_FID")
##     if getCurvy("notCurvy_" + fc.name.replace(" ","_"),False,False):
##          print("Something went horribly wrong! {0}").format(fc.name)
##     flds = arcpy.ListFields(fc)
##     # use python list comprehension, removing list objects in a loop will return an error
##     fldsList = [fld for fld in flds if fld.name not in passFlds]
##     # a feature class may have only passFlds and script fails
##     if fldsList:
##          fldNames = []
##          cnt = 1
##          for f in fldsList:
##               if cnt < len(fldsList):
##                    fldNames.append(f.name)
##               elif cnt == len(fldsList):
##                    fldNames.append(f.name)
##               cnt = cnt + 1
##          fldNames = ';'.join(map(str, fldNames))
##          if getShapeType(fc) == "Polyline":
##               arcpy.TransferAttributes_edit("curvy_" + fc.name.replace(" ","_"), "notCurvy_" + fc.name.replace(" ","_"), fldNames, "1 Feet", "", "attTransfer" + fc.name.replace(" ","_"))
##               if fixTrueCurves:
##                    # delete coincident lines first due to ArcFM Feeder Mananger messages
##                    # append after delete or ArcFM Feeder Manager will present excessive messages
##                    #arcpy.SelectLayerByAttribute_management(fc,"NEW_SELECTION",whereOID)
##                    #arcpy.DeleteFeatures_management(fc)
##                    #arcpy.Append_management("notCurvy_" + fc.name.replace(" ","_"),fc.name,"NO_TEST")
##                    pass
##               else:
##                    pass
##     print("{0}: {1} Copied: {2} notCurvy: {3}".format(fc.name,len(cntSource),len(cntCopy),len(curveList)))
##print("Script finished")
