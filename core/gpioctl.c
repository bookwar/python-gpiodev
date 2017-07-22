#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <sys/ioctl.h>

#include "gpioctl.h"


int get_chipinfo(int fd, struct gpiochip_info* info){
  int status;
  status = ioctl(fd, GPIO_GET_CHIPINFO_IOCTL, info);
  return status;
};

int get_lineinfo(int fd, struct gpioline_info *info) {
  int status;

  status = ioctl(fd, GPIO_GET_LINEINFO_IOCTL, info);
  return status;
};

int get_linehandle(int fd, struct gpiohandle_request *req) {
  int status;

  status = ioctl(fd, GPIO_GET_LINEHANDLE_IOCTL, req);
  return status;
};

int get_lineevent(int fd, struct gpioevent_request *req) {
  int status;

  status = ioctl(fd, GPIO_GET_LINEEVENT_IOCTL, req);
  return status;
};

int get_line_values(int fd, struct gpiohandle_data *data) {
  int status;

  status = ioctl(fd, GPIOHANDLE_GET_LINE_VALUES_IOCTL, data);

  return status;
};

int set_line_values(int fd, struct gpiohandle_data *data) {
  int status;

  status = ioctl(fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, data);
  return status;
};
