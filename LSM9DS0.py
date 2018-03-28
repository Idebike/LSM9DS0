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

# Arrays for the 3 axis orientation (pitch, roll, yaw).

oriX = []
oriY = []
oriZ = []

accX = []
accY = []
accZ = []

magX = []
magY = []
magZ = []

# Processing.
for i in range (10):

    oriX.append(readGYRx())
    oriY.append(readGYRy())
    oriZ.append(readGYRz())

    accX.append(readACCx())
    accY.append(readACCy())
    accZ.append(readACCz())

    magX.append(readMAGx())
    magY.append(readMAGy())
    magZ.append(readMAGz())

    time.sleep(1)

# Converting the values.
for i in range (10):

    oriX[i] = oriX[i] * 0.070
    oriY[i] = oriY[i] * 0.070
    oriZ[i] = oriZ[i] * 0.070

    accX[i] = accX[i] * 0.732
    accY[i] = accY[i] * 0.732
    accZ[i] = accZ[i] * 0.732

    magX[i] = magX[i] * 0.48
    magY[i] = magY[i] * 0.48
    magZ[i] = magZ[i] * 0.48


for i in range (10):

    oriX[i] = round(oriX[i], 1)
    oriY[i] = round(oriY[i], 1)
    oriZ[i] = round(oriZ[i], 1)

    print "X-Axis of Rotation : %d" %oriX[i]
    print "Y-Axis of Rotation : %d" %oriY[i]
    print "Z-Axis of Rotation : %d\n" %oriZ[i]

    print "Acceleration X : %d" %accX[i]
    print "Acceleration Y : %d" %accY[i]
    print "Acceleration Z : %d\n" %accZ[i]

    print "Magnetometre X : %d" %magX[i]
    print "Magnetometre Y : %d" %magY[i]
    print "Magnetometre Z : %d\n" %magZ[i]

# the name of the file where the values will be written.
#filename = "LSM9DS0.csv"

#file = open(filename, 'w')

#file.write(["oriX","oriY","oriZ","accX","accY","accZ","magX","magY","magZ"])

#for i in range(10):

 #   file.write(str(oriX[i]) + ';' + str(oriY[i]) + ';' + str(oriZ[i]) +';\n' + str(accX[i]) +';' + str(accY[i]) + ';' + str(accZ[i]) + ';\n' + str(magX[i]) + ';' + str(magY[i]) + ';' + str(magZ[i]) + ';\n')

 #   file.close()

now = time.strftime('%d-%m-%Y %H:%M:%S')
with open('LSM9DS0data%s.csv' %now, 'a') as LSM9DS0:
	filewriter = csv.writer(LSM9DS0, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	filewriter.writerow(['oriX', 'oriY', 'oriZ', 'accX', 'accY', 'accZ', 'magX', 'magY', 'magZ'])

	for i in range (10):
 		oriX[i] = readGYRx()
		now = time.strftime('%d-%m-%Y %H:%M:%S')
		filewriter.writerow([now, oriX[i]])
		time.sleep(1)
