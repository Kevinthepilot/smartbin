#include "esp_camera.h"
#include <WiFi.h>
#include "camera_pins.h"
#include "key.h"
#include "fb_gfx.h"
#include "esp_http_server.h"



#define CAMERA_MODEL_ESP32S3_EYE

const char ssid[] = SSID;
const char pass[] = PASSWD;



void adjustSettings(){
  sensor_t * s = esp_camera_sensor_get();
  s->set_brightness(s, 1);                  // -2 to 2: Increase to make text stand out
  s->set_contrast(s, 2);                    // -2 to 2: Improve text-background separation
  s->set_saturation(s, 0);                  // -2 to 2: 0 is natural
  s->set_sharpness(s, 2);   
  s->set_vflip(s, 1); 
  s->set_hmirror(s,1) ;             // 0 to 2: Sharper edges for clearer text

  s->set_gainceiling(s, (gainceiling_t)6);  // 0 to 6: Boost sensitivity
  s->set_whitebal(s, 1);                    // Auto white balance
  s->set_awb_gain(s, 1);                    // More accurate white balance
  s->set_exposure_ctrl(s, 1);               // Enable auto exposure
  s->set_aec2(s, 1);                        // Improve low-light exposure
  s->set_ae_level(s, 0);                    // -2 to 2: 0 = neutral exposure

  s->set_special_effect(s, 0);              // 0 = no effect
  s->set_lenc(s, 1);                        // Lens correction (distortion fix)

}

String serverName = "172.20.10.4"; //Change this to match server's local IP
String serverPath = "/upload";
WiFiClient client;
WiFiServer server(80);

void captureImg(){
  camera_fb_t * fb = NULL;
  fb = esp_camera_fb_get();

  if (!fb){
    Serial.println("Camera capture failed");
    return;
  }
  //Connecting to server
  if (client.connect(serverName.c_str(), 8080)){
    String head = "--ESP\r\nContent-Disposition: form-data; name=\"imageFile\"; filename=\"cam.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n";
    String tail = "\r\n--ESP--\r\n";

    uint32_t imageLen = fb->len;
    uint32_t extraLen = head.length() + tail.length();
    uint32_t totalLen = imageLen + extraLen;

    //Printing HTTP headers
    client.println("POST " + serverPath + " HTTP/1.1");
    client.println("Host: " + serverName);
    client.println("Content-Length: " + String(totalLen));
    client.println("Content-Type: multipart/form-data; boundary=ESP");
    client.println();
    client.print(head);

    //Sending image chunks
    uint8_t *fbBuf = fb->buf;
    size_t fbLen = fb->len;
    for (size_t i = 0; i < fbLen; i += 1024) {
      if (i+1024 <= fbLen) {
        client.write(fbBuf, 1024);
        fbBuf += 1024;
      }
      else if (fbLen % 1024 > 0) {
        size_t remainder = fbLen%1024;
        client.write(fbBuf, remainder);
      }
    }   
    client.print(tail);

    client.stop();
  }
  esp_camera_fb_return(fb);
}


void setup() {
  Serial.begin(115200);
  Serial.println("");

  //Camera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 10000000;
  config.frame_size = FRAMESIZE_XGA;
  config.pixel_format = PIXFORMAT_JPEG; // for streaming
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count = 2;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
  Serial.println("Camera initialized successfully!!!");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  WiFi.setSleep(false);

  Serial.print("WiFi connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());
  server.begin();

  adjustSettings();
}

unsigned long lastTime = 0;
void loop() {
  WiFiClient incoming = server.available();
  if (incoming){
    String header = "";
    String currentLine = "";

    while (incoming.connected()){
      if (incoming.available()){
        char c = incoming.read();
        header += c;

        if (c == '\n') {
          if (currentLine.length() == 0) {
            incoming.println("HTTP/1.1 200 OK");
            incoming.println("Content-type:text/html");
            incoming.println("Connection: close");
            incoming.println();
            incoming.println("Trash type received!");

            if (header.indexOf("GET /recycle") >= 0){
              Serial.println("Recycle trash");
            } else if (header.indexOf("GET /non-recycle") >= 0){
              Serial.println("Non Recycle trash");
            } else if (header.indexOf("GET /dangerous") >= 0){
              Serial.println("Dangerous trash");
            }

            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
      }
    }
    delay(10);
    incoming.stop();
  }

  if (millis() - lastTime >= 10000){
      captureImg();
      lastTime = millis();
  }
}


