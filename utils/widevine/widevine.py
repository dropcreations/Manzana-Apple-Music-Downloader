import base64

from utils.widevine.cdm import Device
from utils.widevine.cdm import ContentDecryptionModule

class Widevine:

    WidevineSystemId = [237, 239, 139, 169, 121, 214, 74, 206, 163, 200, 39, 220, 213, 29, 33, 237]

    def __init__(self, init_data, cert_data, device_name, device_path):
        self.initData = init_data
        self.certData = cert_data
        self.deviceName = device_name
        self.devicePath = device_path

        self.cdm = ContentDecryptionModule()

        def checkPssh(b64Pssh):
            pssh = base64.b64decode(b64Pssh)
            if not pssh[12:28] == bytes(self.WidevineSystemId):
                newPssh = bytearray([0, 0, 0])
                newPssh.append(32 + len(pssh))
                newPssh[4:] = bytearray(b'pssh')
                newPssh[8:] = [0, 0, 0, 0]
                newPssh[13:] = self.WidevineSystemId
                newPssh[29:] = [0, 0, 0, 0]
                newPssh[31] = len(pssh)
                newPssh[32:] = pssh

                return base64.b64encode(newPssh)
            else:
                return b64Pssh

        self.session = self.cdm.open(
            checkPssh(self.initData),
            Device(self.deviceName, self.devicePath)
        )

        if self.certData:
            self.cdm.setServiceCertificate(self.session, self.certData)

    def get_keys(self):
        decryptKeys = []

        try:
            for key in self.cdm.getKeys(self.session):
                if key.type == 'CONTENT':
                    decryptKeys.append(
                        '{}:{}'.format(
                            key.kid.hex(),
                            key.key.hex()
                        )
                    )

        except Exception:
            return None
        
        return decryptKeys

    def get_challenge(self): return self.cdm.getLicenseRequest(self.session)
    def update_license(self, b64License): self.cdm.provideLicense(self.session, b64License)