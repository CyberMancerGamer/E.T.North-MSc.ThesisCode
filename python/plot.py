import numpy as np # For arrays and math
import matplotlib.pyplot as plt # Plotting module
import matplotlib.axes as ax # Customizing tick marks on plot
from matplotlib.colors import ListedColormap, LinearSegmentedColormap # Imports colors
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

plt.rcParams.update({
  "font.family": "Arial",
  "font.size": 21, # Changes font size. 19 for normal plots. 21 for large figures
  "figure.figsize": "12.8, 9.6",  # figure size in inches. This is twice as large as normal (6.4, 4.8)
  "lines.markersize": 12, # marker size, in points. 6 standard. 9 for QCM
  "figure.constrained_layout.use": True,
  "xtick.direction": "in",
  "ytick.direction": "in",
  "xtick.top": True,
  "xtick.bottom": True,
  "xtick.minor.visible": True,
  "ytick.left": True,
  "ytick.right": True,
  "ytick.minor.visible": True,
  "xtick.major.size": 14, # major tick size in points (3.5 default)
  "xtick.minor.size": 8, # minor tick size in points (2 default)
  "ytick.major.size": 14, # major tick size in points (3.5 default)
  "ytick.minor.size": 8 # minor tick size in points (2 default)
})

#plt.rcdefaults() # Restores default rcparams
#uio_palette = ["#FFFEA7","#FEA11B", "#DC4234", "#000000"] # UiO yellow, UiO orange, PMS-485, black. Taken from: https://www.uio.no/om/designmanual/profilelementer/fargepalett/
uio_palette = ["#86A4F7", "#2EC483", "#FEA11B", "#FB6666"] # UiOs secondary colors blue->red.
uio_cmp = LinearSegmentedColormap.from_list("UiO colormap", uio_palette) # Creates a colormap from the palette
markers = ["o", "^", "v", "s", "D", "p", "*"] # Markers for plots. Circle, triangle_up, triangle_down, square, diamond, pentagon, star

def read_XRD(filename):
    """
    Reads an inputfile and returns data as tuple of x and y-data as lists.
    """
    theta = [] # Creates list to store x-data
    counts = [] # Creates list to store x-data
    with open(filename) as infile:

        if filename.split(".")[-1]=="txt":
            infile.readline()
            separator = ","
        elif filename.split(".")[-1]=="xy":
            separator = " "

        infile.readline()
        lines = infile.readlines() # Reads and stores all data

        for line in lines: # Iterates over each line
            words = line.split(separator) # Splits the line into words for each separator it finds
            theta.append(float(words[0])) # Stores the theta as a number to the list "theta"
            counts.append(float(words[1])) # Stores the counts as a number to the list "counts"

    return theta, counts

def plot_XRD(filename, title=None):
    """
    Reads an XRD file and plots it.
    """
    x, y = read_XRD(filename) # Reads file
    x = np.array(x) # Converts to array
    y = np.array(y) # Converts to array

    y = y / np.amax(y) # Divide all numbers in y by the maximum number (converts counts to relative intensity)

    plt.plot(x, y, "k") # Plots a black line

    plt.xlabel("2θ [°]") # x-axis name
    plt.ylabel("Intensity [a.u.]") # y-axis name

    if title!=None:
        plt.title(title) # Graph title

    plt.show() # Shows the figure

def read_OpticsLab(filename):
    """
    Reads an inputfile and returns data as tuple of x and y-data as lists.
    """
    wavelength = []
    counts = []
    with open(filename) as infile: # Opens the file and reads it
        for i in range(14): # Discards first 14 lines, as they are just info
            infile.readline()
        lines = infile.readlines() # Reads and stores all data

        for line in lines: # Iterates over each line
            words = line.split("\t") # Splits the line into words for each whitespace it finds
            wavelength.append(float(words[0])) # Stores the wavelength as a number to the list "wavelength"
            counts.append(float(words[1])) # Stores the counts as a number to the list "counts"

    return wavelength, counts

def plot_OpticsLab(filename, title=None, cutoff=None):
    """
    Reads a file from the Optics Lab and plots it.
    """
    x, y = read_OpticsLab(filename) # Reads file
    x = np.array(x) # Converts to array
    y = np.array(y) # Converts to array

    if "trans" or "Transmission" in filename: # If data is transmittance
        y = y / np.amax(y) * 100 # Divide all numbers in y by the maximum number (converts counts to percentage)
        plt.ylabel("Transmission [%]") # y-axis name
        plt.ylim(0,100)
    elif "reflec" in filename: # If data is reflectance
        y = y / np.amax(y) * 100 # Divide all numbers in y by the maximum number (converts counts to percentage)
        plt.ylabel("Reflectivity [%]") # y-axis name
        plt.ylim(0,100)
    elif "PL" in filename: # It data is fluorescence
        plt.ylabel("Fluorescence Intensity [a.u.]")


    if cutoff != None: # If cutoff is wanted
        for i, val in enumerate(y):
            if val > cutoff: # If the count is higher than the cutoff
                y[i] = cutoff # Set the value to 0
            if val < 0: # If negative values are found set them to zero
                y[i] = 0
    else:
        for i, val in enumerate(y):
            if val < 0: # If negative values are found set them to zero
                y[i] = 0

    if title!=None:
        plt.title(title) # Graph title

    plt.plot(x, y, "k") # Plots a black line
    plt.xlabel("Wavelength [nm]") # x-axis name
    plt.show() # Shows the figure

