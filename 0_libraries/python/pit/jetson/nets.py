#!/usr/bin/python3

import jetson_inference
import jetson_utils
import time
import argparse
import numpy as np

class ImageNet():

    def __init__(
            self,network = 'googlenet',
            imageWidth=640,
            imageHeight=480, 
            threshold = 0.1, 
            showImage = True, 
            outputURI = "", 
            verbose=True
        ):
        '''
        threshold - used in combination with topK=0 for image tagging; 
        classes with confidence higher than threshold are shown
        network - pre-trained model to load, one of the following:
            alexnet
            googlenet
            googlenet-12
            resnet-18
            resnet-50
            resnet-101
            resnet-152
            vgg-16
            vgg-19
            inception-v4
        '''

        self.verbose=verbose
        self.font=jetson_utils.cudaFont()
        self.modelName = 'imageNet'
        
        if showImage:
            self._output = jetson_utils.videoOutput(outputURI)
        self.showImage = showImage
        
        self.net=jetson_inference.imageNet(network)
        self.net.SetThreshold(threshold)

        self.img=jetson_utils.cudaAllocMapped(width=imageWidth,
                                              height=imageHeight,
                                              format='rgb8')
        
        if not self.showImage:
                print('The parameter showImageOutput is set to False.',
                      'When running the render() function',
                      'it will never display the image despite being called.')
        
    def pre_process(self, inputImg):
        #https://github.com/dusty-nv/jetson-utils/blob/master/python/examples/cuda-from-cv.py
        bgrImg = jetson_utils.cudaFromNumpy(inputImg, isBGR=True)
        jetson_utils.cudaConvertColor(bgrImg, self.img)
        return self.img

    def predict(self, inputImg, topK = 2, textOnImage = True): 

        self.predictions = self.net.Classify(inputImg, topK=topK)
        labelList = []
        confidenceList = []
        
        for n, (classID, confidence) in enumerate(self.predictions):
            classLabel = self.net.GetClassLabel(classID)
            confidence *= 100.0
            if self.verbose:
                print(f"{self.modelName}: {confidence:05.2f}%",
                        f"class #{classID} ({classLabel})")
            labelList.append(classLabel)
            confidenceList.append(confidence)

            if self.showImage:
                if textOnImage:
                    self.font.OverlayText(inputImg, 
                                text=f"{confidence:05.2f}% {classLabel}", 
                                x=5, 
                                y=5 + n * (self.font.GetSize() + 5),
                                color=self.font.White, 
                                background=self.font.Gray40)
            
        return labelList, confidenceList

    def render(self, printPerformance = False):
        if self.showImage:
            self._output.Render(self.img)
            # update the title bar
            self._output.SetStatus("{:s} | Network {:.0f} FPS".format(
                        self.net.GetNetworkName(), self.net.GetNetworkFPS()))
            
            if printPerformance:
                # print out performance info
                self.net.PrintProfilerTimes()
        else:
            pass #function will ony work 
                 #if showImageOutput was enabled on initialization

