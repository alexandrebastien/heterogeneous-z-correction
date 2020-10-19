from ij import IJ
from ij.gui import GenericDialog
from ij import Prefs

def main(*R):
	""" Main function
	"""
	# Show intial progress bar
	IJ.showProgress(0,50)
	IJ.showStatus("Heterogeneous Z Correction")

    # Retrieve the values R (with default values) from previous attempts
	Rstr = "[(-0.05977, 83.3, 78.73),(-0.05976, 41.65, 39.36)]"
	R = eval(Prefs.get("HetZCorr.R", Rstr))

	# Load current image and get infos
	imp = IJ.getImage()
	stk = imp.getStack()
	(sx,sy,sz) = stackSize(stk)
	cal = imp.getCalibration()

	# Get unique values
	val = getUniqueValues(stk)

	# Get R from dialog
	R = showDialogR(R,val)
	
	# Generate optical model
	correction = generateModel(stk,R,val)
	imp.setCalibration(cal)

	#Show model image
	correction.show();
	correction.setSlice(sz);
	IJ.run(correction, "Enhance Contrast", "saturated=0.35");
	IJ.run(correction, "Fire", "");

def showDialogR(R,val):
	""" Create dialog for input and save R values in settings
	"""
	gui = GenericDialog("Heterogeneous Z Correction")
	msg = "Heterogeneous Z Correction calculates an optical model\n"\
		  "based on rational fluorescence intensity attenuation\n"\
		  "over depth, in the form of (ax+b)/(x+c). Please specify\n"\
		  "(a,b,c) for each region. You should provide a z-stack with\n"\
		  "unique pixel values for each region.\n"
	gui.addMessage(msg)
	for ii in range(len(val)):
		gui.addNumericField("Region "+str(ii)+" ("+str(val[ii])+"):   a", R[ii][0], 2) 
		gui.addToSameRow();	gui.addNumericField("b", R[ii][1], 2)
		gui.addToSameRow();	gui.addNumericField("c", R[ii][2], 2)
	gui.addHelp(r"https://github.com/alexandrebastien/heterogeneous-z-correction") 
	gui.showDialog()
	if gui.wasOKed():
		R = []
		for ii in range(len(val)):
			R = R + [(gui.getNextNumber(),
	    	          gui.getNextNumber(),
	    	          gui.getNextNumber())]
		Prefs.set("HetZCorr.R", str(R))
		return R
	else:
		return

def f(OPL,R):
	"""	Restoration function calculated from optical path length (OPL)
	and from rational function parameter (R). The rational is multiplied
    along all optical path.
    """
	x = 1
	for ii in range(len(OPL)):
		x = x * (OPL[ii] + R[ii][2]) / (R[ii][0] * OPL[ii] + R[ii][1])
	return x

def stackSize(stk):
	""" Get stack size
	"""
	sx = stk.getWidth()
	sy = stk.getHeight()
	sz = stk.size()
	return sx, sy, sz

def getUniqueValues(stk):
	""" Function to get unique values from stack
	"""
	# Get stack size
	(sx,sy,sz) = stackSize(stk)

	# Get uniques values (val) in image
	val = []
	for ii in range(sz):
		ip = stk.getProcessor(ii+1)
		sp = ip.convertToShortProcessor()
		pixels = sp.getPixels()
		val = val + list(set(pixels))
		val = list(set(val))
	return val

def generateModel(stk,R,val):
	""" Generation optical model
	"""
	(sx,sy,sz) = stackSize(stk)
	# Initialize correction output and temporary OPL
	cor = IJ.createImage("Correction", "32-bit black", sx, sy, sz)
	corstk = cor.getStack()
	OPL = 0*[len(val)]
	OPL = [0 for i in range(len(val))]
	
	lastOPL = OPL
	
	for xx in range(sx):
		for yy in range(sy):
			sub = stk.getVoxels(xx, yy, 0, 1, 1, sz,[])
			for zz in range(sz):
				for ii in range(len(val)):
					if sub[zz] == val[ii]:
						if zz >= 1:
							OPL[ii] = lastOPL[ii] + 1
						else:
							OPL[ii] = 1
					else:
						if zz >= 1:
							OPL[ii] = lastOPL[ii]
						else:
							OPL[ii] = 0
					lastOPL[ii] = OPL[ii]
				vv = f(OPL,R);
				corstk.setVoxel(xx, yy, zz, vv)
		IJ.showProgress(xx,sx)

	return cor

""" ================
	Main script call
	================
"""
main()