def read_UVVis(filename):
    """
    Reads an inputfile and returns data as tuple of x and y-data as lists.
    """
    wavelength = []
    intensity = []
    with open(filename) as infile: # Opens the file and reads it
        infile.readline() # Reads and discards the 1st line (info)
        infile.readline() # Reads and discards the 2nd line (units)
        lines = infile.readlines() # Reads and stores all data

        if "," in lines[0]: # If the separator is a comma
            for line in lines: # Iterates over each line
                line = line.replace(",", ".") # Replaces comma with period
                words = line.split() # Splits the line into words for each whitespace it finds
                if len(words)==2:
                    wavelength.append(float(words[0])) # Stores the wavelength as a number to the list "wavelength"
                    intensity.append(float(words[1])) # Stores the intensity as a number to the list "intensity"
        elif "." in lines[0]: # If the separator is a period
            for line in lines: # Iterates over each line
                words = line.split() # Splits the line into words for each whitespace it finds
                if len(words)==2:
                    wavelength.append(float(words[0])) # Stores the wavelength as a number to the list "wavelength"
                    intensity.append(float(words[1])) # Stores the intensity as a number to the list "intensity"
        else:
            print("Could not determine if separator was \",\" or \".\". Defaulting to \".\".")
            for line in lines: # Iterates over each line
                words = line.split() # Splits the line into words for each whitespace it finds
                if len(words)==2:
                    wavelength.append(float(words[0])) # Stores the wavelength as a number to the list "wavelength"
                    intensity.append(float(words[1])) # Stores the intensity as a number to the list "intensity"
    return wavelength, intensity

def plot_UVVis(filename, title=None, type="transY"):
    """
    Reads a file from the UV-Vis and plots it.
    """
    x, y = read_UVVis(filename)
    x = np.array(x)
    y = np.array(y)

    plt.plot(x, y, "k") # Plots a black line

    plt.xlabel("Wavelength [nm]") # x-axis name
    if type=="trans":
        plt.ylabel("Transmission [T\%]") # y-axis name
    elif type=="reflec":
        plt.ylabel("Reflectivity [R\%]") # y-axis name
    else:
        print("This function only takes transmission (trans) and reflectivity (reflec) measurements.")
        print("If you want to measure absorption (abs), use read_UVVIS on trans and reflec, then calculate manually.")
        return

    if title!=None:
        plt.title(title) # Graph title

    plt.ylim(0,100)
    plt.show() # Shows the figure

def read_QCM_average(filename):
    """Reads a QCM Average_no_X.txt file and stores the data as a list."""
    time = []
    Average_A = []
    StdevA1 = []
    StdevA2 = []
    Average_B = []
    StdevB1 = []
    StdevB2 = []
    with open(filename) as infile: # Opens the file and reads it
        infile.readline() # Reads and discards the 1st line (info)
        lines = infile.readlines() # Reads and stores all data
        for line in lines:
            words = line.split("\t")
            time.append(float(words[0]))
            Average_A.append(float(words[1]))
            StdevA1.append(float(words[2]))
            StdevA2.append(float(words[3]))
            Average_B.append(float(words[4]))
            StdevB1.append(float(words[5]))
            StdevB2.append(float(words[6]))
    return time, Average_A, StdevA1, StdevA2, Average_B, StdevB1, StdevB2

def read_FTIR(filename):
    """
    Reads an inputfile and returns its wavenumber and transmittance as a nested list
    File as follows:
    1 data1 data2
    2 ...
    """
    wavenumber = []
    transmittance = []
    with open(filename) as infile: # Opens the file and reads it
        lines = infile.readlines() # Reads and stores all data

        if "," in lines[0]: # If the separator is a comma
            for line in lines: # Iterates over each line
                line = line.replace(",", ".") # Replaces comma with period
                words = line.split() # Splits the line into words for each whitespace it finds
                wavenumber.append(float(words[0])) # Stores the wavenumber as a number to the list "wavenumber"
                transmittance.append(float(words[1])) # Stores the transmittance as a number to the list "transmittance"
        elif "." in lines[0]: # If the separator is a period
            for line in lines: # Iterates over each line
                words = line.split() # Splits the line into words for each whitespace it finds
                wavenumber.append(float(words[0])) # Stores the wavenumber as a number to the list "wavenumber"
                transmittance.append(float(words[1])) # Stores the transmittance as a number to the list "transmittance"
        else:
            print("Could not determine if separator was \",\" or \".\". Defaulting to \".\".")
            for line in lines: # Iterates over each line
                words = line.split() # Splits the line into words for each whitespace it finds
                wavenumber.append(float(words[0])) # Stores the wavenumber as a number to the list "wavenumber"
                transmittance.append(float(words[1])) # Stores the transmittance as a number to the list "transmittance"
    return wavenumber, transmittance