class ActionNet():
    def __init__(
            self,
            network = 'resnet-18',
            imageWidth=640,
            imageHeight=480, 
            threshold = 0.1, 
            skipFrames = 1, 
            showImage = True, 
            outputURI = "", 
            verbose=True
        ):
        '''
        threhold - class with confidence higher than threshold is shown
        skipFrames - number of frames to skip when 
                    using consecutive frames as input to actoinNet
        network - pre-trained model to load, one of the following:
            resnet-18
            resnet-34
        '''
        self.verbose=verbose
        self.font=jetson_utils.cudaFont()
        self.modelName = 'actionNet'
        
        if showImage:
            self._output = jetson_utils.videoOutput(outputURI)
        self.showImage = showImage
        
        self.net=jetson_inference.actionNet(network)
        self.net.SetThreshold(threshold)
        self.net.SetSkipFrames(skipFrames)

        self.img=jetson_utils.cudaAllocMapped(width=imageWidth,
                                              height=imageHeight,
                                              format='rgb8')
        
        if not self.showImage:
                print('The parameter showImageOutput is set to False.',
                      'When running the render() function',
                      'it will never display the image despite being called.')
                
    def pre_process(self, inputImg):
        #https://github.com/dusty-nv/jetson-utils/blob/master/python/examples/cuda-from-cv.py
        bgrImg = jetson_utils.cudaFromNumpy(inputImg, isBGR=True)
        jetson_utils.cudaConvertColor(bgrImg, self.img)
        return self.img

    def predict(self, inputImg, textOnImage = True): 

        self.predictions = self.net.Classify(inputImg)
        labelList = []
        confidenceList = []

        
        classID, confidence = self.predictions
        confidence*=100

        if classID==-1:
            return labelList, confidenceList

        classLabel = self.net.GetClassDesc(classID)
        if self.verbose:
            print(f"{self.modelName}: {confidence:05.2f}%",
                        f"class #{classID} ({classLabel})")
        
        labelList.append(classLabel)
        confidenceList.append(confidence)

        if self.showImage and textOnImage:
            self.font.OverlayText(
                inputImg, 
                inputImg.width, 
                inputImg.height, 
                "{:05.2f}% {:s}".format(confidence, classLabel), 
                x=5, y=5,
                color=self.font.White, 
                background=self.font.Gray40)
                
        return labelList, confidenceList

    def render(self, printPerformance = False):
        if self.showImage:
            self._output.Render(self.img)
            # update the title bar
            self._output.SetStatus("{:s} | Network {:.0f} FPS".format(
                        self.net.GetNetworkName(), self.net.GetNetworkFPS()))
            
            if printPerformance:
                # print out performance info
                self.net.PrintProfilerTimes()
        else:
            pass #function will ony work 
                 #if showImageOutput was enabled on initialization
         
class DetectNet():
    def __init__(
            self,
            network = 'SSD-Mobilenet-v2',
            imageWidth=640,
            imageHeight=480, 
            threshold = 0.5, 
            alpha = 120, 
            lineWidth = 2.0, 
            showImage = True, 
            outputURI = "", 
            verbose=True
        ):
        """
        threshold - classes with confidence higher than threshold are shown
        alpha - overlay alpha blending value, range 0-255 (default: 120)
        lineWidth - used during overlay when 'lines' is used
        network - pre-trained model to load, one of the following:
            ssd-mobilenet-v1
            ssd-mobilenet-v2 (default)
            ssd-inception-v2
            peoplenet
            peoplenet-pruned
            dashcamnet
            trafficcamnet
            facedetect
        """
        self.network = network
        self.verbose=verbose
        self.modelName = 'detectNet'
        if showImage:
            self._output = jetson_utils.videoOutput(outputURI)
        self.showImage = showImage
        
        self.net=jetson_inference.detectNet(network)

        self.net.SetConfidenceThreshold(threshold)
        self.net.SetLineWidth(lineWidth)
        self.net.SetOverlayAlpha(alpha)

        self.img=jetson_utils.cudaAllocMapped(width=imageWidth,
                                              height=imageHeight,
                                              format='rgb8')
        
        if not self.showImage:
                print('The parameter showImageOutput is set to False.',
                      'When running the render() function',
                      'it will never display the image despite being called.')

    def pre_process(self, inputImg):
        #https://github.com/dusty-nv/jetson-utils/blob/master/python/examples/cuda-from-cv.py
        bgrImg = jetson_utils.cudaFromNumpy(inputImg, isBGR=True)
        jetson_utils.cudaConvertColor(bgrImg, self.img)
        return self.img

    def predict(self, inputImg, overlay = 'box,labels,conf'): 
        # valid combinations are:  'box', 'lines', 'labels', 'conf', 'none'
        # it is possible to combine flags. See default.
	    # (bitwise OR) together with commas or pipe (|) symbol.

        self.predictions = self.net.Detect(inputImg, overlay=overlay)
        labelList = []
        confidenceList = []

        # if type(self.predictions) is tuple:
        #     self.predictions=[self.predictions]
        for n, detection in enumerate(self.predictions):
            classLabel = self.net.GetClassLabel(detection.ClassID)
            confidence = detection.Confidence*100.0
            if self.verbose:
                print(f"{self.modelName}: {confidence:05.2f}%",
                        f"class #{detection.ClassID} ({classLabel})")

            labelList.append(classLabel)
            confidenceList.append(confidence)
        
        return labelList, confidenceList
            
    def render(self, printPerformance = False):
        if self.showImage:
            self._output.Render(self.img)
            # update the title bar
            self._output.SetStatus("{:s} | Network {:.0f} FPS".format(
                                self.network, self.net.GetNetworkFPS()))
            if printPerformance:
                # print out performance info
                self.net.PrintProfilerTimes()
        else:
            pass #function will ony work 
                 #if showImageOutput was enabled on initialization
 
