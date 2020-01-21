#include <stdio.h>

#include <tinkerforge/ip_connection.h>
#include <tinkerforge/brick_imu_v2.h>

#define HOST "localhost"
#define PORT 4223
#define UID "6euhcj" // Change XXYYZZ to the UID of your IMU Brick 2.0

int main(void) {
	// Create IP connection
	IPConnection ipcon;
	ipcon_create(&ipcon);

	// Create device object
	IMUV2 imu;
	imu_v2_create(&imu, UID, &ipcon);

	// Connect to brickd
	if(ipcon_connect(&ipcon, HOST, PORT) < 0) {
		fprintf(stderr, "Could not connect\n");
		return 1;
	}
	// Don't use device before ipcon is connected
	//IMU_V2_SENSOR_FUSION_OFF
	//IMU_V2_SENSOR_FUSION_ON
	imu_v2_set_sensor_fusion_mode(&imu,IMU_V2_SENSOR_FUSION_ON_WITHOUT_MAGNETOMETER);
	//imu_v2_set_sensor_fusion_mode(&imu,IMU_V2_SENSOR_FUSION_OFF);
	//imu_v2_set_sensor_fusion_mode(&imu,IMU_V2_SENSOR_FUSION_ON);
        int16_t x, y, z;
	int16_t h,r,p;
	while(true)
	{	
		imu_v2_get_angular_velocity(&imu, &x, &y, &z);
		printf("x angular velocity: %f\n",x/16.0);
		printf("y angular velocity: %f\n",y/16.0);
		printf("z angular velocity: %f\n",z/16.0);

		imu_v2_get_orientation(&imu,&h,&r,&p);
		printf("h angular: %f\n",h/16.0);
		printf("r angular: %f\n",r/16.0);
		printf("p angular: %f\n",p/16.0);
		sleep(1);
	}
	// Get current quaternion
	//int16_t w, x, y, z;
	//if(imu_v2_get_quaternion(&imu, &w, &x, &y, &z) < 0) {
	//	fprintf(stderr, "Could not get quaternion, probably timeout\n");
	//	return 1;
	//}

	//printf("Quaternion [W]: %f\n", w/16383.0);
	//printf("Quaternion [X]: %f\n", x/16383.0);
	//printf("Quaternion [Y]: %f\n", y/16383.0);
	//printf("Quaternion [Z]: %f\n", z/16383.0);

	printf("Press key to exit\n");
	getchar();
	imu_v2_destroy(&imu);
	ipcon_destroy(&ipcon); // Calls ipcon_disconnect internally
	return 0;
}
