import smbus
import time

bus = smbus.SMBus(1)
bus.write_byte_data(0x6B, 0x20, 0x1F)  #modification du registre de controle 1 pour Gyro
bus.write_byte_data(0x6B, 0x23, 0x30)  #modification du registre de controle 4 pour Gyro


# time.sleep(0.5)

# Calibrating the gyro
def readGYRx():
    data0 = bus.read_byte_data(0x6B, 0x28)
    data1 = bus.read_byte_data(0x6B, 0x29)
    gyr_combined = (data0 | data1 >>8)

    return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

def readGYRy():
    data0 = bus.read_byte_data(0x6B, 0x2A)
    data1 = bus.read_byte_data(0x6B, 0x2B)
    gyr_combined = (data0 | data1 >>8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536

def readGYRz():
    data0 = bus.read_byte_data(0x6B, 0x2C)
    data1 = bus.read_byte_data(0x6B, 0x2D)
    gyr_combined = (data0 | data1 >>8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536
#Arrays for the 3 axis orientation (pitch, roll, yaw).
oriX = []
oriY = []
oriZ = []

# Processing.
for i in range (10):

    oriX.append(readGYRx())
    oriY.append(readGYRy())
    oriZ.append(readGYRz())
    time.sleep(1)
# Converting the values.
for i in range (10):

    oriX[i] = oriX[i] * 0.070
    oriY[i] = oriY[i] * 0.070
    oriZ[i] = oriZ[i] * 0.070
for i in range (10):
    oriX[i] = round(oriX[i], 1)
    oriY[i] = round(oriY[i], 1)
    oriZ[i] = round(oriZ[i], 1)

    print "X-Axis of Rotation : %d" %oriX[i]
    print "Y-Axis of Rotation : %d" %oriY[i]
    print "Z-Axis of Rotation : %d" %oriZ[i]