class PoseNet():
    def __init__(
            self, 
            network = 'resnet18-body',
            imageWidth=640,
            imageHeight=480, 
            threshold = 0.15, 
            keypointScale = 0.0052, 
            linkScale = 0.0013, 
            showImage = True, 
            outputURI = "", 
            verbose=True
        ):

        '''
        threshold - value which sets the minimum threshold for detection 
                    (the default is 0.15)
        keypointScale - value which controls the radius 
                        of the keypoint circles in the overlay 
                        (the default is 0.0052)
        linkScale - value which controls the line width 
                    of the link lines in the overlay 
                    (the default is 0.0013)
        network - pre-trained model to load, one of the following:
            resnet18-body
		    resnet18-hand
		    densenet121-body
        '''

        self.network = network
        self.verbose=verbose
        self.font=jetson_utils.cudaFont()
        self.modelName = 'poseNet'
        if showImage:
            self._output = jetson_utils.videoOutput(outputURI)
        self.showImage = showImage
        
        self.net=jetson_inference.poseNet(network)

        self.net.SetThreshold(threshold)
        self.net.SetKeypointScale(keypointScale)
        self.net.SetLinkScale(linkScale)

        self.img=jetson_utils.cudaAllocMapped(width=imageWidth,
                                              height=imageHeight,
                                              format='rgb8')
        
        if not self.showImage:
                print('The parameter showImageOutput is set to False.',
                      'When running the render() function',
                      'it will never display the image despite being called.')
        
    def pre_process(self, inputImg):
        #https://github.com/dusty-nv/jetson-utils/blob/master/python/examples/cuda-from-cv.py
        bgrImg = jetson_utils.cudaFromNumpy(inputImg, isBGR=True)
        jetson_utils.cudaConvertColor(bgrImg, self.img)
        return self.img

    def predict(self, inputImg, overlay = 'links,keypoints'):
        # detection overlay flags (e.g. --overlay=links,keypoints)
		# valid combinations are:  'box', 'links', 'keypoints', 'none'

        self.poses = self.net.Process(inputImg, overlay=overlay)

        if self.verbose:
            # print the pose results
            print("detected {:d} objects in image".format(len(self.poses)))
            # for pose in self.poses:
            #     print(pose)
            #     print(pose.Keypoints)
            #     print('Links', pose.Links)  
        
        return self.poses
  
    def render(self, printPerformance = False):
        if self.showImage:
            self._output.Render(self.img)
            # update the title bar
            self._output.SetStatus("{:s} | Network {:.0f} FPS".format(
                                self.network, self.net.GetNetworkFPS()))
            
            if printPerformance:
                # print out performance info
                self.net.PrintProfilerTimes()
        else:
            pass #function will ony work 
                 # if showImageOutput was enabled on initialization

