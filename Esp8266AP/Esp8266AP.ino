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
  myStepper(int *p, char *cs[4])
  {
    pins = p;
    codes = cs;
    phase = 0;
    dir = 1;
    pinNum = 3;
    rot = 512;
  };

  void step()
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
    dir = direct;
    deg = rot * deg;
    phase = 0;
    while (deg > 0)
    {
      step();
      deg--;
      delay(3);
    }
  };

private:
  int pinNum;
  int *pins;
  char **codes;
  // 当前高电平所在的相位
  int phase;
  // 电机旋转得方向
  int dir;
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
myStepper Down(GROUP_3, P1);

/* Set these to your desired credentials. */
const char *ssid = APSSID;
const char *password = APPSK;

ESP8266WebServer server(80);

void initPins()
{
  for (int i = 0; i < 9; i++)
    pinMode(PINS[i], OUTPUT);
}

void act(char face, char deg)
{
  Serial.print(face);
  Serial.print(" - ");
  Serial.println(deg);
  switch (face)
  {
  case 'L':
    Left.rotate(1, -1);
    break;

  case 'R':
    Right.rotate(1, -1);
    break;

  case 'F':
    Front.rotate(1, -1);
    break;

  case 'B':
    Back.rotate(1, -1);
    break;

  default:
    break;
  }
}

void analyse(char *command)
{
  act(command[0], command[1]);
  char *next = strchr(command, ',');
  while (next != 0)
  {
    Serial.print(" | ");
    ++next;
    act(next[0], next[1]);
    next = strchr(next, ',');
  }
  Serial.println();
}

void onIndex()
{
  Serial.println("/");
  server.send(200, "text/html", "<h1>You are connected</h1>");
}

void onWait()
{
  Serial.println("/wait");
  int waitTime = 2000;
  if (server.hasArg("time"))
  {
    waitTime = atoi(server.arg("time").c_str());
  }
  delay(waitTime);
  server.send(200, "text/html", "<h1>waited " + String(waitTime) + " ms</h1>");
}

void onAction()
{
  Serial.println("/action");
  if (server.hasArg("action"))
  {
    String s_action = server.arg("action");
    char *command = new char[s_action.length() + 1];
    s_action.toCharArray(command, s_action.length() + 1);
    analyse(command);
  }
  server.send(200, "text/plain", "message"); //Response to the HTTP request
}

void onRestore()
{
  Serial.println("/restore");
  if (server.hasArg("ins"))
  {
    String s_actions = server.arg("ins");

    char *c_actions = new char[s_actions.length() + 1];
    s_actions.toCharArray(c_actions, s_actions.length() + 1);

    char *command = strtok(c_actions, " ");
    while (command != 0)
    {
      analyse(command);
      command = strtok(0, " ");
    }
  }
  server.send(200, "text/plain", "message"); //Response to the HTTP request
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
  server.on("/wait", onWait);
  server.on("/action", onAction);
  server.on("/restore", onRestore);
  server.begin();
  Serial.println("HTTP server started");
}

void loop()
{
  server.handleClient();
}