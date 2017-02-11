// PROXY MAGNETOMETER
// spits out com port data like a real mag.
//
int pauseThing = 5000;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  SerialOutput_g857();
}

void SerialOutput_g857()
{
  Serial.println("209 000534?588007");
  delay(pauseThing);
  Serial.println("209 000534?588007");
  delay(pauseThing);
  Serial.println("209 000534?588007");
  delay(pauseThing);
  Serial.println("209 000534?588007");
  delay(pauseThing);
  Serial.println("209 000534?588007");
  delay(pauseThing);
  Serial.println("209 000534?588000");
  delay(pauseThing);
  Serial.println("209 000534 586400");
  delay(pauseThing);
}

void SerialOutput_SAM()
{
  Serial.println("25.08.15 03:19:42: X,10919,Y,-19789,Z,-47587");
  delay(pauseThing);
  Serial.println("25.08.15 03:19:42: X,10919,Y,-19789,Z,-47587");
  delay(pauseThing);
  Serial.println("25.08.15 03:19:42: X,10919,Y,-19789,Z,-47587");
  delay(pauseThing);
  Serial.println("25.08.15 03:19:42: X,1740919,Y,-19789,Z,-47587");
  delay(pauseThing);
  Serial.println("25.08.15~!$@%GSG19:42: X,1091we5r,2435345,^&^%9,Y,-19789,Z,-47587");
  delay(pauseThing);
}


