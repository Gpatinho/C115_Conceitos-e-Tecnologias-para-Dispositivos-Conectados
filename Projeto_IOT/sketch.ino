/************************************************
 *  VARAL AUTOMÁTICO COM ESP32 + MQTT + BLYNK
 *  Moisture Sensor → Detecta chuva
 *  LEDs:
 *   Azul (chuva) – GPIO 2
 *   Verde (sol) – GPIO 4
 *   Vermelho (motor em movimento) – GPIO 5
 *   Amarelo (varal recolhido) – GPIO 18
 *   Branco (varal estendido) – GPIO 19
 *  Motor (relé) – GPIO 23
 *  Sensor – GPIO 34 (A0)
 ***********************************************/

#include <WiFi.h>
#include <PubSubClient.h>
#include <BlynkSimpleEsp32.h>

// -----------------------------
// CONFIGURAÇÃO WIFI
// -----------------------------
char ssid[] = "WOKWI-GUEST";  // Troque para seu WiFi real
char pass[] = "";             // senha

// -----------------------------
// CONFIGURAÇÃO BLYNK
// -----------------------------
char auth[] = "SEU_TOKEN_DO_BLYNK";

// -----------------------------
// OLED & Pinos dos LEDs
// -----------------------------
#define LED_AZUL 2
#define LED_VERDE 4
#define LED_VERMELHO 5
#define LED_AMARELO 18
#define LED_BRANCO 19

// Relé
#define PINO_RELE 23

// Sensor de chuva
#define SENSOR_CHUVA 34

// -----------------------------
// MQTT
// -----------------------------
const char* mqtt_server = "test.mosquitto.org";
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;

bool varalRecolhido = false;   // false = estendido, true = recolhido

// ----------------------------------------------------
// FUNÇÃO PARA LIGAR O MOTOR (RECOLHER OU ESTENDER)
// ----------------------------------------------------
void acionarMotor() {
  digitalWrite(LED_VERMELHO, HIGH);   // LED motor ligado
  digitalWrite(PINO_RELE, HIGH);      // Aciona o relé

  delay(3000); // Motor funcionando 3 segundos

  digitalWrite(LED_VERMELHO, LOW);
  digitalWrite(PINO_RELE, LOW);
}

// ----------------------------------------------------
// MQTT CALLBACK
// ----------------------------------------------------
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Mensagem recebida do MQTT: ");
  Serial.println(topic);
}

// ----------------------------------------------------
// CONNECT MQTT
// ----------------------------------------------------
void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT...");
    if (client.connect("ESP32-Varal-Automatico")) {
      Serial.println("Conectado!");
      client.subscribe("varal/status");
    } else {
      Serial.print("Erro, rc=");
      Serial.print(client.state());
      delay(1000);
    }
  }
}

// ----------------------------------------------------
// SETUP
// ----------------------------------------------------
void setup() {
  Serial.begin(115200);

  pinMode(LED_AZUL, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);
  pinMode(LED_AMARELO, OUTPUT);
  pinMode(LED_BRANCO, OUTPUT);
  pinMode(PINO_RELE, OUTPUT);

  digitalWrite(PINO_RELE, LOW);

  // Conectando ao WiFi
  WiFi.begin(ssid, pass);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");

  // MQTT
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // Blynk
  Blynk.begin(auth, ssid, pass);

  // Estado inicial: varal estendido
  varalRecolhido = false;
  digitalWrite(LED_BRANCO, HIGH);
  digitalWrite(LED_AMARELO, LOW);
}

// ----------------------------------------------------
// LOOP PRINCIPAL
// ----------------------------------------------------
void loop() {
  Blynk.run();
  if (!client.connected()) reconnect();
  client.loop();

  int leitura = analogRead(SENSOR_CHUVA);
  Serial.print("Leitura do sensor: ");
  Serial.println(leitura);

  bool chovendo = leitura > 3000;  // Ajuste conforme necessário

  // --------------------------
  // LÓGICA DO CLIMA
  // --------------------------
  if (chovendo) {
    digitalWrite(LED_AZUL, HIGH);
    digitalWrite(LED_VERDE, LOW);

    client.publish("varal/clima", "CHUVA");
    Blynk.virtualWrite(V0, "CHUVA");

    // --- SE CHOVER E O VARAL ESTIVER ESTENDIDO → RECOLHER ---
    if (!varalRecolhido) {
      acionarMotor();
      varalRecolhido = true;

      digitalWrite(LED_AMARELO, HIGH);
      digitalWrite(LED_BRANCO, LOW);

      client.publish("varal/estado", "RECOLHIDO");
      Blynk.virtualWrite(V1, "RECOLHIDO");
    }
  }

  else {  // ENSOLARADO
    digitalWrite(LED_AZUL, LOW);
    digitalWrite(LED_VERDE, HIGH);

    client.publish("varal/clima", "ENSOLARADO");
    Blynk.virtualWrite(V0, "SOL");

    // --- SE FICAR ENSOLARADO E O VARAL ESTIVER RECOLHIDO → ESTENDER ---
    if (varalRecolhido) {
      acionarMotor();
      varalRecolhido = false;

      digitalWrite(LED_AMARELO, LOW);
      digitalWrite(LED_BRANCO, HIGH);

      client.publish("varal/estado", "ESTENDIDO");
      Blynk.virtualWrite(V1, "ESTENDIDO");
    }
  }

  delay(300);
}


