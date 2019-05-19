#include <ArduinoJson.h>
int USER_ID = 2;
int getIntData(int min, int max){
  return random(min, max);
}
float getFloatData(int min, int max){
  return random(0, 100)/100.0 + getIntData(min,max);
}
void setup() {
  Serial.begin(9600);
  while (!Serial) continue;
}

void loop() {
  DynamicJsonDocument data(1024);
  int heart_rate_1 = getIntData(60, 170);
  int heart_rate_2 = getIntData(60, 170);
  data["max_heart_rate"] = heart_rate_1 > heart_rate_2 ? heart_rate_1: heart_rate_2;
  data["min_heart_rate"] = heart_rate_1 < heart_rate_2 ? heart_rate_1: heart_rate_2;
  data["glucose_rate"] = getFloatData(2, 8);
  data["protein_rate"] = getIntData(50, 90);
  data["albumin_rate"] = getIntData(10, 60);
  data["myoglobin_rate"] = getIntData(10, 90);
  data["ferritin_rate"] = getIntData(10, 130);
  data["cholesterol_rate"] = getIntData(1, 10);
  data["temperature"] =  getFloatData(34, 43);
  data["user_id"] =  USER_ID;
  serializeJson(data, Serial);
  Serial.println();
  delay(60000);
}
