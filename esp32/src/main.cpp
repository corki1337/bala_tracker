#include <Arduino.h>
#include <micro_ros_platformio.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <geometry_msgs/msg/point.h>
#include <ESP32Servo.h>



rcl_subscription_t subscriber;
geometry_msgs__msg__Point msg;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

Servo serwodolne, serwogorne;
int dolnePin = 15;
int gornePin = 16;


void subscription_callback(const void* msgin){

    const geometry_msgs__msg__Point* received_msg = (const geometry_msgs__msg__Point *)msgin;
    float x = received_msg ->x;
    float y = received_msg ->y;


    int xwsp = int(map(x,1,1280,132,87));
    int ywsp = int(map(y,1, 720, 72, 108));
    serwodolne.write(xwsp);
    serwogorne.write(ywsp);

}

void setup(){
    Serial.begin(115200);
    set_microros_serial_transports(Serial);
    allocator = rcl_get_default_allocator();


    while (rclc_support_init(&support, 0, NULL, &allocator) != RCL_RET_OK) {
        delay(100);
    }


    //servos
    ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
    serwodolne.setPeriodHertz(50);
    serwogorne.setPeriodHertz(50);
    serwodolne.attach(dolnePin, 500, 2400);
    serwogorne.attach(gornePin, 500, 2400);
    //serwogorne.write()
    serwodolne.write(100);


    rclc_node_init_default(&node, "esp32_node", "", &support);

    rclc_subscription_init_default(
        &subscriber,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Point),
        "kordy"
    );


    rclc_executor_init(&executor, &support.context, 1, &allocator);
    rclc_executor_add_subscription(&executor, &subscriber, &msg, &subscription_callback, ON_NEW_DATA);
}

void loop(){
    rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
    delay(10);
}


