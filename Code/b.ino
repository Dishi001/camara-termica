#include <Wire.h>
#include <Adafruit_MLX90640.h>
#include <ESP8266WiFi.h>

Adafruit_MLX90640 mlx;
float frame[32*24];

// Configuración WiFi
const char* ssid = "Maximo";
const char* password = "gmcg1546";

WiFiServer server(1234); // puerto TCP

void setup() {
  Serial.begin(500000);
  Wire.begin(4, 5);
  Wire.setClock(400000);

  Serial.println("Conectando a WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado!");
  Serial.print("IP del servidor: ");
  Serial.println(WiFi.localIP());

  server.begin();

  if(!mlx.begin(MLX90640_I2CADDR_DEFAULT, &Wire)) {
    Serial.println("MLX90640 no encontrado!");
    while(1) delay(10);
  }

  mlx.setMode(MLX90640_CHESS);
  mlx.setResolution(MLX90640_ADC_18BIT);
  mlx.setRefreshRate(MLX90640_16_HZ);
}

void loop() {
  WiFiClient client = server.available();
  if (!client) return;

  if (mlx.getFrame(frame) != 0) return;

  // Enviar toda la matriz en formato CSV
  for (uint8_t h = 0; h < 24; h++) {
    for (uint8_t w = 0; w < 32; w++) {
      client.print(frame[h * 32 + w], 1);
      if (w < 31) client.print(",");
    }
    client.println();
  }
  client.println("===");  // fin de frame
}
