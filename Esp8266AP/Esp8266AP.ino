/*
   reference:
   1.Getting query parameters
   ->:https://techtutorialsx.com/2016/10/22/esp8266-webserver-getting-query-parameters/
**/

/* Create a WiFi access point and provide a web server on it. */

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#ifndef APSSID
#define APSSID "Rubik-Cube"
#define APPSK "1213141516"
#endif

class myStepper
{
public:
  myStepper(int *p, char *cs[4], int r = 512)
  {
    pins = p;
    codes = cs;
    phase = 0;
    pinNum = 3;
    rot = r;
  };

  void step(int dir)
  {
    for (int i = 0; i < pinNum; i++)
    {
      digitalWrite(pins[i], codes[phase][i] == '1');
    }

    phase += dir;
    // dir == 1
    if (phase > 3)
      phase = 0;
    // dir == -1
    else if (phase < 0)
      phase = 3;
  };

  void rotate(int deg, int direct)
  {
    // phase = 0;
    deg = rot * deg;
    while (deg > 0)
    {
      step(direct);
      deg--;
      delay(3);
    }
  };

  void r_steps(int steps, int direct)
  {
    while (steps > 0)
    {
      step(direct);
      steps--;
      delay(3);
    }
  };

  int rots() { return rot; }

private:
  int pinNum;
  int *pins;
  char **codes;
  // 当前高电平所在的相位
  int phase;
  // 单位角度对应的 step 数，也就是90°对应的step数512
  int rot;
};

/* D0 16, D1 5, D2 4, D3 0, D4 2, D5 14, D6 12, D7 13, D8 15 */
int PINS[9] = {0, 2, 4, 5, 12, 13, 14, 15, 16};
char *P1[4] = {"000", "001", "010", "011"};
char *P2[4] = {"100", "101", "110", "111"};

int GROUP_1[3] = {12, 13, 15};
int GROUP_2[3] = {0, 2, 14};
int GROUP_3[3] = {16, 5, 4};

myStepper Left(GROUP_1, P1);
myStepper Right(GROUP_2, P1);
myStepper Front(GROUP_1, P2);
myStepper Back(GROUP_2, P2);
myStepper Down(GROUP_3, P1, 256);

/* Set these to your desired credentials. */
const char *ssid = APSSID;
const char *password = APPSK;

ESP8266WebServer server(80);

void initPins()
{
  for (int i = 0; i < 9; i++)
    pinMode(PINS[i], OUTPUT);
}

void config(char face, int steps, int clockwise)
{
  switch (face)
  {
  case 'L':
    Left.r_steps(steps, clockwise);
    break;

  case 'R':
    Right.r_steps(steps, clockwise);
    break;

  case 'F':
    Front.r_steps(steps, clockwise);
    break;

  case 'B':
    Back.r_steps(steps, clockwise);
    break;

  case 'D':
    Down.r_steps(steps, clockwise);
    break;

  default:
    break;
  }
}

void flip(myStepper L, myStepper R, int deg, int dir)
{
  int steps = L.rots() * deg;
  while (steps > 0)
  {
    L.step(dir);
    R.step(-dir);
    steps--;
    delay(3);
  }
}

void act(char face, int deg, int clockwise)
{
  switch (face)
  {
  case 'L':
    Left.rotate(deg, clockwise);
    break;

  case 'R':
    Right.rotate(deg, clockwise);
    break;

  case 'F':
    Front.rotate(deg, clockwise);
    break;

  case 'B':
    Back.rotate(deg, clockwise);
    break;

  case 'D':
    Down.rotate(deg, clockwise);
    break;

  case 'H':
    flip(Front, Back, deg, clockwise);
    break;

  case 'V':
    flip(Left, Right, deg, clockwise);
    break;

  default:
    break;
  }
}

void onIndex()
{
  Serial.println("/");
  server.send(200, "text/html", "<h1>You are connected</h1>");
}

void onConfig()
{
  Serial.println("/config");
  if (server.hasArg("steps"))
  {
    char face = (server.arg("face").c_str())[0];
    int steps = atoi(server.arg("steps").c_str());
    int clockwise = atoi(server.arg("clockwise").c_str());
    config(face, steps, clockwise);
  }
  server.send(200, "text/plain", "/config"); //Response to the HTTP request
}

void onAction()
{
  Serial.println("/action");
  if (server.hasArg("deg"))
  {
    char face = (server.arg("face").c_str())[0];
    int deg = atoi(server.arg("deg").c_str());
    int clockwise = atoi(server.arg("clockwise").c_str());
    act(face, deg, clockwise);
  }
  server.send(200, "text/plain", "/action"); //Response to the HTTP request
}

void setup()
{
  delay(1000);
  Serial.begin(115200);
  initPins();
  openWifi();
  setupRouters();
}

void openWifi()
{
  Serial.println("\n Configuring access point...");
  WiFi.softAP(ssid, password);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
}

void setupRouters()
{
  server.on("/", onIndex);
  server.on("/config", onConfig);
  server.on("/action", onAction);
  server.begin();
  Serial.println("HTTP server started");
}

void loop()
{
  server.handleClient();
}
