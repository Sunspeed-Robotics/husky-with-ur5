cmake_minimum_required(VERSION 2.8.3)
project(imu_node)

find_package(catkin REQUIRED COMPONENTS
  diagnostic_msgs
  roscpp
  std_msgs
)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES imu_node
  CATKIN_DEPENDS diagnostic_msgs roscpp std_msgs
  DEPENDS system_lib
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(imu_brick_node src/imu_brick_node.cpp)
target_link_libraries(imu_brick_node ${catkin_LIBRARIES} tinkerforge.so pthread)

install(
    TARGETS
        imu_brick_node
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

install(DIRECTORY launch
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

