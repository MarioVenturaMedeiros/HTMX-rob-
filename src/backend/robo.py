import pydobot

class InteliArm(pydobot.Dobot):

    def __init__(self, port=None, verbose=False):
        self.verbose = verbose
        self.port = port
        self.is_connected = False  # Track connection status

    def conectar_porta(self, port):
        if self.is_connected:
            print(f"Already connected to {self.port}")
            return True
        try:
            super().__init__(port=port, verbose=self.verbose)
            self.is_connected = True
            print(f"Connected to {port}")
            return True
        except Exception as e:
            print(f"Failed to connect to port {port}: {e}")
            return False

    def movej_to(self, x, y, z, r, wait=True):
        if not self.is_connected:
            print("Not connected to any port.")
            return False
        try:
            super()._set_ptp_cmd(x, y, z, r, mode=pydobot.enums.PTPMode.MOVJ_XYZ, wait=wait)
            return True
        except Exception as e:
            print(f"Error during movej_to: {e}")
            return False
