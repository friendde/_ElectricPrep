call _DeleteGeoNet.py "C:/temp/electricNet.log"
call _ApplyDomains.py
timeout /t 30
call 1_fixTrueCurves.py 
timeout /t 30
call 2_MigrateRelationshipClass.py
timeout /t 30
call 3_AddLabelFieldNames_fgdb.py
timeout /t 30
::call 4_UpdatePoleEquipment.py
::call 4_UpdatePoleEquipment_stocknumber.py
timeout /t 30
call 5_UpdateLabelFieldNames.py
timeout /t 30
call 6_ElectricSearchTable.py
timeout /t 30
call 6a_DeviceSearchTable.py
timeout /t 30
call 7_TiePoints.py
timeout /t 30
call 8_AerialCable.py
timeout /t 30
call 9_OrangeCappedLights.py
timeout /t 30
call 10_Backbone.py
timeout /t 30
call C:\arcdata\MIMSPython\SyncCopy.py C:\arcdata\Transfer\MIMS_Electric_Extract.gdb C:\arcdata\MIMS_Electric_Extract.gdb NEWER