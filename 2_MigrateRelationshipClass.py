# Name: MigrateRelationshipClass.py
# Description: Migrate an ObjectID-based relationship class to a GlobalID-based
#       relationship class. This script lists the ObjectID-based relationships classes
#       in a workspace, checks for GlobalIDs in the origin, then runs the tool

# Import system modules
import arcpy

# Set local variables
#workspace = r'Database Connections\grucwgisdv01_MapED_ArcFM.sde\Electric'
#workspace = r'c:\arcdata\ed_extract.gdb'
#workspace = r'C:\arcdata\MIMS_Electric_Extract.gdb'
workspaces = [r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb',r'C:\arcdata\transfer\MIMS_Electric_Extract.gdb\Electric']
passTable = ['mapedpr.SDE.Cu_Gas','mapedpr.SDE.Cu_Electric','mapedpr.SDE.CuAttributeRelationship','mapedpr.SDE.CuExtendedDataRelationship']
rc_poles = ['mapedpr.ARCFM_ED.eSuppStructure_VoltRegBank','mapedpr.ARCFM_ED.eSuppStructure_Switch','mapedpr.ARCFM_ED.eSuppStructure_Light','mapedpr.ARCFM_ED.eSuppStructure_TransformerBank','mapedpr.ARCFM_ED.eSuppStructure_Recloser','mapedpr.ARCFM_ED.eSuppStructure_CapacitorBank','mapedpr.ARCFM_ED.eSuppStructure_ServicePoint','mapedpr.ARCFM_ED.eSurfaceStructure_Switch','mapedpr.ARCFM_ED.eSuppStructure_Sectionalizer','mapedpr.ARCFM_ED.eSuppStructure_Fuse']

for workspace in workspaces:
    # List all of the relationship classes within the given workspace
    #rc_list = [c.name for c in arcpy.Describe(workspace).children if c.datatype == "RelationshipClass"]
    print("Checking workspace {0}".format(workspace))
    rc_list = [c.name for c in arcpy.Describe(workspace).children if c.datatype == "RelationshipClass" and c.name not in passTable]

    # Build a list of relationship classes which have an OBJECTID based origin class key
    rc_migrate = []
    for rc in rc_list:
        rc_path = workspace + "\\" + rc
        rc_desc = arcpy.Describe(rc_path)
        print rc_desc.name
        for item in rc_desc.OriginClassKeys:
            if "OBJECTID" in item:
                rc_migrate.append(rc_path)

    # Check that the origin feature classes have Global Ids
    rc_final = []
    for rel in rc_migrate:
        originfc = workspace + "\\" + arcpy.Describe(rel).originClassNames[0]
        if arcpy.ListFields(originfc,"","GlobalID"):
            rc_final.append(rel)
            print("Adding {0} to the migrate list.\n".format(rel.rsplit("\\",1)[1]))
        else:
            print("{0} must have Global Ids to migrate relationship class.\n".format(originfc.rsplit("\\",1)[1]))
            arcpy.AddGlobalIDs_management(originfc)
            rc_final.append(rel)

    # Pass the list of valid relationship classes into the Migrate Relationship tool
    print("Passing valid relationship classes into the Migrate Relationship Class tool.\n")
    for rel_class in rc_final:
        print("Migrating {0}... \n".format(rel_class.rsplit("\\",1)[1]))
        arcpy.MigrateRelationshipClass_management(rel_class)
        print(arcpy.GetMessages() + "\n")
