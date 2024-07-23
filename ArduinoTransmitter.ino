void setup() {

Serial.begin(2000000);
pinMode(1,OUTPUT);
}

void loop() 
{
Serial.write("NOKC");
delayMicroseconds(100);
}

