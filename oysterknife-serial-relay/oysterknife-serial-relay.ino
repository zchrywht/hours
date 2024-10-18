void setup() {
  Serial.begin(9600);  // Start serial communication at 9600 baud
}

char lastInput = 'O';

void loop() {

  char currentInput = lastInput;
  int analogValue = analogRead(A0);  // Read the analog value from the keypad on pin A0
  int resetValue = analogRead(A2);

  if (analogValue < 60) {
    currentInput = 'R';
  }
  else if (analogValue < 200) {
    currentInput = 'U';
  }
  else if (analogValue < 400) {
    currentInput = 'D';
  }
  else if (analogValue < 600) {
    currentInput = 'L';
  }
  else if (analogValue < 800) {
    currentInput = 'S';
  }
  else if (resetValue == 0) {
    currentInput = 'E';
  }
  else {
    currentInput = 'O';
  }

  if (currentInput != lastInput && currentInput != 'O') {
    Serial.println(currentInput);  // Send the value over the serial port
  }

  lastInput = currentInput;

  delay(100);  // Small delay to avoid flooding the serial port
}
