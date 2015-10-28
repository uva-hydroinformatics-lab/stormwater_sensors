#include <DS1337RTC.h>
#include <Time.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
const int rainGauge = 2;
int rainState = 0; 
volatile int rainCount = 0;
int tempPin = 0;
float tempC;
int reading;
float rainCorrect;
int i = 0;
File tempArchive;
File rainArchive;

void setup() {
  // put your setup code here, to run once:
Serial.begin(38400);
analogReference(INTERNAL);
attachInterrupt(digitalPinToInterrupt(rainGauge),rainGageClick,RISING);
 Serial.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(10)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  }
  Serial.println("card initialized.");
}

void loop() {
  i++;
  reading = analogRead(tempPin);
  tempC = reading/9.31;
  rainCorrect= rainCount/100.0;
  writetoSD(String(tempC), "temp.txt", "temp");
  writetoSD(String(rainCorrect), "rain.txt", "rain");
//  if (i==12){
//    sendSDdata("temp.txt");
//    sendSDdata("rain.txt");
//    i = 0;
//  }
  delay(5000);
 }

void rainGageClick(){
 static unsigned long last_interrupt_time = 0;
 unsigned long interrupt_time = millis();
 // If interrupts come faster than 200ms, assume it's a bounce and ignore
 if (interrupt_time - last_interrupt_time > 200) 
 {
   rainCount++;
 }
 last_interrupt_time = interrupt_time;
}
  

void sendSDdata(String filename){
  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  File dataFile = SD.open(filename);
  File archFile = SD.open("archive/"+filename);

  // if the file is available, write to it:
  if (dataFile) {
    while (dataFile.available()) {
      Serial.write(dataFile.read());
    } 
    dataFile.close();
    SD.remove(filename);
  }
   
  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening datalog.txt");
  }
}

void writetoSD(String dataString, String filename, String param){
  File dataFile = SD.open(filename, FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.println(timestamp()+","+dataString);
    Serial.println(param+","+timestamp()+","+dataString);
    
    // print to the serial port too:
    //Serial.println(dataString);
  }
  dataFile.close();
}

String timestamp(){
  String ts = "";
 // put your main code here, to run repeatedly:
  time_t clock = RTC.get(CLOCK_ADDRESS);
  tmElements_t clockSet;
  breakTime(clock, clockSet);

  //print the time using Time.h
  ts+=(int)clockSet.Day;
  ts+=(" ");
  ts+=((int)clockSet.Month);//monthName[month() - 1]);
  ts+=(" ");
  ts+=((int)(1970+clockSet.Year));//year());
  ts+=(" ");
  ts+=((int)clockSet.Hour);//hour());
  ts+=(":");
  ts+=(clockSet.Minute);//minute());
  ts+=(":");
  ts+=(clockSet.Second);//second());
  return(ts);
}


String printDigits(int digits){
  // utility function for digital clock display: prints preceding colon and leading 0
  Serial.print(":");
  if(digits < 10)
    Serial.print('0');
  return(String(digits));
}

