
import arcpy

# fGDB variables
OH_Primary = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\Electric\ePriOHElectricLineCond'
UG_Primary = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\Electric\ePriUGElectricLineCond'
mimsFDS = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\MIMS'
backbone = r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\MIMS\mmBackbone'

arcpy.CreateFeatureclass_management(mimsFDS,'mmBackbone','POLYLINE')
arcpy.AlterAliasName(backbone,'Backbone')
arcpy.AddField_management(backbone,'FEEDERID','TEXT',field_alias='Circuit Number')
arcpy.MakeFeatureLayer_management(OH_Primary,'OHBackbone',"BACKBONEINDICATOR = 'Y'")
arcpy.MakeFeatureLayer_management(UG_Primary,'UGBackbone',"BACKBONEINDICATOR = 'Y'")
arcpy.Append_management(['OHBackbone','UGBackbone'],backbone,'NO_TEST')

arcpy.RecalculateFeatureClassExtent_management(backbone)
result = arcpy.GetCount_management(backbone)
print('Total Backbone '),int(result.getOutput(0))
print 'finished'

