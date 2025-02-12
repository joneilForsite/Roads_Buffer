import arcpy

# Set workspace
arcpy.env.workspace = r"C:\GIS\Projects\RoadBuffer.gdb"
input_roads = "Roads"  # Input roads feature class

# Create output feature class for merged buffers
output_buffer_fc = "Roads_Buffered"
if not arcpy.Exists(output_buffer_fc):
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, output_buffer_fc, "POLYGON", input_roads)

# Get unique road class and type combinations
road_classes = set()
with arcpy.da.SearchCursor(input_roads, ["ROAD_CLASS", "ROAD_TYPE"]) as cursor:
    for row in cursor:
        road_classes.add(row)

# Loop through each road class and type
for road_class, road_type in road_classes:
    query = f"ROAD_CLASS = '{road_class}' AND ROAD_TYPE = '{road_type}'"
    arcpy.AddMessage(f"Processing: {road_class} - {road_type}")

    # Select roads by class and type
    selected_roads = arcpy.management.SelectLayerByAttribute(input_roads, "NEW_SELECTION", query)

    # Apply buffer using the BUFFER field
    temp_buffer = f"Buffer_{road_class}_{road_type}"
    arcpy.analysis.Buffer(selected_roads, temp_buffer, "BUFFER", "FULL", "ROUND", "ALL")

    # Append to final buffered roads dataset
    arcpy.management.Append(temp_buffer, output_buffer_fc, "NO_TEST")

    # Cleanup temp layers
    arcpy.management.Delete(temp_buffer)

print("Buffer process completed!")