class DepthNet():
    def __init__(
            self, 
            network = 'fcn-mobilenet',
            imageWidth=640,
            imageHeight=480, 
            visualize = 'input,depth', 
            depthSize = 1, 
            showImage = True, 
            outputURI = "", 
            verbose=True
        ):
        
        '''
        visualize - decide what to desplay. Default displays input and depth
        images side-by-side. To view only depth use visualze='depth'
        visualize - visualization options 
        (can be 'input' 'depth' 'input,depth')
        depth-size - value which scales the size of the depth map 
        relative to the input (the default is 1.0)
        network - pre-trained model to load, one of the following:
            fcn-mobilenet
            fcn-resnet18
            fcn-resnet50
        '''

        self.network = network
        self.verbose=verbose
        self.modelName = 'depthNet'
        self.useInput = 'input' in visualize
        self.useDepth = 'depth' in visualize

        self.net=jetson_inference.depthNet(network)
        if showImage:
            self._output = jetson_utils.videoOutput(outputURI)
        self.showImage = showImage

        self.depth = None
        self.composite = None
        self.depthSize = depthSize

        depth_size = (imageHeight * self.depthSize, 
                      imageWidth * self.depthSize)
        
        composite_size = [0,0]

        if self.useDepth:
            composite_size[0] = depth_size[0]
            composite_size[1] += depth_size[1]
            
        if self.useDepth:
            composite_size[0] = imageHeight
            composite_size[1] += imageWidth

        self.depth = jetson_utils.cudaAllocMapped(width=depth_size[1], 
                                                  height=depth_size[0], 
                                                  format='rgb8')
        
        self.composite = jetson_utils.cudaAllocMapped(width=composite_size[1], 
                                                      height=composite_size[0], 
                                                      format='rgb8')

        self.img=jetson_utils.cudaAllocMapped(width=imageWidth,
                                              height=imageHeight,
                                              format='rgb8')
        
        if not self.showImage:
                print('The parameter showImageOutput is set to False.',
                      'When running the render() function',
                      'it will never display the image despite being called.')
  
    def pre_process(self, inputImg):
        #https://github.com/dusty-nv/jetson-utils/blob/master/python/examples/cuda-from-cv.py
        bgrImg = jetson_utils.cudaFromNumpy(inputImg, isBGR=True)
        jetson_utils.cudaConvertColor(bgrImg, self.img)
        return self.img

    def predict(
            self, 
            inputImg, 
            filter_mode = 'linear', 
            colormap = 'viridis_inverted'
        ):
        
        # colormap - choices=["inferno", "inferno-inverted", 
        #           "magma", "magma-inverted", "parula", "parula-inverted", 
        #            "plasma", "plasma-inverted", "turbo", "turbo-inverted", 
        #            "viridis", "viridis-inverted"])
        # filtermode - filtering mode used during visualization, 
        #           options are: 'point' or 'linear' (default: 'linear')

        self.net.Process(inputImg, self.depth, colormap, filter_mode)

        if self.useInput:
            jetson_utils.cudaOverlay(inputImg, self.composite, 0, 0)

        if self.useDepth:
            jetson_utils.cudaOverlay(self.depth, 
                                     self.composite, 
                                     inputImg.width if self.useInput else 0, 0)

        return jetson_utils.cudaToNumpy(self.depth).squeeze()

    def render(self, printPerformance = False):
        # for consistency the input image argument is there,
        # but nothing happens with it, it grabs the correct 
        # image from the predict function
        if self.showImage:
            self._output.Render(self.composite)
            # update the title bar
            self._output.SetStatus("{:s} | Network {:.0f} FPS".format(
                    self.net.GetNetworkName(), self.net.GetNetworkFPS()))
            jetson_utils.cudaDeviceSynchronize()
            if printPerformance:
                # print out performance info
                self.net.PrintProfilerTimes()
        else:
            pass #function will ony work 
                 #if showImageOutput was enabled on initialization

