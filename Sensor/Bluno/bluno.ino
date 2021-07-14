#include "I2Cdev.h"
#include "MPU6050.h"

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

#define SAMPLING_RATE 50



MPU6050 accelgyro;
int16_t ax, ay, az;
int16_t gx, gy, gz;
long previousSensorDetectedTime;
long currentTime,timeDiff;

void setoffsets(){
//      X Accel  Y Accel  Z Accel   X Gyro   Y Gyro   Z Gyro
//    int offsets[] = {-5046,    -768,     -48,     220,     -59,       6}; //dev3
//    int offsets[] = {-6288,     624,    1414,      60,     -10,       4};//dev2
    int offsets[] = {-1482,    1156,    1398,      26,     -26,      42}; //dev1

    
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
  //1 Bytes
  sendHeader();
  //6 bytes
  Serial.write((int8_t)((int16_t)ax >> 8));
  Serial.write((int8_t)((int16_t)ay >> 8));
  Serial.write((int8_t)((int16_t)az >> 8));
  Serial.write((int8_t)((int16_t)gx >> 8));
  Serial.write((int8_t)((int16_t)gy >> 8));
  Serial.write((int8_t)((int16_t)gz >> 8));
}

void printData(){
  //1 Bytes
//  sendHeader();
  //6 bytes
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
  
  Serial.print(ax); Serial.print("\t");
  Serial.print(ay); Serial.print("\t");
  Serial.print(az); Serial.print("\t");
  Serial.print(gx); Serial.print("\t");
  Serial.print(gy); Serial.print("\t");
  Serial.println(gz);
  
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



int calculateRMS(){
  float sum = 0;
  for(rms_I = 0; rms_I < numSamples; rms_I++ ){
    sum+= pow(myoware[rms_I],2);
  }
  float result  = pow(sum/numSamples, 0.5) * 100;
  return result;
}

int calculateMAV(){
  float sum = 0;
  for(rms_I = 0; rms_I <numSamples; rms_I++ ){
    sum+= abs(myoware[rms_I]);
  }
  float result  = (sum/numSamples ) * 100;
  return result ;
}

int calculateZeroCross(){
  
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
  float result  = cross *100;
  return result;
}

void sendHeaderMyoware(){
  //1 Bytes
  Serial.write((uint8_t) 2 );
  
}

void sendMyoware(){
  sendHeaderMyoware();
  
  Serial.write((char*)&RMS, sizeof(RMS));
  Serial.write((char*)&MAV, sizeof(MAV));
  Serial.write((char*)&ZCS, sizeof(ZCS));


  
//  Serial.print(RMS); Serial.print("\t");
//  Serial.print(MAV); Serial.print("\t");
//  Serial.print(ZCS); Serial.println();
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
    Serial.begin(115200);               //initial the Serial
    while(!Serial);

  //Sensor Init
    accelgyro.initialize();
    setoffsets();
    setFilters();
    initMyoware();
    previousSensorDetectedTime = millis();
    
}


void loop()
{ 
  currentTime = millis();
  timeDiff = currentTime - previousSensorDetectedTime2;

  if(currentTime - previousSensorDetectedTime2 > fastsample){
    analogPlaceholder = analogRead(A3);
    moving_average = 0.9 * moving_average + 0.1*analogPlaceholder;
    if (sampleI > numSamples ||sampleI < 0 ){
      sampleI=0;
    }
    myoware[sampleI] = analogPlaceholder-moving_average;
//    Serial.println(myoware[sampleI]);
    
    sampleI+=1;
    if (sampleI==halfNumSamples){
      RMS = calculateRMS();
      MAV = calculateMAV();
      ZCS = calculateZeroCross();
      sendMyoware();
//      send_for_serial(2);
    } else if (sampleI > numSamples){
      RMS = calculateRMS();
      MAV = calculateMAV();
      ZCS = calculateZeroCross();
      sendMyoware();
//      send_for_serial(2);
    }

    previousSensorDetectedTime2 = currentTime;

  }

  
  if(currentTime - previousSensorDetectedTime < SAMPLING_RATE){
    return;
  }
  
  previousSensorDetectedTime = currentTime;
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  sendData();
//  send_for_serial(1);

  
}  
