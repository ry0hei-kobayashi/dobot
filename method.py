def get_eio(self, addr):
    return self._get_eio_level(addr)

def set_eio(self, addr, val):
    return self._set_eio_level(addr, val)

def close(self):
    self._on = False
    self.lock.acquire()
    self.ser.close()
    if self.verbose:
        print('pydobot: %s closed' % self.ser.name)
    self.lock.release()

def go(self, x, y, z, r=0.):
    warnings.warn('go() is deprecated, use move_to() instead')
    self.move_to(x, y, z, r)

def move_to(self, x, y, z, r, wait=False):
    self._set_ptp_cmd(x, y, z, r, mode=PTPMode.MOVL_XYZ, wait=wait)

def suck(self, enable):
    self._set_end_effector_suction_cup(enable)

def grip(self, enable):
    self._set_end_effector_gripper(enable)

def speed(self, velocity=100., acceleration=100.):
    self._set_ptp_common_params(velocity, acceleration)
    self._set_ptp_coordinate_params(velocity, acceleration)

def wait(self, ms):
    self._set_wait_cmd(ms)

def pose(self):
    response = self._get_pose()
    x = struct.unpack_from('f', response.params, 0)[0]
    y = struct.unpack_from('f', response.params, 4)[0]
    z = struct.unpack_from('f', response.params, 8)[0]
    r = struct.unpack_from('f', response.params, 12)[0]
    j1 = struct.unpack_from('f', response.params, 16)[0]
    j2 = struct.unpack_from('f', response.params, 20)[0]
    j3 = struct.unpack_from('f', response.params, 24)[0]
    j4 = struct.unpack_from('f', response.params, 28)[0]
    return x, y, z, r, j1, j2, j3, j4
