#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <DHT.h>;

int j=0;
float tempAv =0;
float humAv = 0;
float densityAv = 0;
float gasvalueAv=0;
float bmeTempAv=0;
float bmeHumAv=0;
float bmePressureAv=0;
float bmeGasAv=0;
float tempBME = 0;
float humBME = 0;
float pressureBME = 0;
float gasBME = 0;

#define DHTPIN 2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE);
int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value

const int AOUTpin=1;  //the AOUT pin of the CO sensor goes into analog pin A0 of the arduino
const int DOUTpin=8;  //the DOUT pin of the CO sensor goes into digital pin D8 of the arduino

int limit;
int gasvalue;

#define        COV_RATIO                       0.2            //ug/mmm / mv
#define        NO_DUST_VOLTAGE                 400            //mv
#define        SYS_VOLTAGE                     5000    

const int iled = 7;                                            //drive the led of sensor
const int vout = 0; 

float density, voltage;
int   adcvalue;

/*
private function
*/
int Filter(int m)
{
  static int flag_first = 0, _buff[10], sum;
  const int _buff_max = 10;
  int i;
  
  if(flag_first == 0)
  {
    flag_first = 1;

    for(i = 0, sum = 0; i < _buff_max; i++)
    {
      _buff[i] = m;
      sum += _buff[i];
    }
    return m;
  }
  else
  {
    sum -= _buff[0];
    for(i = 0; i < (_buff_max - 1); i++)
    {
      _buff[i] = _buff[i + 1];
    }
    _buff[9] = m;
    sum += _buff[9];
    
    i = sum / 10.0;
    return i;
  }
}

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME680 bme; // I2C

void setup() {
  Serial.begin(9600);
  pinMode(DOUTpin, INPUT);  //sets the pin as an input to the arduino
  pinMode(iled, OUTPUT);
  digitalWrite(iled, LOW); 

  dht.begin();
  while (!Serial);
  //Serial.println(F("BME680 initialization"));

  if (!bme.begin(0x77)) 
  {
    Serial.println("Could not find a valid BME680 sensor, check wiring!");
    while (1);
  }

  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150); // 320*C for 150 ms

  //Serial.println("Temperature(C),Pressure(hPa),Humidity(%),Gas(KOhms),Altitude(m)");
}

void loop() {
  j++;
  gasvalue= analogRead(AOUTpin);  //reads the analaog value from the CO sensor’s AOUT pin
  limit= digitalRead(DOUTpin); 
  gasvalueAv = gasvalueAv + gasvalue;
  
  digitalWrite(iled, HIGH);
  delayMicroseconds(280);
  adcvalue = analogRead(vout);
  digitalWrite(iled, LOW);
  
  adcvalue = Filter(adcvalue);
  
  /*
  covert voltage (mv)
  */
  voltage = (SYS_VOLTAGE / 1024.0) * adcvalue * 11;
  
  /*
  voltage to density
  */
  if(voltage >= NO_DUST_VOLTAGE)
  {
    voltage -= NO_DUST_VOLTAGE;
    
    density = voltage * COV_RATIO;
  }
  else
    density = 0;

  densityAv = densityAv + density;

  hum = dht.readHumidity();
  humAv = humAv + hum;
  temp= dht.readTemperature();
  tempAv = tempAv + temp;

  if (! bme.performReading()) 
  {
    Serial.println("Failed to perform reading :(");
    return;
  }
  tempBME = bme.temperature;
  bmeTempAv = bmeTempAv + tempBME;
  pressureBME = bme.pressure / 100.0;
  bmePressureAv = bmePressureAv + pressureBME;
  humBME = bme.humidity;
  bmeHumAv = bmeHumAv + humBME;
  gasBME = bme.gas_resistance / 1000.0;
  bmeGasAv = bmeGasAv + gasBME;
  delay(30000);
  if (j==4){
    Serial.print(tempAv/4);
    Serial.print(",");
    Serial.print(humAv/4);
    Serial.print(",");
    Serial.print(densityAv/4);
    Serial.print(",");  
    Serial.print(gasvalueAv/4);  //prints the CO value
    Serial.print(",");
    Serial.print(bmeTempAv/4);
    Serial.print(",");
    Serial.print(bmePressureAv/4);
    Serial.print(",");
    Serial.print(bmeHumAv/4);
    Serial.print(",");
    Serial.print(bmeGasAv/4);
    Serial.println();
    //Serial.print(",");
    //Serial.println(bme.readAltitude(SEALEVELPRESSURE_HPA));
    tempAv = 0;
    humAv = 0;
    densityAv = 0;
    gasvalueAv = 0;
    bmeTempAv = 0;
    bmeHumAv = 0;
    bmePressureAv = 0;
    bmeGasAv = 0;
    j=0;
  }
}