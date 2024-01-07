#define switch 3

String command;

void setup() {
  Serial.begin(9600);
  Serial.println("Type Command (On=on, Off=off)");

  pinMode(switch, OUTPUT);

  delay(1000);
}

void loop() {
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();

    //On
    if (command.equals("on")) {
      digitalWrite(switch, HIGH);
    }

    //Off
    if (command.equals("off")) {
      digitalWrite(switch, LOW);
    }
  }
}