import arcpy
arcpy.TableToDomain_management(r'C:\arcdata\Transfer\Domains.gdb\SAPInstallType',"Code","Description",r'C:\arcdata\Transfer\MIMS_Electric_Extract.gdb',"SAPInstallType")
arcpy.TableToDomain_management(r'C:\arcdata\Transfer\Domains.gdb\SAPPremiseType',"Code","Description",r'C:\arcdata\Transfer\MIMS_Electric_Extract.gdb',"SAPPremiseType")
#arcpy.TableToDomain_management(r'C:\arcdata\Transfer\Domains.gdb\SAPInstallType',"Code","Description",r'C:\arcdata\MIMS_Electric_Extract.gdb',"SAPInstallType")
#arcpy.TableToDomain_management(r'C:\arcdata\Transfer\Domains.gdb\SAPPremiseType',"Code","Description",r'C:\arcdata\MIMS_Electric_Extract.gdb',"SAPPremiseType")
arcpy.AssignDomainToField_management(r'C:\arcdata\Transfer\MIMS_Electric_Extract.gdb\SAP_INSTALLATION',"PREMISE_TYPE","SAPInstallType")
arcpy.AssignDomainToField_management(r'C:\arcdata\Transfer\MIMS_Electric_Extract.gdb\SAP_INSTALLATION',"Install_TYPE","SAPPremiseType")
#arcpy.AssignDomainToField_management(r'C:\arcdata\MIMS_Electric_Extract.gdb\SAP_INSTALLATION',"PREMISE_TYPE","SAPInstallType")
#arcpy.AssignDomainToField_management(r'C:\arcdata\MIMS_Electric_Extract.gdb\SAP_INSTALLATION',"Install_TYPE","SAPPremiseType")
