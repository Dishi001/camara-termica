#include <Wire.h>
 #include <Adafruit_MLX90640.h> 
 
 Adafruit_MLX90640 mlx; 
 float frame[32*24]; 

 void setup() { Serial.begin(115200);
  while(!Serial) delay(10); 
  Serial.println("Iniciando..."); 
  
  Wire.begin(4, 5);
  Wire.setClock(400000);
  
  if(!mlx.begin(MLX90640_I2CADDR_DEFAULT, &Wire)) {
     Serial.println("MLX90640 no encontrado!"); 
     while(1) delay(10); 
     } 
  
    Serial.println("MLX90640 detectado!"); 
    mlx.setMode(MLX90640_CHESS);
    mlx.setResolution(MLX90640_ADC_18BIT);
    mlx.setRefreshRate(MLX90640_2_HZ); 
  } 
  
  void loop() { 
    if(mlx.getFrame(frame) != 0)
     { Serial.println("Error leyendo frame");
      delay(500); 
      return; 
      } 
    
    // Imprimir matriz 32x24 solo con números 
    for(uint8_t h=0; h<24; h++) { 
      for(uint8_t w=0; w<32; w++) { 
        Serial.print(frame[h*32 + w], 1); // un decimal 
        Serial.print(" "); // separa con espacio 
      } 
      Serial.println(); // nueva línea por cada fila 
    } 
    
    Serial.println("==="); // indica fin de frame 
    delay(500); // medio segundo entre frames 
  }