bool isOnSeven = false;
bool isOnSix = false;
bool isOnFive = false;
bool isOnFour = false;

int incomingOrder = 0;

void setup() {
	// Open connection.
	Serial.begin(9600);
	// Setup pins for output.
	pinMode(7, OUTPUT);
	pinMode(6, OUTPUT);
	pinMode(5, OUTPUT);
	pinMode(4, OUTPUT);

	// Let python know we're ready.
	Serial.write('1');
}


void loop() {
	incomingOrder = 0;
	if (Serial.available() > 0) {
		incomingOrder = Serial.read();
		if (incomingOrder == 7) {
			if (isOnSeven) {
				isOnSeven = false;
				digitalWrite(7, LOW);
			} else {
				isOnSeven = true;
				digitalWrite(7, HIGH);
			}
		} else if (incomingOrder == 6) {
			if (isOnSix) {
				isOnSix = false;
				digitalWrite(6, LOW);
			} else {
				isOnSix = true;
				digitalWrite(6, HIGH);
			}
		}  else if (incomingOrder == 5) {
			if (isOnFive) {
				isOnFive = false;
				digitalWrite(5, LOW);
			} else {
				isOnFive = true;
				digitalWrite(5, HIGH);
			}
		}  else if (incomingOrder == 4) {
			if (isOnFour) {
				isOnFour = false;
				digitalWrite(4, LOW);
			} else {
				isOnFour = true;
				digitalWrite(4, HIGH);
			}
		}
	}
}