class SegNet():
    def __init__(
            self,
            network = 'fcn-resnet18-voc',
            imageWidth=640,
            imageHeight=480, 
            visualize='overlay,mask', 
            filter_mode = 'linear', 
            alpha=120.0, 
            showImage = True, 
            outputURI = "",
            verbose=True
        ):
        '''
        visualize - flag accepts mask and/or overlay modes 
        (default is 'overlay,mask')
        alpha - flag sets the alpha blending value for overlay 
        (default is 120)
        filter_mode - flag accepts point or linear sampling 
        (default is linear)
        network - pre-trained model to load, one of the following:
            *If the resolution is omitted from the argument, 
            the lowest resolution model is loaded*
            fcn-resnet18-cityscapes
            fcn-resnet18-cityscapes-512x256
            fcn-resnet18-cityscapes-1024x512
            fcn-resnet18-cityscapes-2048x1024
            fcn-resnet18-deepscene
            fcn-resnet18-deepscene-576x320
            fcn-resnet18-deepscene-864x480
            fcn-resnet18-mhp
            fcn-resnet18-mhp-512x320
            fcn-resnet18-mhp-640x360
            fcn-resnet18-voc
            fcn-resnet18-voc-512x320
            fcn-resnet18-voc-320x320
            fcn-resnet18-sun
            fcn-resnet18-sun-512x400
            fcn-resnet18-sun-640x512
        '''
        self.modelname = 'segNet'
        self.filter_mode = filter_mode
        if showImage:
            self._output = jetson_utils.videoOutput(outputURI)
        self.showImage = showImage
        
        self.net=jetson_inference.segNet(network)
        self.img=jetson_utils.cudaAllocMapped(width=imageWidth,
                                              height=imageHeight,
                                              format='rgb8')
        self.mask = None
        self.overlay = None
        self.composite = None
        self.verbose = verbose
        self.use_mask = "mask" in visualize
        self.use_overlay = "overlay" in visualize
        self.use_composite = self.use_mask and self.use_overlay
        

        if not self.showImage:
                print('The parameter showImageOutput is set to False.',
                      'When running the render() function',
                      'it will never display the image despite being called.')

        if showImage and not self.use_overlay and not self.use_mask:
            raise Exception("invalid visualize flags - ",
                            "valid values are 'overlay' 'mask' 'overlay,mask'")
        
        self.net.SetOverlayAlpha(alpha)
        self.grid_width, self.grid_height = self.net.GetGridSize()	
        self.num_classes = self.net.GetNumClasses()

        self.class_mask = jetson_utils.cudaAllocMapped(width=self.grid_width, 
                                                       height=self.grid_height, 
                                                       format="gray8")
        
        self.class_mask_np = jetson_utils.cudaToNumpy(self.class_mask)

        if self.use_overlay:
            self.overlay = jetson_utils.cudaAllocMapped(width=imageWidth, 
                                                        height=imageHeight, 
                                                        format='rgb8')

        if self.use_mask:
            mask_downsample = 2 if self.use_overlay else 1
            self.mask = jetson_utils.cudaAllocMapped(
                                    width=imageWidth/mask_downsample, 
                                    height=imageHeight/mask_downsample, 
                                    format='rgb8') 

        if self.use_composite:
            self.composite = jetson_utils.cudaAllocMapped(
                                    width=self.overlay.width+self.mask.width, 
                                    height=self.overlay.height, 
                                    format='rgb8') 

    def pre_process(self, inputImg):
        #https://github.com/dusty-nv/jetson-utils/blob/master/python/examples/cuda-from-cv.py
        bgrImg = jetson_utils.cudaFromNumpy(inputImg, isBGR=True)
        jetson_utils.cudaConvertColor(bgrImg, self.img)
        return self.img

    def predict(self, inputImg, ignore_class = "void"): 
        # ignore_class - class to ignore during segmentation 
        # (defalut = 'void')
        
        self.net.Process(inputImg, ignore_class=ignore_class)
        self.net.Mask(self.class_mask, self.grid_width, self.grid_height)
        # generate the overlay
        if self.overlay:
            self.net.Overlay(self.overlay, filter_mode=self.filter_mode)

        # generate the mask
        if self.mask:
            self.net.Mask(self.mask, filter_mode=self.filter_mode)

        # composite the images
        if self.composite:
            jetson_utils.cudaOverlay(self.overlay, self.composite, 0, 0)
            jetson_utils.cudaOverlay(self.mask, 
                                     self.composite, 
                                     self.overlay.width, 
                                     0)
        
        label_mask_np=self.class_mask_np.copy().squeeze()
        if self.verbose:
            self.net.Mask(self.class_mask, self.grid_width, self.grid_height)

            # compute the number of times each class occurs in the mask
            class_histogram, _ = np.histogram(self.class_mask_np, 
                                              bins=self.num_classes, 
                                              range=(0, self.num_classes-1))

            print('grid size:   {:d}x{:d}'.format(self.grid_width, 
                                                  self.grid_height))
            
            print('num classes: {:d}'.format(self.num_classes))

            print('-----------------------------------------')
            print(' ID  class name        count     %')
            print('-----------------------------------------')

            for n in range(self.num_classes):
                percentage = (
                    float(class_histogram[n]) / (
                        float(self.grid_width * self.grid_height)))
                
                print(' {:>2d}  {:<18s} {:>3d}   {:f}'.format(
                                                    n, 
                                                    self.net.GetClassDesc(n), 
                                                    class_histogram[n], 
                                                    percentage))
        
        return label_mask_np

    def render(self, printPerformance=False):
        
        if self.showImage:
            if printPerformance:
                # print out performance info
                self.net.PrintProfilerTimes()
            if self.use_overlay and self.use_mask:
                self._output.Render(self.composite)
            elif self.use_overlay:
                self._output.Render(self.overlay)
            elif self.use_mask:
                self._output.Render(self.mask)
        else:
            pass #function will ony work 
                 #if showImageOutput was enabled on initialization
        
