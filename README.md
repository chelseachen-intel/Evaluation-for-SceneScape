## Evaluation the performance of the SceneScape using synthetic data

This repo provides an initial benchmark for testing the performance of SceneScape using synthetic data. 

The synthetic data is generated by Unity and then is feed to the tracker system. The predicted trajectory can be obtained from the SceneScape and the ground truth of the position can be obtained from Unity. Mean distance error between the predicted position and ground truth is then calculated. 

### Data generation 

##### Environment set up

Following the [Scalable Virtual Retail Environment repo](https://gitlab.devtools.intel.com/adamcart/virtual-retail-environment) , we can setup the scene for testing the model. For example, a simple scene (a simulated 20 x 10 meters "room")  with one camera and two person is developed.  Using the generated frames , MP4 format video can be obtained using FFMPEG.

<img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/image-20211230145950066.png" alt="image-20211230145950066" style="zoom:50%;">

##### Obtain of the ground truth 

For the position of each person, you can add the following code in the BoundingBoxController.cs, which allows to obtain the screen and world position of each person in each frame in the output Json file. The Wposition means the position in the Unity simulated world, where the unit should be meter.  And the Sposition in pixel level is the position from the camera's point of view.

<img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/image-20211230150816452.png" style="zoom:33%;" />

<img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/image-20211230150922436.png" alt="image-20211230150922436" style="zoom:33%;" />

<img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/image-20211230150857877.png" alt="image-20211230150857877" style="zoom:50%;" />

##### Camera homography 

Four calibration points are needed for camera to map the pixel level point to the meter-level position.

We can set four objects located at the apex of a square.  Using the camera position and the map position of these four calibration points, we can update the scene.json file of the SceneScape, which is used to calculate the camera homography matrix.

### Model testing

For testing the generated video, you can refer to the README in tracker folder of SceneScape. You may have to preprocess the video using percebro and then you can run the tracker. Note that in the SceneScape, all the coordinate origin locate at the top left. But in the Unity Screen Space, the  coordinate origin locate at the bottom left. 

<img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/image-20211230153519207.png" alt="image-20211230153519207" style="zoom:70%;" />

So in the SceneScape/sscape/moving object.py , you should update the code as follows:
<img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/MicrosoftTeams-image (1).png" style="zoom:33%;" />


##### Write predicted data

You can use the following code in SceneScape/tracker/tracker.py to write the predicted position per frame if the track argument is added when you run the tracker. For example:

`tracker/tracker --config  scene.json video.json --track outfile.json`

<img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/MicrosoftTeams-image (2).png" style="zoom:33%;" />

### Results

Some results for reference.

1. #### Simple scene

   

   <img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/L3FrontCam_1.jpg" style="zoom:33%;" />

   When the trajectory of each person is simple, the tracking result can be very accurate as shown in the following figure where the solid line is the ground truth position and the dot line is the predicted position. And the mean distance error for two players are 0.12m and 0.14m respectively.

 
   <img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/F1230_1.png" style="zoom:33%;" />

2. #### Influence of the camera height
The height and view of the camera is essential for the result. In the following scene, the camera is pretty low.
   <center class="half">
   <img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/scene.png" width = "50%" align=left/>
   <img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/L3FrontCam_3.jpg" width = "50%"  align=right />
   </center>

The predicted trajectory of Player-2M has offset with the ground truth. The effects of camera height and view on the performance can be further studied.
<img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/F1230_2.png" style="zoom:33%;" />

3. #### RE-ID issue

   When the trajectory is complex, the global id is unstable for a certain person. For example, the following fours results all have switch ID issue. Note that in this case, the mean distance error is calculated under the situation that the detected global ID and the player-ID is paired manually. The REID module can be further improved.
   <img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/F1229_3.png" style="zoom:33%;" />
   <img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/F1229_4.png" style="zoom:15%;" />
   <img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/F1230_3.png" style="zoom:33%;" />
   <img src="https://github.com/chelseachen-intel/Evaluation-for-SceneScape/blob/main/images/F1230_4.png" style="zoom:33%;" />
