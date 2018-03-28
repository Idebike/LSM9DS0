import smbus
import time

bus = smbus.SMBus(1)

bus.write_byte_data(0x1D, 0x20, 0x67) # registre de controle 1 XM 100Hz
bus.write_byte_data(0x1D, 0x21, 0x20) # registre de controle 2 XM +-16g
bus.write_byte_data(0x1D, 0x24, 0xF0) # registre de controle 5 XM
bus.write_byte_data(0x1D, 0x25, 0x60) # registre de controle 6 XM +-12gauss
bus.write_byte_data(0x1D, 0x26, 0x00) # registre de controle 7 XM


# Calibrating of Accelerometre


def readACCx():
    data0 = bus.read_byte_data(0x1D, 0x28)
    data1 = bus.read_byte_data(0x1D, 0x29)
    ACC_comb = (data0 | data1 >>8)

    return ACC_comb  if ACC_comb < 32768 else ACC_comb - 65536

def readACCy():
    data0 = bus.read_byte_data(0x1D, 0x2A)
    data1 = bus.read_byte_data(0x1D, 0x2B)
    ACC_comb = (data0 | data1 >>8)

    return ACC_comb if ACC_comb < 32768 else ACC_comb - 65536

def readACCz():
    data0 = bus.read_byte_data(0x1D, 0x2C)
    data1 = bus.read_byte_data(0x1D, 0x2D)
    ACC_comb = (data0 | data1 >>8)

    return ACC_comb if ACC_comb < 32768 else ACC_comb - 65536

# Calibrating of Magnetometre

def readMAGx():
    data0 = bus.read_byte_data(0x1D, 0x08)
    data1 = bus.read_byte_data(0x1D, 0x09)
    MAG_comb = (data0 | data1 >>8)

    return MAG_comb if MAG_comb < 32768 else MAG_comb - 65536

def readMAGy():
    data0 = bus.read_byte_data(0x1D, 0x0A)
    data1 = bus.read_byte_data(0x1D, 0x0B)
    MAG_comb = (data0 | data1 >>8)

    return MAG_comb if MAG_comb < 32768 else MAG_comb - 65536

def readMAGz():
    data0 = bus.read_byte_data(0x1D, 0x0C)
    data1 = bus.read_byte_data(0x1D, 0x0D)
    MAG_comb = (data0 | data1 >>8)

    return MAG_comb if MAG_comb < 32768 else MAG_comb - 65536

# Arrays for the 3 axis orientation (pitch, roll, yaw).

accX = []
accY = []
accZ = []

magX = []
magY = []
magZ = []

# Processing.
for i in range (10):

    accX.append(readACCx())
    accY.append(readACCy())
    accZ.append(readACCz())

    magX.append(readMAGx())
    magY.append(readMAGy())
    magZ.append(readMAGz())

    time.sleep(1)
# Converting the values.
for i in range (10):

    accX[i] = accX[i] * 0.732
    accY[i] = accY[i] * 0.732
    accZ[i] = accZ[i] * 0.732

    magX[i] = magX[i] * 0.48
    magY[i] = magY[i] * 0.48
    magZ[i] = magZ[i] * 0.48

    print "Acceleration X : %d" %accX[i]
    print "Acceleration Y : %d" %accY[i]
    print "Acceleration Z : %d" %accZ[i]

    print "Magnetometre X : %d" %magX[i]
    print "Magnetometre Y : %d" %magY[i]
    print "Magnetometre Z : %d" %magZ[i]

