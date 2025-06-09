import numpy as np
import cv2
from ultralytics import YOLO
import torch 
import os
from pit.YOLO.utils import TrafficLight,Obstacle,MASK_COLORS_RGB
import requests
import platform
from tqdm import tqdm
import copy

class YOLOv8():
    """This LaneNet class is designed to simplify the usage of LaneNet. Memory 
       allocation, pre-processing, inference, and post-processing are all handled
       by this class.
    
    Attributes:
        defaultPath (str): Default path to the optimized TensorRT engine. 
        modelPath (str): User specified path to model.
        imageHeight (int): Height of the input image.
        imageWidth (int): Width of the input image.
        img (ndarray): Buffer for the input image.
        net (YOLO): an instance of YOLO from Ultralytics.

    """
    def __init__(
        self,
        imageWidth = 640,
        imageHeight = 480,
        modelPath = None,
        convert_tensorrt = True,
        ):
        """Creates a LaneNet Instance. Find the path to the LaneNet model, load the 
           Tensor RT engine, and prepare for executing inference.

        Args:
            modelPath (str): User specified path to model.
            imageHeight (int): Expected height of the input image.
            imageWidth (int): Expected width of the input image.

        """
        self.defaultPath = os.path.normpath(os.path.join(
                        os.path.dirname(__file__), 
                        '../../../resources/pretrained_models/yolov8s-seg.engine'))
        self.imageWidth , self.imageHeight = self._dim_check(imageWidth, imageHeight)
        self.convert_tensorrt = convert_tensorrt and not platform.system() == "Windows"
        
        self.modelPath = self.__check_path(modelPath)
        self.img=np.empty((self.imageHeight,self.imageWidth,3),dtype=np.uint8)
        self._calc_distence = False
        self.net=YOLO(self.modelPath,task='segment')
        print('YOLOv8 model loaded')   

    def pre_process(self,inputImg):
        '''Resize input image to the expected image shape if applicable. 

        Args: 
            inputImg (ndarray): RGB image, typically front camera feed.

        Returns:
            ndarray: Resized input image in expected shape.

        '''
        self.inputShape=inputImg.shape[:2]
        if inputImg.shape[:2] != (self.imageHeight,self.imageWidth):
            inputImg=cv2.resize(inputImg,
                                (self.imageWidth,self.imageHeight))
        self.img[:,:,:]=inputImg[:,:,:]
        return self.img
    
    def predict(self, inputImg, classes = [2,9,11,33], confidence = 0.3, verbose = False, half = False):
        '''Use YOLOv8s-seg to run predictions and output segmentation masks of 
           detected objects. 

        Args:
            inputImg (ndarray): Pre-processed input image array in the expected 
                                input image shape.
            classes (list): Filters predictions to a set of class IDs. Only detections 
                            belonging to the specified classes will be returned.
            confidence (float): Sets the minimum confidence threshold for detections. 
                                Objects detected with confidence below this threshold 
                                will be disregarded.
            verbose (bool): If set to True , return log string for each prediction.
            half (bool): Enables half-precision (FP16) inference, which can speed 
                         up model inference on supported GPUs with minimal impact
                         on accuracy.


        Returns:
            Results: An Ultralytics Results object which stores all information about
                     the prediction output. Refer to the following link:
                     https://docs.ultralytics.com/modes/predict/#working-with-results

        '''
        self.predictions = self.net.predict(inputImg,
                                            verbose = verbose,
                                            imgsz = (self.imageHeight,
                                                     self.imageWidth),
                                            classes = classes,
                                            conf = confidence,
                                            half = half
                                            )
        self.objectsDetected=self.predictions[0].boxes.cls.cpu().numpy()
        self.FPS=1000/self.predictions[0].speed['inference']
        return self.predictions[0]
    
    def render(self,showFPS=True):
        '''Annotate the input image using Ultralytics API. Annotated image will 
           be resized if needed.

        Args:
            showFPS (bool): If set to True, texts showing the FPS will be added 
                            to the top right conner of the output image.

        Returns:
            ndarray: Input image overlaid with predicted segmentation masks.

        '''
        annotatedImg = self.predictions[0].plot()
        if annotatedImg.shape[:2] != self.inputShape:
            annotatedImg=cv2.resize(annotatedImg,
                                (self.inputShape[1],self.inputShape[0]))
        if showFPS:
            cv2.putText(annotatedImg, 'Inference FPS: '+str(round(self.FPS)), 
                        (495,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255,255,255), 2)
        return annotatedImg

    def post_processing(self,alignedDepth=None,clippingDistance=10):
        '''Calculate the distance to each detected objects and determine the status
           of the traffic lights in applicable.

        Args:
            alignedDepth (ndarray): A depth image aligned to the rgb input. If not
                                    provided, the distance calculation will be skipped.
            clippingDistance (float): Pixels in the depth image further from clipping
                                      distance will be set to zero.

        Returns:
            list: A list of Obstacle objects which store relevant information 
                  of detected objects.

        '''

        self.processedResults = []
        self._calc_distence = False

        if len (self.objectsDetected) == 0:
            return self.processedResults
        self.bounding = self.predictions[0].boxes.xyxy.cpu().numpy().astype(int)
        if alignedDepth is not None:
            if alignedDepth.shape[:2] != (self.imageHeight,self.imageWidth):
                alignedDepth=cv2.resize(alignedDepth,
                                        (self.imageWidth,self.imageHeight))
            depth3D = np.dstack((alignedDepth,alignedDepth,alignedDepth))
            bgRemoved = np.where((depth3D > clippingDistance)| 
                                 (depth3D <= 0), 0, depth3D)
            self._calc_distence = True
            self.depthTensor=torch.as_tensor(bgRemoved,device="cuda:0")
        for i in range(len(self.objectsDetected)):
            if self.objectsDetected[i]==9:
                trafficBox = self.bounding[i]
                traficLightColor = self.check_traffic_light(trafficBox,self.img)
                result=TrafficLight(color=traficLightColor)
                result.name+=(' ('+traficLightColor+')')
            else:
                name=self.predictions[0].names[self.objectsDetected[i]]
                result=Obstacle(name=name)
            if alignedDepth is not None:
                mask=self.predictions[0].masks.data.cuda()[i]
                distance=self.check_distance(mask,self.depthTensor[:,:,:1])
                result.distance=distance.cpu().numpy().round(3)
            points=self.predictions[0].boxes.xyxy.cpu()[i]
            conf=self.predictions[0].boxes.conf.cpu().numpy()[i]
            x=int(points.numpy()[0])
            y=int(points.numpy()[1])
            result.x=x
            result.y=y
            result.conf=conf
            self.processedResults.append(result)
        return self.processedResults

    def post_process_render(self, showFPS = True, bbox_thickness = 4):
        '''Annotate input image with colored segmentation mask and distances.
        
        Args:
            showFPS (bool): If set to True, texts showing the FPS will be added 
                            to the top right conner of the output image.
            bbox_thickness (int): Thichness of the bounding box outline.
        
        Returns:
            ndarray: Input image annotated with colored segmentation masks and
                     distances to the objects.

        '''
        if not self.processedResults:
            if self.img.shape[:2] != self.inputShape:
                out=cv2.resize(self.img,
                               (self.inputShape[1],self.inputShape[0]))
            else: out=self.img
            return out
        colors=[]
        masks = self.predictions[0].masks.data.cuda()
        boxes = self.predictions[0].boxes.xyxy.cpu().numpy().astype(int)
        imgClone=self.img.copy()
        for i in range(len(self.objectsDetected)):
            colors.append(MASK_COLORS_RGB[self.objectsDetected[i].astype(int)])
            name=self.processedResults[i].name
            x=self.processedResults[i].x
            y=self.processedResults[i].y
            distance=self.processedResults[i].distance
            cv2.rectangle(imgClone,(boxes[i,:2]),(boxes[i,2:4]),colors[i],bbox_thickness)
            cv2.putText(imgClone, name, 
                        (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        colors[i], 2)
            if self._calc_distence:
                cv2.putText(imgClone,str(distance) + " m",
                            (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            colors[i], 2)
        if showFPS:
            cv2.putText(imgClone, 'Inference FPS: '+str(round(self.FPS)), 
                        (495,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255,255,255), 2)
        imgTensor=torch.from_numpy(imgClone).to("cuda:0")
        imgMask=self.mask_color(masks, imgTensor,colors)
        if imgMask.shape[:2] != self.inputShape:
            imgMask=cv2.resize(imgMask,
                               (self.inputShape[1],self.inputShape[0]))
        return imgMask

    @staticmethod
    def convert_to_trt(path,
                       imageWidth = 640,
                       imageHeight = 480,
                       half = True,
                       batch = 1,
                       int8 = False
                       ):
        '''Optimize input pytorch model via Ultralytics API and save as TensorRT engine. 
        
        Args:
            path (str): Path to the pytorch model.
            imageWidth (int): Expected image width.
            imageHeight (int): Expected image height.
            half (bool): Enables FP16 (half-precision) quantization, reducing model 
                         size and potentially speeding up inference on supported hardware.
            batch (bool): Specifies model batch inference size.
            int8 (bool): Activates INT8 quantization, further compressing the model 
                         and speeding up inference with minimal accuracy loss, 
                         primarily for edge devices.

        Returns:
            str: path to the TensorRT engine.

        '''
        print('Converting to teneorRT engine')
        model = YOLO(path)
        model.export(format="engine",
                     imgsz=(imageHeight,imageWidth),
                     half=half,
                     batch=batch,
                     int8=int8)
        enginePath = os.path.splitext(path)[0]+'.engine'
        return enginePath
        
    @staticmethod
    def mask_color(masks, im_gpu,colors, alpha=0.5):
        '''Overlay input image with segmentation masks with assigned colors.
        
        Args: 
            masks (torch.Tensor): Segmentation masks of detected objects
            im_gpu (torch.Tensor): Input image
            colors (list): List of colors (RGB values) assigned to each object.
            alpha (float): Transparency of the mask color.

        Returns:
            ndarray: Input image overlaid with colored object masks.

        '''
        colors = torch.tensor(colors, device="cuda:0", dtype=torch.float32) / 255.0 
        colors = colors[:, None, None]
        masks = masks.unsqueeze(3)
        masks_color = masks * (colors * alpha)
        inv_alpha_masks = (1 - masks * alpha).cumprod(0) 
        mcs = masks_color.max(dim=0).values  
        im_gpu = im_gpu/255
        im_gpu = im_gpu * inv_alpha_masks[-1] + mcs 
        im_mask = im_gpu * 255
        im_mask_np = im_mask.squeeze().byte().cpu().numpy()
        return im_mask_np
    
    @staticmethod
    def _dim_check(height,width):
        '''Check the shape of the input image if they are a multiple of 32, if not
           override the image shape to the closest multiple of 32.
        
        Args: 
            height (int): Expected image height.
            width (int): Expected image width.

        Returns:
            Tuple: Index 0 - Adjusted image height.
                   Index 1 - Adjusted image width.

        '''
        height_remainder=height%32
        width_remainder=width%32
        new_height = height
        new_width = width
        if height_remainder == 0 and width_remainder == 0:
            return height,width
        if height_remainder != 0:
            new_height=height-height_remainder+32
        if width_remainder != 0:
            new_width=width-width_remainder+32
        print('image size',(height,width),'must be multiple of max stride 32, updating to',(new_height,new_width))
        return new_height,new_width

    
    def check_traffic_light(self,traffic_box,im_cpu):
        '''Check traffic light status by estimating the position of the three lights
           and comparing the color brightness of the three locations.
        
        Args: 
            traffic_box (ndarray): Boxing box of the detected image in xyxy format.
            im_cpu (ndarray): Input RGB image.

        Returns:
            str: color of the traffic light, return 'idle' if none is on.

        '''
        mask = np.zeros((self.imageHeight,self.imageWidth),dtype='uint8')
        x1,y1,x2,y2=(traffic_box[0], traffic_box[1], traffic_box[2], traffic_box[3])
        d = 0.3*(x2-x1)
        R_center=(int(x1/2+x2/2),int(3*y1/4+y2/4))
        Y_center=(int(x1/2+x2/2),int(y1/2+y2/2))
        G_center=(int(x1/2+x2/2),int(y1/4+3*y2/4))
        maskR=cv2.circle(copy.deepcopy(mask),R_center,int(d/2),1,-1)
        maskY=cv2.circle(copy.deepcopy(mask),Y_center,int(d/2),1,-1)
        maskG=cv2.circle(copy.deepcopy(mask),G_center,int(d/2),1,-1)
        maskR_gpu=torch.tensor(maskR,device="cuda:0").unsqueeze(2)
        maskY_gpu=torch.tensor(maskY,device="cuda:0").unsqueeze(2)
        maskG_gpu=torch.tensor(maskG,device="cuda:0").unsqueeze(2)
        im_hsv=cv2.cvtColor(im_cpu, cv2.COLOR_RGB2HSV)
        im_hsv_gpu = torch.tensor(im_hsv,device="cuda:0")
        masked_red = im_hsv_gpu*maskR_gpu
        masked_yellow = im_hsv_gpu*maskY_gpu
        masked_green = im_hsv_gpu*maskG_gpu
        value_R=torch.sum(masked_red[:,:,2])/torch.count_nonzero(masked_red[:,:,2])
        value_Y=torch.sum(masked_yellow[:,:,2])/torch.count_nonzero(masked_yellow[:,:,2])
        value_G=torch.sum(masked_green[:,:,2])/torch.count_nonzero(masked_green[:,:,2])
        mean = (value_R+value_Y+value_G)/3
        threshold_perc=0.25
        min= torch.min(torch.tensor([value_R,value_Y,value_G]))
        max= torch.max(torch.tensor([value_R,value_Y,value_G]))
        if (max-min)<30:
            return 'idle'
        threshold=(max-min)*threshold_perc
        # print('red',value_R,'yellow',value_Y,'green',value_G,mean,threshold)
        redOn=(value_R>mean) and (value_R-mean)>threshold
        yellowOn=(value_Y>mean) and (value_Y-mean)>threshold
        greenOn=(value_G>mean) and (value_G-mean)>threshold
        traffic_light_status=[redOn.cpu().numpy(),yellowOn.cpu().numpy(),greenOn.cpu().numpy()]
        colors=['red','yellow','green']
        traffic_light_color=''
        for i in range(len(traffic_light_status)):
            if traffic_light_status[i]:
                traffic_light_color+=colors[i]
                traffic_light_color+=' '
        return traffic_light_color

    @staticmethod
    def check_distance(mask,depth_gpu):
        '''Check the distance to a detect object by masking the depth image with 
           the segmentation mask and computing median value of the masked region.
        
        Args: 
            mask (torch.Tensor): Segmentation mask of one detected object.
            depth_gpu (torch.Tensor): Input depth image.

        Returns:
            torch.Tensor: distance to the detect object.

        '''
        mask=mask.unsqueeze(2)
        isolated_depth = mask*depth_gpu
        # distance = torch.sum(isolated_depth)/torch.count_nonzero(isolated_depth)
        distance = torch.median(isolated_depth[isolated_depth.nonzero(as_tuple=True)])
        return distance
    
    @staticmethod
    def reshape_for_matlab_server(frame):
        '''Reshape image for streaming to MATLAB servers to address aliasing issues.

        '''
        frame=frame.copy()[:,:,[2,1,0]]
        flatten = frame.flatten(order='F').copy() 
        return flatten.reshape(frame.shape,order='C')
    
    def __download_model(self):
        '''Download Quanser's pre-trained YOLOv8s-seg model.

        '''
        url = 'https://quanserinc.box.com/shared/static/ce0gxomeg4b12wlcch9cmlh0376nditf.pt'
        filepath = os.path.splitext(self.defaultPath)[0]+'.pt'
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        print('Downloading yolov8s-seg.pt')
        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            with open(filepath, "wb") as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
        if total_size != 0 and progress_bar.n != total_size:
            raise RuntimeError("Could not download file")

    def __check_path(self, modelPath):
        '''Verify the user specified path to model. If no path is specified, Quanser's
           model will be downloaded and converted to Tensor RT engine if not already
           done. If the user specified a pytorch model, it will be converted to Tensor 
           RT engine in the same directory.
        
        Args: 
            modelPath (str): Path to the user specified model.

        Returns:
            str: Path to the TensorRT engine.

        '''
        if self.convert_tensorrt:
            if modelPath:

                enginePath = os.path.splitext(modelPath)[0]+'.engine'
                if os.path.exists(enginePath):
                    return enginePath
                
                if os.path.splitext(modelPath)[1] != '.engine':
                    try:
                        enginePath = self.convert_to_trt(path = modelPath,
                                                        imageWidth = self.imageWidth,
                                                        imageHeight = self.imageHeight)
                    except:
                        errorMsg = modelPath + ' does not exist, or is in unsupported formats.'
                        raise SystemExit(errorMsg) 
                else:
                    enginePath = modelPath
            else: 
                if not os.path.exists(self.defaultPath):
                    ptPath = os.path.splitext(self.defaultPath)[0]+'.pt'
                    if not os.path.exists(ptPath):
                        self.__download_model()
                    enginePath = self.convert_to_trt(path = ptPath,
                                                    imageWidth = self.imageWidth,
                                                    imageHeight = self.imageHeight)
                else:
                    enginePath = self.defaultPath
            return enginePath
        
        else:
            if modelPath:
                return modelPath
            else:
                self.defaultPath = os.path.splitext(self.defaultPath)[0]+'.pt'
                if not os.path.exists(self.defaultPath):
                    self.__download_model()
                return self.defaultPath