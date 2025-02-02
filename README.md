
![yolo5](https://user-images.githubusercontent.com/33355278/232350798-3ce7af8c-ab21-402d-beb5-8e931f9d9d4b.jpg)


# Cats and Dogs detection using yolov5 and deployment using REST API (Flask)
![Screenshot 2023-04-17 061324](https://user-images.githubusercontent.com/33355278/232351759-12253d57-61f0-4c2f-bd05-2450684bf371.png)
)



![Screenshot 2023-04-17 060830](https://user-images.githubusercontent.com/33355278/232352004-a08de8c9-57d0-4433-bcf7-b312b5452362.png)
![Screenshot 2023-04-17 060925](https://user-images.githubusercontent.com/33355278/232352007-d0cb8706-22fe-4e6f-be45-35fef1c06f35.png)
![Screenshot 2023-04-17 061512](https://user-images.githubusercontent.com/33355278/232352008-e08a9bba-e441-46b6-8abe-9b1d52d7315e.png)


# Installation


To get started with this project, follow the steps below:

1. Clone the repository to your local machine:


2. Create a virtual environment using `venv` module:
  `py -m venv myenv`

3. Activate the virtual environment:
  `myenv\Scripts\activate`

4. Install the project dependencies:
  `py -m pip install -r requirements.txt`

5. Start the application:
  `py myapp.py --port 5000`
</br> `myapp.json.py` can be used for getting json output 


# Dataset 
The given datasets has 103 images with different types of image extenson like .jpg , .svg, jpeg . So we need to preprocess data properly . We used a python function called `preprocess.py` which performs 
## Checking image format 
## Convert all types of images into .jpg format
## Create new directory 
*-obj/images,
-obj/labels*,

*-test/images,
-test/labels*



## Check annotation 

# Annotation : 
For annotatating I used "labelImg" (https://github.com/heartexlabs/labelImg)

# Model: 
</br>
YOLOv5s (You Only Look Once version 5 small) is a state-of-the-art object detection model s. It is an improvement over previous versions of YOLO, which are known for their speed and accuracy in real-time object detection. YOLOv5s is based on a deep neural network architecture that uses convolutional layers to analyze an image at different scales and extract features that are then used to detect objects in the image.

One of the key advantages of YOLOv5s is its high accuracy in object detection. It achieves state-of-the-art results on several object detection benchmarks while being much faster than other object detection models.


# Training : 
For the first time I used 100 epochs , batch size: 8 and image size  416 . I used rtx 3070 graphics card to train the model .-

`
py train.py --img 416 --batch 8 --epochs 100 --data E:\s1\Job\Final\dataset.yml --weights E:\s1\Job\Final\yolov5-master\yolov5s.pt`
</br> precision : .99
</br>recall .93 
</br> mAP_0.5 : .99 
</br> mAP_0.5:0.95 .76

- But the overall results show  that the model is overfitting , meaning that it is performing well on the training data but may not generalize well to new data. As ephocs number is increasing , we can see that the model performence in training data is increasing but no improvment in testing data . 
- Here is the result 
![results](https://user-images.githubusercontent.com/33355278/232404960-525fb434-1303-4d27-af17-d8cd99f93b73.png)
-For more results 
( https://github.com/sftSalman/cats_and_dogs_detection_Yolov5_RESTAPI_Deployment/tree/main/yolov5-master/runs/train/exp) 

</br> As my model is overfitting thats why I need to take severel steps to ruduce the overfitting . So I take following steps : 
- Reduce epochs
- Increase image size 
- Use augmented data 
- Use early stopping with patience 6 
- </br>
-`py train.py --img 640 --batch 16 --epochs 100 --data E:\s1\Job\Final\dataset.yml --weights E:\s1\Job\Final\yolov5-master\yolov5s.pt--patience 6`

But due to early stopping with patience 6, the model stops learning so quickly. It runs for just 18 epochs so I don't get the satisfactory result   
(https://github.com/sftSalman/cats_and_dogs_detection_Yolov5_RESTAPI_Deployment/tree/main/yolov5-master/runs/train/exp2)
![results](https://user-images.githubusercontent.com/33355278/232408239-bdc34b3b-da00-44e6-887b-8d53778f352d.png)



</br>For the  third time, I use everything the same as before just changed the patience 6 to 10 and increase the epoch to 100 , which means
- image size 640 
- batch 16 
- epoch 100 
- Use augmented data 
- Early stopping with patience 10 



-`py train.py --img 640 --batch 16 --epochs 100 --data E:\s1\Job\Final\dataset.yml --weights E:\s1\Job\Final\yolov5-master\yolov5s.pt --patience 10 ` 

</br>  This time I get a very satisfactory result with no overfitting. It runs for 68 epochs and we get our best result best model in 57 epoch . 
( https://github.com/sftSalman/cats_and_dogs_detection_Yolov5_RESTAPI_Deployment/tree/main/yolov5-master/runs/train/exp3)
-The final results are : 
-</br> precision : .93
</br>recall .99
</br> mAP_0.5 : .99 
</br> mAP_0.5:0.95 .74

</br> Here are all results taken from this training 
![F1_curve](https://user-images.githubusercontent.com/33355278/232432216-a2b130d4-0173-42bc-b276-beddf95587e9.png)

![P_curve](https://user-images.githubusercontent.com/33355278/232432245-afd0d476-ac42-4e3a-a932-c851f3ebd0ee.png)
![R_curve](https://user-images.githubusercontent.com/33355278/232432258-7e74eb36-a56b-48f5-876f-c071826f0d8d.png)
![PR_curve](https://user-images.githubusercontent.com/33355278/232432285-7b15d92d-842a-4c54-b134-2e32774be4c0.png)
![results](https://user-images.githubusercontent.com/33355278/232432312-61b45b96-532d-4d1e-bac7-0450975ed28f.png)



# Testing in real data and Challenges : 


As we know the dataset is very small and it has a lot of duplicated images (the same images with different names) in both the training and test set which leads the data leakage. If a dataset has duplicate images from the training set to the test set, it is called data leakage. Data leakage occurs when information from the training set leaks into the test set, resulting in artificially inflated performance metrics. It can lead to overfitting and make it difficult to accurately evaluate the model's performance on new, unseen data.  That's why, besides having very good evaluation metrics the model may not work accordingly in case of new and unseen data. 
Here is a sample of new and unseen data





# Reference 
## https://github.com/ultralytics/yolov5
## https://github.com/ultralytics/yolov5/tree/master/utils/flask_rest_api


