#!/usr/bin/python3

import jetson_inference
import jetson_utils
import time
import argparse
import sys


'''
Download networks for using the Jetson Inference Library. 
By default, all models for ImageNet, ActionNet, DetectNet, PoseNet, DepthNet 
and SegNet are downloaded and converted to tensorRT engines. 

By adding an argument when running the file you can choose which net 
to download models from. 

1- ImageNet
2- ActionNet
3- DetectNet
4- PoseNet
5- DepthNet
6. SegNet

Modify the variables 'downloadNetName' to False if none of the networks 
for that type of net will be downloaded. 

Change values in the 'netName_models' dictionary to False if only 
some of the networks for that type of net will be downloaded.
'''

start_time=time.time()

downloaded = 'Models successfully downloaded: '
failed = 'Models failed during download: '

downloadImageNet = True
downloadActionNet = True
downloadDetectNet = True
downloadPoseNet = True
downloadDepthNet = True
downloadSegNet = True

if len(sys.argv) > 1:
    downloadImageNet = False
    downloadActionNet = False
    downloadDetectNet = False
    downloadPoseNet = False
    downloadDepthNet = False
    downloadSegNet = False

    netToDownload = int(sys.argv[1])

    if netToDownload == 1:
        downloadImageNet = True
    elif netToDownload == 2:
        downloadActionNet = True
    elif netToDownload == 3:
        downloadDetectNet = True
    elif netToDownload == 4:
        downloadPoseNet = True
    elif netToDownload == 5:
        downloadDepthNet = True
    elif netToDownload == 6:
        downloadSegNet = True
    else:
        print('Argument must be a number between 1 and 6')
            

# -- -- -- -- -- -- -- imageNet Models -- -- -- -- -- -- -- -- -- 

if downloadImageNet:
    imageNet_models = { 'alexnet': True,
                        'googlenet': True,
                        # 'googlenet-12': False, # loading issue to solve manually  https://github.com/dusty-nv/jetson-inference/issues/1734
                        'resnet-18': True,
                        'resnet-50': True,
                        'resnet-101': True,
                        'resnet-152': True,
                        'resnet18-tagging-voc': True,
                        'vgg-16': True,
                        'vgg-19': True,
                        'inception-v4': True
                        }  

    for net in imageNet_models:
        if imageNet_models[net]:
            try:
                jetson_inference.imageNet(net)
                downloaded = downloaded + net + ', '
            except:
                failed = failed + net + ', '

# -- -- -- -- -- -- -- actionNet Models -- -- -- -- -- -- -- -- -- 

if downloadActionNet:
    actionNet_models = {'resnet-18': True,
                        'resnet-34': True
                        } 

    for net in actionNet_models:
        if actionNet_models[net]:
            try:
                jetson_inference.actionNet(net)
                downloaded = downloaded + net + ', '
            except:
                failed = failed + net + ', '

# -- -- -- -- -- -- -- depthNet Models -- -- -- -- -- -- -- -- -- 

if downloadDepthNet:
    depthNet_models =  {'fcn-mobilenet': True,
                        'fcn-resnet18': True,
                        'fcn-resnet50': True
                        } 

    for net in depthNet_models:
        if depthNet_models[net]:
            try:
                jetson_inference.depthNet(net)
                downloaded = downloaded + net + ', '
            except:
                failed = failed + net + ', '

# -- -- -- -- -- -- -- detectNet Models -- -- -- -- -- -- -- -- -- 

if downloadDetectNet:
    detectNet_models = {'ssd-mobilenet-v2': True,
                        'ssd-inception-v2': True,
                        # 'ssd-mobilenet-v1': False, # can't load, unresolved
                        'peoplenet': True,
                        'peoplenet-pruned': True,
                        'dashcamnet': True,
                        'trafficcamnet': True,
                        'facedetect': True
                        } 

    for net in detectNet_models:
        if detectNet_models[net]:
            try:
                jetson_inference.detectNet(net)
                downloaded = downloaded + net + ', '
            except:
                failed = failed + net + ', '

# -- -- -- -- -- -- -- poseNet Models -- -- -- -- -- -- -- -- -- 

if downloadPoseNet:
    poseNet_models = {'resnet18-body': True,
                      'resnet18-hand': True,
                      'densenet121-body': True
                       } 

    for net in poseNet_models:
        if poseNet_models[net]:
            try:
                jetson_inference.poseNet(net)
                downloaded = downloaded + net + ', '
            except:
                failed = failed + net + ', '

# -- -- -- -- -- -- -- segNet Models -- -- -- -- -- -- -- -- -- 

if downloadSegNet:
    segNet_models = {'fcn-resnet18-cityscapes': True,
                     'fcn-resnet18-cityscapes-512x256': True,
                     'fcn-resnet18-cityscapes-1024x512': True,
                     'fcn-resnet18-cityscapes-2048x1024': True,
                     'fcn-resnet18-deepscene': True,
                     'fcn-resnet18-deepscene-576x320': True,
                     'fcn-resnet18-deepscene-864x480': True,
                     'fcn-resnet18-mhp': True,
                     'fcn-resnet18-mhp-512x320': True,
                     'fcn-resnet18-mhp-640x360': True,
                     'fcn-resnet18-voc': True,
                     'fcn-resnet18-voc-320x320': True,
                     'fcn-resnet18-voc-512x320': True,
                     'fcn-resnet18-sun': True,
                     'fcn-resnet18-sun-512x400': True,
                     'fcn-resnet18-sun-640x512': True
                     } 

    for net in segNet_models:
        if segNet_models[net]:
            try:
                jetson_inference.segNet(net)
                downloaded = downloaded + net + ', '
            except:
                failed = failed + net + ', '


print('task complete, process time {:.2f} seconds'.format(time.time()-start_time))

print(downloaded)

print(failed)