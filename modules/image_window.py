import tkinter as tk
from PIL import Image, ImageTk
from modules.image_methods import (negative, reduceBits, brighten, histogramEqual,
                                gammaCorrection,histogramLocalEqual, smoothBox, smoothGaussian, statisticalFilter,
                                unsharpFilter, sharpenLaplacian)

class ImageWindow(tk.Frame):
    def __init__(self, parent, image_path, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.var_image_path = image_path
        self.var_image = Image.open(self.var_image_path)
        self.var_image_factor = 1
        self.var_image_stack = []
        self.label_image = tk.Label(self.parent)
        self.menu_bar = tk.Menu(self)
        self.normalize_resolution()
        self.display_image()
        self.load_menubar()

    def normalize_resolution(self):
        var_image_width, var_image_height = self.var_image.size
        var_window_width, var_window_height = self.winfo_screenwidth(), self.winfo_screenheight()
        var_width_factor = var_image_width / var_window_width
        var_height_factor = var_image_height / var_window_height
        if ((var_height_factor > 1) or (var_width_factor > 1)):
            self.var_image_factor = var_width_factor if var_width_factor > var_height_factor  else var_height_factor
            var_image_width, var_image_height = int(var_image_width / self.var_image_factor), int(var_image_height / self.var_image_factor)
            self.var_image = self.var_image.resize((var_image_width, var_image_height))
        self.var_image_stack.append(self.var_image)

    def display_image(self):
        var_image = ImageTk.PhotoImage(self.var_image)
        self.label_image.configure(image=var_image)
        self.label_image.image = var_image
        self.label_image.pack(side="top", fill="both", expand="no")

    def menubar_file_undo(self):
        if(len(self.var_image_stack) > 1):
            self.var_image_stack.pop(-1)
            self.var_image = self.var_image_stack[-1]
        self.display_image()

    def menubar_file_save_as(self):
        var_types_extensions = [('PNG file','*.png')]
        try:
            var_save_file = tk.filedialog.asksaveasfile("wb", filetypes=var_types_extensions, defaultextension=var_types_extensions)
            self.var_image  = self.var_image.resize((int(self.var_image.size[0]*self.var_image_factor), int(self.var_image.size[1]*self.var_image_factor)))
            self.var_image.save(var_save_file, format='PNG')
        except AttributeError:
            pass
    
    def menubar_image_negative(self):
        self.var_image = negative(self.var_image_path)
        self.var_image_stack.append(self.var_image)
        self.display_image()
    
    def menubar_image_reducebits(self,count):
        self.var_image = reduceBits(self.var_image_path,count)
        self.var_image_stack.append(self.var_image)
        self.display_image()
    
    def menubar_image_brighten(self,brightVal):
        self.var_image = brighten(self.var_image_path,brightVal)
        self.var_image_stack.append(self.var_image)
        self.display_image()
    
    def menubar_image_histogramEqual(self):
        self.var_image = histogramEqual(self.var_image_path)
        self.var_image_stack.append(self.var_image)
        self.display_image()
    
    def menubar_image_gammaCorrection(self,gamma,constant):
        self.var_image = gammaCorrection(self.var_image_path,gamma,constant)
        self.var_image_stack.append(self.var_image)
        self.display_image()
    
    def menubar_image_histogramLocalEqual(self,neighborhood_size):
        self.var_image = histogramLocalEqual(self.var_image_path,neighborhood_size)
        self.var_image_stack.append(self.var_image)
        self.display_image()
    
    def menubar_image_smoothBox(self,kernelSize):
        self.var_image = smoothBox(self.var_image_path,kernelSize)
        self.var_image_stack.append(self.var_image)
        self.display_image()
    
    def menubar_image_smoothGaussian(self,kernelSize):
        self.var_image = smoothGaussian(self.var_image_path,kernelSize)
        self.var_image_stack.append(self.var_image)
        self.display_image()
    
    def menubar_image_statisticalFilter(self,neighborhoodSize, statCode):
        self.var_image = statisticalFilter(self.var_image_path,neighborhoodSize, statCode)
        self.var_image_stack.append(self.var_image)
        self.display_image()
    
    def menubar_image_unsharpFilter(self,kernelSize):
        self.var_image = unsharpFilter(self.var_image_path,kernelSize)
        self.var_image_stack.append(self.var_image)
        self.display_image()
    
    def menubar_image_sharpenLaplacian(self,kernelSize):
        self.var_image = sharpenLaplacian(self.var_image_path,kernelSize)
        self.var_image_stack.append(self.var_image)
        self.display_image()

    def menubar_null(self):
        pass

    def load_menubar(self):
        #file menu
        fileMenu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Undo", command=self.menubar_file_undo)
        fileMenu.add_command(label="Save As", command=self.menubar_file_save_as)
        fileMenu.add_command(label="Close File", command=self.parent.destroy)
        #intensity mods menu
        intensityMenu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Intensity Mods", menu=intensityMenu)
        intensityMenu.add_command(label="Negative transform", command=self.menubar_image_negative)
        bitreductionMenu = tk.Menu(intensityMenu, tearoff=False) #bitreduction
        intensityMenu.add_cascade(label="Bit reduction", menu=bitreductionMenu)
        bitreductionMenu.add_command(label="2 bits per pixel", command=lambda: self.menubar_image_reducebits(7))
        bitreductionMenu.add_command(label="4 bits per pixel", command=lambda: self.menubar_image_reducebits(6))
        bitreductionMenu.add_command(label="8 bits per pixel", command=lambda: self.menubar_image_reducebits(5))
        bitreductionMenu.add_command(label="16 bits per pixel", command=lambda: self.menubar_image_reducebits(4))
        bitreductionMenu.add_command(label="32 bits per pixel", command=lambda: self.menubar_image_reducebits(3))
        bitreductionMenu.add_command(label="64 bits per pixel", command=lambda: self.menubar_image_reducebits(2))
        bitreductionMenu.add_command(label="128 bits per pixel", command=lambda: self.menubar_image_reducebits(1))
        
        brigthenMenu = tk.Menu(intensityMenu, tearoff=False) #brighten
        intensityMenu.add_cascade(label="Brighten transform", menu=brigthenMenu)
        brigthenMenu.add_command(label="+25 intensity", command=lambda: self.menubar_image_brighten(25))
        brigthenMenu.add_command(label="+50 intensity", command=lambda: self.menubar_image_brighten(50))
        brigthenMenu.add_command(label="+75 intensity", command=lambda: self.menubar_image_brighten(75))
        brigthenMenu.add_command(label="+100 intensity", command=lambda: self.menubar_image_brighten(100))
        gammaMenu = tk.Menu(intensityMenu, tearoff=False) #gamma correction
        intensityMenu.add_cascade(label="Gamma correction", menu=gammaMenu)
        gammaMenu.add_command(label="gamma = 0.2", command=lambda: self.menubar_image_gammaCorrection(0.2,1))
        gammaMenu.add_command(label="gamma = 0.3", command=lambda: self.menubar_image_gammaCorrection(0.3,1))
        gammaMenu.add_command(label="gamma = 0.4", command=lambda: self.menubar_image_gammaCorrection(0.4,1))
        gammaMenu.add_command(label="gamma = 2.0", command=lambda: self.menubar_image_gammaCorrection(2.0,1))
        gammaMenu.add_command(label="gamma = 3.0", command=lambda: self.menubar_image_gammaCorrection(3.0,1))
        gammaMenu.add_command(label="gamma = 4.0", command=lambda: self.menubar_image_gammaCorrection(4.0,1))
        intensityMenu.add_command(label="Histogram equalization", command=self.menubar_image_histogramEqual)
        localhistMenu = tk.Menu(intensityMenu, tearoff=False) #local hist
        intensityMenu.add_cascade(label="Local histogram equalization", menu=localhistMenu)
        localhistMenu.add_command(label="3x3 kernel", command=lambda: self.menubar_image_histogramLocalEqual(3))
        localhistMenu.add_command(label="5x5 kernel", command=lambda: self.menubar_image_histogramLocalEqual(5))
        localhistMenu.add_command(label="7x7 kernel", command=lambda: self.menubar_image_histogramLocalEqual(7))
        localhistMenu.add_command(label="9x9 kernel", command=lambda: self.menubar_image_histogramLocalEqual(9))
        localhistMenu.add_command(label="11x11 kernel", command=lambda: self.menubar_image_histogramLocalEqual(11))
        localhistMenu.add_command(label="13x13 kernel", command=lambda: self.menubar_image_histogramLocalEqual(13))
        localhistMenu.add_command(label="15x15 kernel", command=lambda: self.menubar_image_histogramLocalEqual(15))
        #filter menu
        filterMenu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Filtering", menu=filterMenu)
        boxfilterMenu = tk.Menu(filterMenu, tearoff=False) #box filter
        filterMenu.add_cascade(label="Smoothing - box filter", menu=boxfilterMenu)
        boxfilterMenu.add_command(label="3x3 kernel", command=lambda: self.menubar_image_smoothBox(3))
        boxfilterMenu.add_command(label="5x5 kernel", command=lambda: self.menubar_image_smoothBox(5))
        boxfilterMenu.add_command(label="7x7 kernel", command=lambda: self.menubar_image_smoothBox(7))
        boxfilterMenu.add_command(label="9x9 kernel", command=lambda: self.menubar_image_smoothBox(9))
        boxfilterMenu.add_command(label="11x11 kernel", command=lambda: self.menubar_image_smoothBox(11))
        boxfilterMenu.add_command(label="13x13 kernel", command=lambda: self.menubar_image_smoothBox(13))
        boxfilterMenu.add_command(label="15x15 kernel", command=lambda: self.menubar_image_smoothBox(15))
        gaussianfilterMenu = tk.Menu(filterMenu, tearoff=False) #gaussian
        filterMenu.add_cascade(label="Smoothing - Gaussian filter ", menu=gaussianfilterMenu)
        gaussianfilterMenu.add_command(label="3x3 kernel", command=lambda: self.menubar_image_smoothGaussian(3))
        gaussianfilterMenu.add_command(label="5x5 kernel", command=lambda: self.menubar_image_smoothGaussian(5))
        gaussianfilterMenu.add_command(label="7x7 kernel", command=lambda: self.menubar_image_smoothGaussian(7))
        gaussianfilterMenu.add_command(label="9x9 kernel", command=lambda: self.menubar_image_smoothGaussian(9))
        gaussianfilterMenu.add_command(label="11x11 kernel", command=lambda: self.menubar_image_smoothGaussian(11))
        gaussianfilterMenu.add_command(label="13x13 kernel", command=lambda: self.menubar_image_smoothGaussian(13))
        gaussianfilterMenu.add_command(label="15x15 kernel", command=lambda: self.menubar_image_smoothGaussian(15))
        laplacianfilterMenu = tk.Menu(filterMenu, tearoff=False) #laplacian
        filterMenu.add_cascade(label="Sharpening - Laplacian filter ", menu=laplacianfilterMenu)
        laplacianfilterMenu.add_command(label="3x3 kernel", command=lambda: self.menubar_image_sharpenLaplacian(3))
        laplacianfilterMenu.add_command(label="5x5 kernel", command=lambda: self.menubar_image_sharpenLaplacian(5))
        laplacianfilterMenu.add_command(label="7x7 kernel", command=lambda: self.menubar_image_sharpenLaplacian(7))
        laplacianfilterMenu.add_command(label="9x9 kernel", command=lambda: self.menubar_image_sharpenLaplacian(9))
        laplacianfilterMenu.add_command(label="11x11 kernel", command=lambda: self.menubar_image_sharpenLaplacian(11))
        laplacianfilterMenu.add_command(label="13x13 kernel", command=lambda: self.menubar_image_sharpenLaplacian(13))
        laplacianfilterMenu.add_command(label="15x15 kernel", command=lambda: self.menubar_image_sharpenLaplacian(15))
        unsharpenfilterMenu = tk.Menu(filterMenu, tearoff=False) #unsharpen
        filterMenu.add_cascade(label="Unsharpening - Gaussian filter", menu=unsharpenfilterMenu)
        unsharpenfilterMenu.add_command(label="3x3 kernel", command=lambda: self.menubar_image_unsharpFilter(3))
        unsharpenfilterMenu.add_command(label="5x5 kernel", command=lambda: self.menubar_image_unsharpFilter(5))
        unsharpenfilterMenu.add_command(label="7x7 kernel", command=lambda: self.menubar_image_unsharpFilter(7))
        unsharpenfilterMenu.add_command(label="9x9 kernel", command=lambda: self.menubar_image_unsharpFilter(9))
        unsharpenfilterMenu.add_command(label="11x11 kernel", command=lambda: self.menubar_image_unsharpFilter(11))
        unsharpenfilterMenu.add_command(label="13x13 kernel", command=lambda: self.menubar_image_unsharpFilter(13))
        unsharpenfilterMenu.add_command(label="15x15 kernel", command=lambda: self.menubar_image_unsharpFilter(15))
        medianfilterMenu = tk.Menu(filterMenu, tearoff=False) #median
        filterMenu.add_cascade(label="Median filter", menu=medianfilterMenu)
        medianfilterMenu.add_command(label="3x3 kernel", command=lambda: self.menubar_image_statisticalFilter(3,1))
        medianfilterMenu.add_command(label="5x5 kernel", command=lambda: self.menubar_image_statisticalFilter(5,1))
        medianfilterMenu.add_command(label="7x7 kernel", command=lambda: self.menubar_image_statisticalFilter(7,1))
        medianfilterMenu.add_command(label="9x9 kernel", command=lambda: self.menubar_image_statisticalFilter(9,1))
        medianfilterMenu.add_command(label="11x11 kernel", command=lambda: self.menubar_image_statisticalFilter(11,1))
        medianfilterMenu.add_command(label="13x13 kernel", command=lambda: self.menubar_image_statisticalFilter(13,1))
        medianfilterMenu.add_command(label="15x15 kernel", command=lambda: self.menubar_image_statisticalFilter(15,1))
        minfilterMenu = tk.Menu(filterMenu, tearoff=False) #min
        filterMenu.add_cascade(label="Minimum filter", menu=minfilterMenu)
        minfilterMenu.add_command(label="3x3 kernel", command=lambda: self.menubar_image_statisticalFilter(3,0))
        minfilterMenu.add_command(label="5x5 kernel", command=lambda: self.menubar_image_statisticalFilter(5,0))
        minfilterMenu.add_command(label="7x7 kernel", command=lambda: self.menubar_image_statisticalFilter(7,0))
        minfilterMenu.add_command(label="9x9 kernel", command=lambda: self.menubar_image_statisticalFilter(9,0))
        minfilterMenu.add_command(label="11x11 kernel", command=lambda: self.menubar_image_statisticalFilter(11,0))
        minfilterMenu.add_command(label="13x13 kernel", command=lambda: self.menubar_image_statisticalFilter(13,0))
        minfilterMenu.add_command(label="15x15 kernel", command=lambda: self.menubar_image_statisticalFilter(15,0))
        maxfilterMenu = tk.Menu(filterMenu, tearoff=False) #max
        filterMenu.add_cascade(label="Maximum filter", menu=maxfilterMenu)
        maxfilterMenu.add_command(label="3x3 kernel", command=lambda: self.menubar_image_statisticalFilter(3,2))
        maxfilterMenu.add_command(label="5x5 kernel", command=lambda: self.menubar_image_statisticalFilter(5,2))
        maxfilterMenu.add_command(label="7x7 kernel", command=lambda: self.menubar_image_statisticalFilter(7,2))
        maxfilterMenu.add_command(label="9x9 kernel", command=lambda: self.menubar_image_statisticalFilter(9,2))
        maxfilterMenu.add_command(label="11x11 kernel", command=lambda: self.menubar_image_statisticalFilter(11,2))
        maxfilterMenu.add_command(label="13x13 kernel", command=lambda: self.menubar_image_statisticalFilter(13,2))
        maxfilterMenu.add_command(label="15x15 kernel", command=lambda: self.menubar_image_statisticalFilter(15,2))
        
        self.parent.config(menu=self.menu_bar)