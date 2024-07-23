void setup() {
Serial.begin(2000000); 

}

void loop() {
 
  if(Serial.available())
  {
    Serial.println(Serial.read());
  }
}
