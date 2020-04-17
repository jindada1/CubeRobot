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

/* Set these to your desired credentials. */
const char *ssid = APSSID;
const char *password = APPSK;

ESP8266WebServer server(80);

void act(char face, char deg)
{
  Serial.print(face);
  Serial.print("-");
  Serial.print(deg);
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
  Serial.println();
  Serial.print("Configuring access point...");
  /* You can remove the password parameter if you want the AP to be open. */
  WiFi.softAP(ssid, password);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("\nAP IP address: ");
  Serial.println(myIP);
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
