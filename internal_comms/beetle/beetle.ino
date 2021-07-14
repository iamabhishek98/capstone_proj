#include <CRCx.h>
#include "Queue.h"
#include "I2Cdev.h"
#include "MPU6050.h"
#include "TrueRMS.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

#define SAMPLING_RATE 100
#define BAUD_RATE 115200
#define HANDSHAKE 'H'
#define ACK 'A'
#define DATA 'D'
#define RESET 'R'
#define DELAY 60

class SensorData {
  public:
    void populate(float accX, float accY, float accZ, float gyroX, float gyroY, float gyroZ);
    float accX;
    float accY;
    float accZ;
    float gyroX;
    float gyroY;
    float gyroZ;
};

void SensorData::populate(float accX, float accY, float accZ, float gyroX, float gyroY, float gyroZ) {
  this->accX = accX;
  this->accY = accY;
  this->accZ = accZ;
  this->gyroX = gyroX;
  this->gyroY = gyroY;
  this->gyroZ = gyroZ;
}

unsigned long start_time = 0;
boolean handshake = false;
boolean handshake_confirmed = false;
Queue<SensorData> sensorData(5);

void(* resetBeetle) (void) = 0;

int computeChecksum(int chksum, char arr[]) {
  for (int i = 0; i < strlen(arr); i++) {
        chksum ^= arr[i];
  }
  return chksum;
}

int writeDataBuffer(float data, char delimiter, int chksum) {
  char datastring[7];
  itoa(int(data),datastring,10);
  Serial.print(datastring);
  chksum = computeChecksum(chksum,datastring);
  Serial.print(delimiter);
  chksum ^= delimiter;
  return chksum;
}

MPU6050 accelgyro;
int16_t ax, ay, az;
int16_t gx, gy, gz;
long previousSensorDetectedTime;
long currentTime,timeDiff;

void setoffsets(){
//      X Accel  Y Accel  Z Accel   X Gyro   Y Gyro   Z Gyro
    int offsets[] = {-5046,    -768,     -48,     220,     -59,       6}; //dev3
//    int offsets[] = {-6288,     624,    1414,      60,     -10,       4};//dev2
//    int offsets[] = {-1482,    1156,    1398,      26,     -26,      42}; //dev1

    
    accelgyro.setXAccelOffset(offsets[0]);
    accelgyro.setYAccelOffset(offsets[1]);
    accelgyro.setZAccelOffset(offsets[2]);
    accelgyro.setXGyroOffset(offsets[3]);
    accelgyro.setYGyroOffset(offsets[4]);
    accelgyro.setZGyroOffset(offsets[5]);
}

void setFilters(){
  accelgyro.setDLPFMode(MPU6050_DLPF_BW_5);
}

void sendHeader(){
  //1 Bytes
  Serial.write((uint8_t) 1 );
  
}

void sendData(){
  unsigned long actual_time = millis() - start_time;
  int8_t chksum = 0;


  // packet code
  Serial.write(DATA);
  
  // accelerometer data
  Serial.write((int8_t)((int16_t) ax >> 8));
  Serial.write((int8_t)((int16_t) ay >> 8));
  Serial.write((int8_t)((int16_t) az >> 8));
  
 // gyroscope data
  Serial.write((int8_t)((int16_t) gx >> 8));
  Serial.write((int8_t)((int16_t) gy >> 8));
  Serial.write((int8_t)((int16_t) gz >> 8));
  
  // timestamp
  byte timestamp[4];
  timestamp[0] = (actual_time >> 24);
  timestamp[1] = (actual_time >> 16);
  timestamp[2] = (actual_time >> 8);
  timestamp[3] = actual_time;
  Serial.write(timestamp, sizeof(timestamp));
  
  // checksum
  Serial.write((int8_t) chksum);
}

const int numSamples = 100;
const int halfNumSamples = numSamples/2;
float myoware[100];
int rms_I;

long previousSensorDetectedTime2 = 0;
int fastsample = 2;
int analogPlaceholder;
float moving_average = 0;
unsigned int sampleI = 0;
int RMS;
int MAV;
int ZCS;

float calculateRMS(){
  float sum = 0;
  for(rms_I = 0; rms_I < numSamples; rms_I++ ){
    sum+= pow(myoware[rms_I],2);
  }
  return pow(sum/numSamples, 0.5);
}

