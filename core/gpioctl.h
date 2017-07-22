#include <linux/gpio.h>

int get_chipinfo(int fd, struct gpiochip_info* info);

int get_lineinfo(int fd, struct gpioline_info *info);

int get_linehandle(int fd, struct gpiohandle_request *req);

int get_lineevent(int fd, struct gpioevent_request *req);

int get_line_values(int fd, struct gpiohandle_data *data);

int set_line_values(int fd, struct gpiohandle_data *data);
