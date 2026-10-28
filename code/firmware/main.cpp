#include <unistd.h>
#include <cmath>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "esp_err.h"
#include "esp_log.h"
#include "esp_timer.h"

#include "driver/ledc.h"

#include <uros_network_interfaces.h>

#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#include <geometry_msgs/msg/twist.h>

#include <rmw_microros/rmw_microros.h>


namespace
{

// Motor GPIO
#define FR_IN1 26
#define FR_IN2 25
#define FL_IN1 19
#define FL_IN2 27
#define RR_IN1 23
#define RR_IN2 12
#define RL_IN1 0
#define RL_IN2 15


constexpr char TAG[] = "motor_mcu";
constexpr size_t ROS_DOMAIN_ID = 99;


// teleop 실행 시 사용할 최대값과 맞춘다
constexpr float MAX_LINEAR = 0.30f;
constexpr float MAX_ANGULAR = 1.00f;

// PWM 0 ~ 255
constexpr int MOTOR_MAX_PWM = 180;


// 명령이 끊기면 자동 정지
constexpr int64_t CMD_TIMEOUT_US = 1000000;


// LEDC
constexpr ledc_mode_t MOTOR_LEDC_MODE = LEDC_LOW_SPEED_MODE;
constexpr ledc_timer_t MOTOR_LEDC_TIMER = LEDC_TIMER_0;
constexpr ledc_timer_bit_t MOTOR_PWM_RESOLUTION = LEDC_TIMER_8_BIT;
constexpr uint32_t MOTOR_PWM_FREQUENCY = 5000;


constexpr ledc_channel_t FR_IN1_CH = LEDC_CHANNEL_0;
constexpr ledc_channel_t FR_IN2_CH = LEDC_CHANNEL_1;
constexpr ledc_channel_t FL_IN1_CH = LEDC_CHANNEL_2;
constexpr ledc_channel_t FL_IN2_CH = LEDC_CHANNEL_3;
constexpr ledc_channel_t RR_IN1_CH = LEDC_CHANNEL_4;
constexpr ledc_channel_t RR_IN2_CH = LEDC_CHANNEL_5;
constexpr ledc_channel_t RL_IN1_CH = LEDC_CHANNEL_6;
constexpr ledc_channel_t RL_IN2_CH = LEDC_CHANNEL_7;


rcl_subscription_t cmd_vel_subscriber;

geometry_msgs__msg__Twist cmd_vel_message;


int64_t last_cmd_time_us = 0;
bool command_active = false;


#define RCCHECK(fn)                           \
    do {                                      \
        rcl_ret_t rc = (fn);                  \
        if (rc != RCL_RET_OK) {               \
            vTaskDelete(nullptr);             \
        }                                     \
    } while (0)


void set_pwm(ledc_channel_t channel, uint32_t duty) {
    if (duty > 255) {
        duty = 255;
    }

    ESP_ERROR_CHECK(
        ledc_set_duty(
            MOTOR_LEDC_MODE,
            channel,
            duty));

    ESP_ERROR_CHECK(
        ledc_update_duty(
            MOTOR_LEDC_MODE,
            channel));
}


void set_motor(ledc_channel_t in1, ledc_channel_t in2, int speed) {
    set_pwm(in1, 0);
    set_pwm(in2, 0);

    if (speed > 0) {
        set_pwm(in1, static_cast<uint32_t>(speed));
    }
    else if (speed < 0) {
        set_pwm(in2, static_cast<uint32_t>(-speed));
    }
}


void set_left_motors(int speed) {
    set_motor(FL_IN1_CH, FL_IN2_CH, speed);
    set_motor(RL_IN1_CH, RL_IN2_CH, speed);
}


void set_right_motors(int speed) {
    set_motor(FR_IN1_CH, FR_IN2_CH, speed);
    set_motor(RR_IN1_CH, RR_IN2_CH, speed);
}


void drive(int left_speed, int right_speed) {
    set_left_motors(left_speed);
    set_right_motors(right_speed);
}


void stop_motors() {
    drive(0, 0);
}


void motor_init() {
    ledc_timer_config_t timer_config = {};

    timer_config.speed_mode = MOTOR_LEDC_MODE;
    timer_config.timer_num = MOTOR_LEDC_TIMER;
    timer_config.duty_resolution = MOTOR_PWM_RESOLUTION;
    timer_config.freq_hz = MOTOR_PWM_FREQUENCY;
    timer_config.clk_cfg = LEDC_AUTO_CLK;

    ESP_ERROR_CHECK(ledc_timer_config(&timer_config));

    struct MotorChannel {
        int gpio;
        ledc_channel_t channel;
    };


    const MotorChannel motor_channels[] = {
        {FR_IN1, FR_IN1_CH},
        {FR_IN2, FR_IN2_CH},
        {FL_IN1, FL_IN1_CH},
        {FL_IN2, FL_IN2_CH},
        {RR_IN1, RR_IN1_CH},
        {RR_IN2, RR_IN2_CH},
        {RL_IN1, RL_IN1_CH},
        {RL_IN2, RL_IN2_CH}
    };


    for (const auto &motor : motor_channels) {
        ledc_channel_config_t config = {};

        config.gpio_num = motor.gpio;
        config.speed_mode = MOTOR_LEDC_MODE;
        config.channel = motor.channel;
        config.intr_type = LEDC_INTR_DISABLE;
        config.timer_sel = MOTOR_LEDC_TIMER;
        config.duty = 0;
        config.hpoint = 0;

        ESP_ERROR_CHECK(ledc_channel_config(&config));
    }
}


float clamp_unit(float value) {
    if (value > 1.0f) {
        return 1.0f;
    }

    if (value < -1.0f) {
        return -1.0f;
    }

    return value;
}


void cmd_vel_callback(const void *msg_in) {
    if (msg_in == nullptr) {
        return;
    }

    const auto *msg = static_cast<const geometry_msgs__msg__Twist *>(msg_in);

    float linear = clamp_unit(static_cast<float>(msg->linear.x) / MAX_LINEAR);
    float angular = clamp_unit(static_cast<float>(msg->angular.z) / MAX_ANGULAR);

    // differential drive
    float left = linear - angular;
    float right = linear + angular;
    float max_value = std::fmax(1.0f, std::fmax(std::fabs(left), std::fabs(right)));

    left /= max_value;
    right /= max_value;

    int left_pwm =static_cast<int>(left * MOTOR_MAX_PWM);
    int right_pwm =static_cast<int>(right * MOTOR_MAX_PWM);

    drive(left_pwm, right_pwm);

    last_cmd_time_us = esp_timer_get_time();
    command_active = std::fabs(linear) > 0.001f || std::fabs(angular) > 0.001f;

    ESP_LOGI(
        TAG,
        "linear=%.2f angular=%.2f left=%d right=%d",
        msg->linear.x,
        msg->angular.z,
        left_pwm,
        right_pwm);
}


void micro_ros_task(void *argument) {
    (void)argument;

    rcl_allocator_t allocator = rcl_get_default_allocator();
    rcl_init_options_t init_options = rcl_get_zero_initialized_init_options();

    RCCHECK(
        rcl_init_options_init(
            &init_options,
            allocator));

    RCCHECK(
        rcl_init_options_set_domain_id(
            &init_options,
            ROS_DOMAIN_ID));


#ifdef CONFIG_MICRO_ROS_ESP_XRCE_DDS_MIDDLEWARE

    rmw_init_options_t *rmw_options = rcl_init_options_get_rmw_init_options(&init_options);

    RCCHECK(
        rmw_uros_options_set_udp_address(
            CONFIG_MICRO_ROS_AGENT_IP,
            CONFIG_MICRO_ROS_AGENT_PORT,
            rmw_options));

#endif


    rclc_support_t support;


    RCCHECK(
        rclc_support_init_with_options(
            &support,
            0,
            nullptr,
            &init_options,
            &allocator));


    rcl_node_t node;


    RCCHECK(
        rclc_node_init_default(
            &node,
            "motor_mcu",
            "",
            &support));


    RCCHECK(
        rclc_subscription_init_default(
            &cmd_vel_subscriber,
            &node,
            ROSIDL_GET_MSG_TYPE_SUPPORT(
                geometry_msgs,
                msg,
                Twist),
            "cmd_vel"));


    rclc_executor_t executor;


    RCCHECK(
        rclc_executor_init(
            &executor,
            &support.context,
            1,
            &allocator));


    RCCHECK(
        rclc_executor_add_subscription(
            &executor,
            &cmd_vel_subscriber,
            &cmd_vel_message,
            cmd_vel_callback,
            ON_NEW_DATA));


    stop_motors();


    ESP_LOGI(
        TAG,
        "Motor MCU Initialized");


    while (true) {

        rclc_executor_spin_some(&executor, RCL_MS_TO_NS(50));

        if (command_active) {
            int64_t now = esp_timer_get_time();

            if (now - last_cmd_time_us > CMD_TIMEOUT_US) {
                stop_motors();

                command_active = false;

                ESP_LOGW(
                    TAG,
                    "cmd_vel timeout -> STOP");
            }
        }


        usleep(10000);
    }
}

} // namespace


extern "C" void app_main(void)
{
    motor_init();
    stop_motors();
    ESP_ERROR_CHECK(uros_network_interface_initialize());

    xTaskCreate(
        micro_ros_task,
        "micro_ros_task",
        CONFIG_MICRO_ROS_APP_STACK,
        nullptr,
        CONFIG_MICRO_ROS_APP_TASK_PRIO,
        nullptr);
}