float calculateMAV(){
  float sum = 0;
  for(rms_I = 0; rms_I <numSamples; rms_I++ ){
    sum+= abs(myoware[rms_I]);
  }
  return sum/numSamples;
}

float calculateZeroCross(){
  
  float cross = 0;
  int isNextPositive;
  int isPreviousPositive = 0;
  for(rms_I = 1; rms_I <numSamples; rms_I++ ){
    isNextPositive = myoware[rms_I] > 0;
    if (isNextPositive != isPreviousPositive){
      cross++;
    }
    isPreviousPositive = isNextPositive;
  }
  return cross;
}

void sendMyoware(){
  unsigned long actual_time = millis() - start_time;
  
  Serial.write('M');
  
  Serial.write((char*)&RMS, sizeof(RMS));
  Serial.write((char*)&MAV, sizeof(MAV));
  Serial.write((char*)&ZCS, sizeof(ZCS));
  
  byte timestamp[4];
  timestamp[0] = (actual_time >> 24);
  timestamp[1] = (actual_time >> 16);
  timestamp[2] = (actual_time >> 8);
  timestamp[3] = actual_time;
  Serial.write(timestamp, sizeof(timestamp));
  

}

void send_for_serial(int type){
  //1 Bytes
//  sendHeader();
  //6 bytes
  if (type == 1){
      Serial.print("a");
      Serial.print("\t");
      Serial.print((int8_t)((int16_t)ax >> 8));
      Serial.print("\t");
      Serial.print((int8_t)((int16_t)ay >> 8));
      Serial.print("\t");
      Serial.print((int8_t)((int16_t)az >> 8));
      Serial.print("\t");
      Serial.print((int8_t)((int16_t)gx >> 8));
      Serial.print("\t");
      Serial.print((int8_t)((int16_t)gy >> 8));
      Serial.print("\t");
      Serial.print((int8_t)((int16_t)gz >> 8));
      Serial.print("\n");
  } else {
      Serial.print("b"); Serial.print("\t");
      Serial.print(RMS); Serial.print("\t");
      Serial.print(MAV); Serial.print("\t");
      Serial.print(ZCS); Serial.println();
  }

  
  
}

void initMyoware(){
  for(rms_I = 0; rms_I <numSamples; rms_I++ ){
    myoware[rms_I] = 0.0;
  }
}

void setup() {
    //Comms Protocols
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif
    Serial.begin(BAUD_RATE);               //initial the Serial
    while(!Serial);

  //Sensor Init
    accelgyro.initialize();
    setoffsets();
    setFilters();
    initMyoware();
    previousSensorDetectedTime = millis();
  
}

void loop() {
  if (Serial.available()) {
    byte cmd = Serial.read();
    switch (cmd) {
      // receive handshake request -> send ack
      case HANDSHAKE:
        start_time = millis();
        handshake = true;
        handshake_confirmed = false;
        Serial.write(ACK);
        start_time = 0;
        break;

      // receive ack -> if handshake not confirmed, confirm handshake
      case ACK:
        if (handshake) {
          handshake = false;
          handshake_confirmed = true;
        }
        break;

      // reset beetle
      case RESET:
        resetBeetle();
    }
  }
  
  if(handshake_confirmed) {
    currentTime = millis();
  timeDiff = currentTime - previousSensorDetectedTime2;

  if(currentTime - previousSensorDetectedTime2 > fastsample){
    analogPlaceholder = analogRead(A3);
    moving_average = 0.9 * moving_average + 0.1*analogPlaceholder;
    if (sampleI > numSamples ||sampleI < 0 ){
      sampleI=0;
    }
    myoware[sampleI] = analogPlaceholder-moving_average;
    
    sampleI+=1;
    if (sampleI==halfNumSamples){
      RMS = calculateRMS();
      MAV = calculateMAV();
      ZCS = calculateZeroCross();
    } else if (sampleI > numSamples){
      RMS = calculateRMS();
      MAV = calculateMAV();
      ZCS = calculateZeroCross();
    }

    previousSensorDetectedTime2 = currentTime;

  }

  
  if(currentTime - previousSensorDetectedTime < SAMPLING_RATE){
    return;
  }
  
  previousSensorDetectedTime = currentTime;
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  sendData();
  }
}