def plot_FTIR(filename, background=None, title=None):
    """
    Plots a graph based on a list/array of x- and y-values.
    """
    x, y = np.array(read_FTIR(filename))

    if background!=None:
        x_back, y_back = np.array(read_FTIR(background))
        #plt.plot(x, (y-y_back)*100, "k") # Plots a black line
        plt.plot(x, (y)*100, "k", label="Data") # Plots a black line
        plt.plot(x_back, (y_back)*100, "k", label="Background") # Plots a black line
    else:
        #y = y/np.max(y)
        plt.plot(x, y*100, "k") # Plots a black line

    if title!=None:
        plt.title(title) # Graph title

    plt.xlabel("Wavenumber [cm$\mathregular{^{-1}}$]") # x-axis name
    plt.ylabel("Reflectance [%]")
    plt.xlim(4000,500)
    #plt.ylim(bottom=70, top=100)
    plt.show() # Shows the figure

def read_CLSEM(filename):
    """
    Reads an inputfile and returns its wavelength and intensity as a nested list
    File as followed:
    1 info
    2 data
    3 ...
    """
    wavelength = []
    intensity = []
    with open(filename) as infile: # Opens the file and reads it
        infile.readline() # Reads and discards the 1st line (info)
        lines = infile.readlines() # Reads and stores all data
        for line in lines: # Iterates over each line
            words = line.split(",") # Splits the line into words for each "," it finds
            wavelength.append(float(words[0])) # Stores the wavelength as a number to the list "wavelength"
            intensity.append(float(words[1])) # Stores the intensity as a number to the list "intensity"
    return wavelength, intensity

def sum_remove_baseline(list, start, stop):
    """
    Calculates the sum of the numbers in list between start and stop and
    removes the baseline of it.
    """
    total = 0
    # baseline = min(list[start], list[stop])
    baseline = (list[start] + list[stop])/2
    for num in list[start:stop]:
        total += num

    print("old total: ", total)
    print("baseline: ", baseline)
    print("total baseline: ", baseline*(stop-start))
    total = total-baseline*(stop-start)
    print("new total: ", total)
    print("\n")
    return total

if __name__ == "__main__": #Only runs if this program is called directly
    wavelength1, transY = np.array(read_UVVis("../data/UV-Vis/ETN4029_Y2Qz3_210428_250-850_M_trans_glass_sphere.txt"))
    wavelength2, reflectY = np.array(read_UVVis("../data/UV-Vis/ETN4029_Y2Qz3_210428_250-850_M_reflect_glass_sphere.txt"))
    wavelength3, transYb = np.array(read_UVVis("../data/UV-Vis/ETN4063_Yb2Qz3_220427_250-850_M_trans_silica_sphere_142958.txt"))
    wavelength4, reflectYb = np.array(read_UVVis("../data/UV-Vis/ETN4063_Yb2Qz3_220427_250-850_M_reflec_silica_sphere_142231.txt"))
    wavelength5, transQz = np.array(read_OpticsLab("../data/Optics Lab/ETNL1_Qz_trans_1ms_1000avg_ethanol-ref_Transmission__0__12-38-53-538.txt"))
    wavelength6, transGlass = np.array(read_UVVis("../data/UV-Vis/clearGlass_210226_250-850_M_trans.txt"))
    colors = uio_cmp(np.linspace(0, 1, 3))

    wavelength5 = wavelength5[137:1557] # 250-850nm
    transQz = transQz[137:1557] # 250-850nm (The file is in % from before, just noise in UV makes it weird)

    # This is not a very scientific or accurate way of averaging data, but it will not create too many issues, is quick to implement and does what I need it to: Reduce noise
    avgtransQz = []
    avgtransQz.append(transQz[0])
    avgtransQz.append((transQz[0] + transQz[1] + transQz[3]) / 3)
    for i in range(2,len(transQz)-2):
        avgtransQz.append((transQz[i-2] + transQz[i-1] + transQz[i] + transQz[i+1] + transQz[i+2]) / 5)
    avgtransQz.append((transQz[-3] + transQz[-2] + transQz[-1]) / 3)
    avgtransQz.append(transQz[-3])
    avgtransQz = np.array(avgtransQz)

    plt.plot(wavelength6, 100-transGlass, color=colors[0], alpha=0.5, label="Glass*")
    plt.plot(wavelength1, 100-transY-reflectY, color=colors[0], label="Y$\mathregular{_2}$Qz$\mathregular{_3}$ on glass")
    plt.plot(wavelength3, 100-transYb-reflectYb, color=colors[1], label="Yb$\mathregular{_2}$Qz$\mathregular{_3}$ on silica")
    #plt.plot(wavelength5, 100-transQz, color=colors[2], label="Qz in ethanol*") # Raw data
    plt.plot(wavelength5, 100-avgtransQz, color=colors[2], label="Qz in ethanol*") # Averaged data
    plt.xlabel("Wavelength [nm]") # x-axis name
    plt.ylabel("Absorption [%]") # y-axis name
    plt.xlim(250,850)
    plt.ylim(-3,100)
    plt.legend()
    plt.show()
