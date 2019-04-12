import arcpy, pythonaddins
import os, os.path, threading, functools

# A decorator that will run its wrapped function in a new thread
def run_in_other_thread(function):
	# functool.wraps will copy over the docstring and some other metadata
	# from the original function
	@functools.wraps(function)
	def fn_(*args, **kwargs):
		thread = threading.Thread(target=function, args=args, kwargs=kwargs)
		thread.start()
		thread.join()
	return fn_
	
startfile = run_in_other_thread(os.startfile)



class earthButton(object):
	"""Implementation for googleJump.earth (Button)"""
	def __init__(self):
		self.enabled = True
		self.checked = False
	def onClick(self):
		#save the mxd in some kind of scratch space
		mxd = arcpy.mapping.MapDocument("CURRENT")
		
		exportMXDPath = r"C:\scratch\kmlConverter.mxd"
		kmlPath = r"C:\scratch\currentLayers.kmz"
		
		#if these files exist then delete them
		if os.path.isfile(exportMXDPath):
			os.remove(exportMXDPath)
		if os.path.isfile(kmlPath):
			os.remove(kmlPath)
		
		mxd.saveACopy(exportMXDPath)
		
		del mxd #delete the current mxd object to prevent schma locks
		
		mxdCopy = arcpy.mapping.MapDocument(exportMXDPath)
		
		#get the extent of the current map
		df = arcpy.mapping.ListDataFrames(mxdCopy)[0]
		print "the name of the dataframe is: " + df.name
		print "the export path is: " + exportMXDPath
		
		clippingExtent = df.extent
		
		#run the map to kml tool with the current extent as the extent parameter
		#MapToKML_conversion (in_map_document, data_frame, out_kmz_file, {map_output_scale}, {is_composite}, {is_vector_to_raster}, {extent_to_export}, {image_size}, {dpi_of_client}, {ignore_zvalue})
		#arcpy.MapToKML_conversion(exportMXDPath, df.name, kmlPath, extent_to_export=clippingExtent)
		arcpy.MapToKML_conversion(exportMXDPath, df.name, kmlPath, extent_to_export=clippingExtent)
		
		print "deleting lose end objects"
		
		#delete the copy mxd object to prevent crashing issues
		del mxdCopy
		del df
		del clippingExtent
		
		print "starting to open kmz file"
		
		#open the kml file and end the script
		startfile(kmlPath)
		
		#can help with the error
		#http://www.fhhyc.com/code-to-open-web-browser-crashes-arcmap-when-run-from-a-python-add-in/