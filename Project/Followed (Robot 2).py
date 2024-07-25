import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import turtlesim.srv
import numpy as np
import random
import json


with open('Project.json') as f:
    veri = json.load(f)

pose = Pose()
poseflag = False
random_secimi= None

def callback(veri):
    global pose
    global poseflag
    pose = veri
    poseflag = True
   
def move_turtlebot2(speed,angle_speed):
    
    while poseflag == False: 
        rospy.sleep(0.01)

    vel_msg = Twist()   
    while True:
        
        vel_msg.linear.x= speed
        vel_pub.publish(vel_msg)
        rospy.sleep(1)

        secim(angle_speed)

        loop_rate.sleep()  
        
def secim(angle_speed):
    
    random_secimi =random.choice([0,1])
    print(random_secimi)
    if random_secimi == 0:
        direct_kontrol(angle_speed)
    elif random_secimi == 1:
        rastgele_kontrol()

def rotate(angle_speed,thetta):
    
    vel_msg = Twist()
    while True:
        diff=abs(pose.theta - thetta)
        
        if diff > 0.1:
            vel_msg.angular.z = angle_speed
            vel_pub.publish(vel_msg)
        else:
            vel_msg.angular.z = 0
            vel_pub.publish(vel_msg)
            break
            
def rastgele_kontrol():
    
    sol = pose.x < 0.1
    sag = pose.x > 11
    ust = pose.y > 11
    alt = pose.y < 0.1
    
    if sol or sag or ust or alt:
        random_turn_angular = random.uniform(-np.pi,np.pi)
        rotate(veri[1]["Acisal_hiz"],random_turn_angular)
    else:
         move_turtlebot2(veri[1]["Dogrusal_hiz"],veri[1]["Acisal_hiz"])
        
def direct_kontrol(angle_speed):
    while not poseflag:
        rospy.sleep(0.01)
        
    thetta = -pose.theta  
    if pose.x < 0.1:
        if pose.theta > 0:
            thetta = np.pi - pose.theta
            rotate(angle_speed, thetta)
        else:
            thetta = -np.pi - pose.theta
            rotate(angle_speed, thetta)
    elif pose.x > 11:
        if pose.theta > 0:
            thetta = np.pi - pose.theta
            rotate(angle_speed, thetta)
        else:
            thetta = -np.pi - pose.theta
            rotate(angle_speed, thetta)
    elif pose.y > 11 or pose.y < 0.1:
        thetta = -pose.theta
        rotate(angle_speed, thetta)


if __name__=='__main__':
    rospy.init_node('robot2',anonymous=True)  
    rospy.Subscriber('/turtle2/pose',Pose,callback,) 
    vel_pub = rospy.Publisher('/turtle2/cmd_vel',Twist,queue_size=5)
    
    loop_rate = rospy.Rate(5)

    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy("spawn", turtlesim.srv.Spawn)
    spawner(random.randint(1,10),random.randint(1,10),random.uniform(-3.14,3.14),'turtle2')
    
    rospy.wait_for_service('kill')
    killer = rospy.ServiceProxy("kill",turtlesim.srv.Kill)
    killer('turtle1')
    
    move_turtlebot2(veri[1]["Dogrusal_hiz"],veri[1]["Acisal_hiz"])
    rospy.spin()
