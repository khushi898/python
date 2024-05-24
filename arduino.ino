const char* data[] = {
  "60,98,50,0,Deep Sleep",
  "58,98,45,0,Deep Sleep",
  "55,97,40,0,Light Sleep",
  "54,97,38,0,REM Sleep",
  "56,97,40,0,Light Sleep",
  "57,98,42,0,Light Sleep",
  "60,98,60,100,Awake",
  "72,99,100,800,Awake",
  "75,98,120,1200,Awake",
  "80,98,140,1500,Awake",
  "78,98,130,1400,Awake",
  "76,98,125,1300,Awake",
  "74,98,110,1200,Awake",
  "77,98,135,1400,Awake",
  "79,98,150,1600,Awake",
  "81,98,155,1700,Awake",
  "82,98,160,1800,Awake",
  "78,98,140,1500,Awake",
  "74,98,120,1200,Awake",
  "70,98,100,1000,Awake",
  "68,98,95,800,Awake",
  "66,98,80,500,Awake",
  "64,98,75,200,Light Sleep",
  "62,98,60,0,Deep Sleep"
};

const int dataLength = sizeof(data) / sizeof(data[0]);
int currentIndex = 0;

void setup() {
  serial.begin(9600);
}

void loop() {
  if (currentIndex < dataLength) {
    serial.println(data[currentIndex]);
    currentIndex++;
    delay(1000); // Simulate 1-second intervals
  }
}
