#include <Adafruit_MLX90614.h>
#include <Servo.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();
Servo servoX;

const int pinServoX = 9;
const int pasosX = 50;
const int anguloMin = 60;
const int anguloMax = 120;

void setup() {
  Serial.begin(9600);
  mlx.begin();
  servoX.attach(pinServoX);
}

void loop() {
  for (int x = 0; x < pasosX; x++) {
    int angX = map(x, 0, pasosX-1, anguloMin, anguloMax);
    servoX.write(angX);
    delay(25);

    float temp = mlx.readObjectTempC();
    Serial.println(temp, 1);
  }
  Serial.println("---Escaneo---");
  delay(500);
}
