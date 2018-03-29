import csv
import smbus
import time

bus = smbus.SMBus(1)

bus.write_byte_data(0x6B, 0x20, 0x1F)  #modification du registre de controle 1 pour Gyro
bus.write_byte_data(0x6B, 0x23, 0x30)  #modification du registre de controle 4 pour Gyro

bus.write_byte_data(0x1D, 0x20, 0x67) # registre de controle 1 XM 100Hz
bus.write_byte_data(0x1D, 0x21, 0x20) # registre de controle 2 XM +-16g
bus.write_byte_data(0x1D, 0x24, 0xF0) # registre de controle 5 XM
bus.write_byte_data(0x1D, 0x25, 0x60) # registre de controle 6 XM +-12gauss
bus.write_byte_data(0x1D, 0x26, 0x00) # registre de controle 7 XM

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


# Processing.

while True:

    oriX = 0.070 * readGYRx()
    oriY = 0.070 * readGYRy()
    oriZ = 0.070 * readGYRz()

    accX = 0.732 * readACCx()
    accY = 0.732 * readACCy()
    accZ = 0.732 * readACCz()

    magX = 0.48 * readMAGx()
    magY = 0.48 * readMAGy()
    magZ = 0.48 * readMAGz()

    time.sleep(1)

# Display the values

    print "X-Axis of Rotation : %d" %oriX
    print "Y-Axis of Rotation : %d" %oriY
    print "Z-Axis of Rotation : %d\n" %oriZ

    print "Acceleration X : %d" %accX
    print "Acceleration Y : %d" %accY
    print "Acceleration Z : %d\n" %accZ

    print "Magnetometre X : %d" %magX
    print "Magnetometre Y : %d" %magY
    print "Magnetometre Z : %d\n" %magZ



    now = time.strftime('%d-%m-%Y_%H:%M:%S')
    with open('LSM9DS0data%s.csv' %now, 'a') as LSM9DS0:
        filewriter = csv.writer(LSM9DS0, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	filewriter.writerow(['oriX', 'oriY', 'oriZ', 'accX', 'accY', 'accZ', 'magX', 'magY', 'magZ'])

        while True:
 		oriX = readGYRx()
		oriY = readGYRy()
		oriZ = readGYRz()
		accX = readACCx()
		accY = readACCy()
		accZ = readACCz()
		magX = readMAGx()
		magY = readMAGy()
		magZ = readMAGz()
		now = time.strftime('%d-%m-%Y_%H:%M:%S')
		filewriter.writerow([now,' %d' %oriX,' %d' %oriY,' %d' %oriZ,' %d' %accX,' %d' %accY,' %d' %accZ,' %d' %magX,' %d' %magY,' %d' %magZ])
		time.sleep(1)
