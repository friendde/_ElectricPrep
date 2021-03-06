import arcpy

geoNet = r'C:\arcdata\Transfer\MIMS_Electric_Extract.gdb\Electric\Electric_Net'
geoNetLog = "C:/GISData/Utilities/Logs/electricNet" + str(datetime.datetime.now().strftime("%Y%m%d%M%H%S")) + ".log"
#geoNetLog = "C:/GISData/Utilities/Logs/electricNet.log"
#geoNetLog = sys.argv[1]
print ("Rebuilding and deleting Electric Net")
arcpy.RebuildGeometricNetwork_management(geoNet,geoNetLog)
arcpy.Delete_management(geoNet)