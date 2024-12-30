#define MAX_WORDS 10 // Maximum number of words to split
#define MAX_WORD_LENGTH 20 // Maximum length of each word


#include <Adafruit_Fingerprint.h>
SoftwareSerial mySerial(2, 3);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

void setup() {
  Serial.begin(9600);
  finger.begin(57600);
  finger.LEDcontrol(FINGERPRINT_LED_OFF, 0, 0, 0);
}

void loop() 
{
  String command[MAX_WORDS];
  // put your main code here, to run repeatedly:
  for (int i=1; i<MAX_WORDS; i++)
    command[i] = "0";
    
  ReadCommand(command);
  String ret = "";
  String ret2 = "";
  String ret3 = "";
  
  if (command[0] == "INIT")
    ret = String(finger.verifyPassword());
  else if (command[0] == "LED")
    ret = String(finger.LEDcontrol(command[1].toInt(), command[2].toInt(), command[3].toInt()));
  else if (command[0] == "GETIMAGE")
    ret = String(finger.getImage());
  else if (command[0] == "IMAGE2TZ")
    ret = String(finger.image2Tz(command[1].toInt()));
  else if (command[0] == "CREATEMODEL")
    ret = String(finger.createModel());
  else if (command[0] == "STOREMODEL")
    ret = String(finger.storeModel(command[1].toInt()));
  else if (command[0] == "DELETEMODEL")
    ret = String(finger.deleteModel(command[1].toInt()));
  else if (command[0] == "EMPTYDATABASE")
    ret = String(finger.emptyDatabase());
  else if (command[0] == "FINGERSEARCH")
  {
    ret = String(finger.fingerSearch());
    ret2 = String(finger.fingerID);
    ret3 = String(finger.confidence);
  }

  Serial.println(ret + " " + ret2 + " " + ret3);
}



int ReadCommand(String words[]) 
{
  String command = "";

  while (command == "") {
    while (!Serial.available());
    command = Serial.readStringUntil('\n'); // Reads until newline character or timeout
    command.trim(); // Removes any leading/trailing whitespace or newline
  }

  // Split the command into words
  int wordIndex = 0;
  int startIndex = 0;
  while (startIndex < command.length() && wordIndex < MAX_WORDS) {
    int endIndex = command.indexOf(' ', startIndex); // Find the next space
    if (endIndex == -1) { // No more spaces, take the rest of the string
      endIndex = command.length();
    }
    words[wordIndex] = command.substring(startIndex, endIndex); // Extract the word
    words[wordIndex].trim(); // Remove any extra spaces around the word
    wordIndex++;
    startIndex = endIndex + 1; // Move to the next word
  }

  return wordIndex; // Return the number of words
}
