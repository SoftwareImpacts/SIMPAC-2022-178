cmake_minimum_required(VERSION 2.8.3)
project(openai_ros)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

catkin_python_setup()


## Generate messages in the 'msg' folder
add_message_files(
   FILES
   RLExperimentInfo.msg
 )

## Generate added messages and services with any dependencies listed here
generate_messages(
   DEPENDENCIES
   std_msgs
 )

catkin_package(
  DEPENDS message_runtime rospy gazebo_msgs std_msgs geometry_msgs controller_manager_msgs
  # system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
