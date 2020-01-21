#include <stdio.h>

// FIXME: This example is incomplete

#include "ip_connection.h"
#include "bricklet_rgb_led_button.h"

#define HOST "localhost"
#define PORT 4223
#define UID "XYZ" // Change XYZ to the UID of your RGB LED Button Bricklet

// Callback function for button state changed callback
void cb_button_state_changed(uint8_t state, void *user_data) {
	(void)user_data; // avoid unused parameter warning

	printf("State: %u\n", state);
}

int main(void) {
	// Create IP connection
	IPConnection ipcon;
	ipcon_create(&ipcon);

	// Create device object
	RGBLEDButton rlb;
	rgb_led_button_create(&rlb, UID, &ipcon);

	// Connect to brickd
	if(ipcon_connect(&ipcon, HOST, PORT) < 0) {
		fprintf(stderr, "Could not connect\n");
		return 1;
	}
	// Don't use device before ipcon is connected

	// Register button state changed callback to function cb_button_state_changed
	rgb_led_button_register_callback(&rlb,
	                                 RGB_LED_BUTTON_CALLBACK_BUTTON_STATE_CHANGED,
	                                 (void *)cb_button_state_changed,
	                                 NULL);

	printf("Press key to exit\n");
	getchar();
	rgb_led_button_destroy(&rlb);
	ipcon_destroy(&ipcon); // Calls ipcon_disconnect internally
	return 0;
}
