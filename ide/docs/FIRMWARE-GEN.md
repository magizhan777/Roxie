# Roxie Embedded Studio - Firmware Generation Guide

## Overview

The Firmware Generator is the AI-powered core of Roxie Embedded Studio. It converts:

```
User Intent + Hardware Configuration → AI Processing → Firmware Code
```

## Architecture

### Components

1. **LLM Adapter** - Interfaces with OpenAI API
2. **Code Generator** - Creates C/C++ firmware from templates
3. **Library Resolver** - Resolves dependencies
4. **Validator** - Checks syntax and hardware compatibility

## Firmware Generation Process

### Phase 1: Validation

```
1. Check hardware compatibility
   - Verify all pins exist on selected board
   - Ensure no pin conflicts
   - Validate voltage levels
   - Check reserved pins

2. Resolve component requirements
   - Identify required libraries
   - Check library compatibility
   - Verify pin capabilities (ADC, PWM, GPIO, I2C, SPI)
```

### Phase 2: Library Resolution

```
Libraries needed:
  MQ2 Sensor:
    - MQ2 library v1.0.0
    - Dependencies: None

  OLED Display:
    - Adafruit_SSD1306 v2.5.9
    - Adafruit_GFX v1.11.9 (dependency)

  Buzzer:
    - No external library needed (GPIO control)

Result: [MQ2, Adafruit_SSD1306, Adafruit_GFX]
```

### Phase 3: Code Generation

The LLM receives a structured prompt:

```
Task: Generate embedded firmware for ESP32

Board: ESP32 DevKit V1
- Microcontroller: Xtensa 32-bit
- Flash: 4 MB
- RAM: 520 KB
- Compiler: ESP-IDF or Arduino-ESP32

Components:
1. MQ2 Gas Sensor (Pin 32, ADC)
2. Buzzer (Pin 33, GPIO + PWM)
3. OLED Display (I2C: GPIO21, GPIO22)

Pin Mapping:
- GPIO32: ADC1_0 (MQ2 analog output)
- GPIO33: GPIO + PWM (Buzzer)
- GPIO21: I2C SDA (OLED)
- GPIO22: I2C SCL (OLED)

Requirements:
1. Read gas concentration from MQ2 every second
2. If concentration > 300 ppm, activate buzzer
3. Display real-time readings on OLED
4. Log to Serial Monitor

Libraries to use:
- MQ2
- Adafruit_SSD1306
- Adafruit_GFX
- Wire (I2C)

Generate production-ready C++ firmware with:
- Proper initialization
- Error handling
- Optimized loops
- Comments
- Constant definitions
```

### Phase 4: Code Validation

Generated code is validated for:

1. **Syntax** - Valid C/C++ syntax
2. **Includes** - All required headers present
3. **Pin Usage** - Correct pin assignments
4. **Hardware** - Compatible with board specs
5. **Libraries** - All libraries included

## Example Generated Code

### Input
```
Board: ESP32 DevKit V1
Components:
  - MQ2 Sensor (Pin 32)
  - Buzzer (Pin 33)
  - OLED (I2C)

Intent: "Monitor gas levels and alert when dangerous"
```

### Output

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "MQ2.h"

// Pin Definitions
#define MQ2_PIN 32      // ADC input
#define BUZZER_PIN 33   // PWM output
#define I2C_SDA 21
#define I2C_SCL 22

// Display Setup
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Gas Sensor Setup
MQ2 mq2(MQ2_PIN);

// Configuration
const int DANGEROUS_PPM = 300;
const int READ_INTERVAL = 1000; // ms

unsigned long lastReadTime = 0;
bool alertActive = false;

void setup() {
  Serial.begin(115200);
  
  // Initialize I2C
  Wire.begin(I2C_SDA, I2C_SCL);
  
  // Initialize Display
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("SSD1306 allocation failed");
    while (true);
  }
  display.display();
  delay(2000);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  
  // Initialize Gas Sensor
  mq2.begin();
  
  // Initialize Buzzer
  pinMode(BUZZER_PIN, OUTPUT);
  
  Serial.println("System initialized");
  displayStartupMessage();
}

void loop() {
  unsigned long currentTime = millis();
  
  // Read sensor at fixed interval
  if (currentTime - lastReadTime >= READ_INTERVAL) {
    lastReadTime = currentTime;
    
    // Read gas concentration
    float ppm = mq2.readPPM();
    
    Serial.print("Gas Level: ");
    Serial.print(ppm);
    Serial.println(" ppm");
    
    // Check if dangerous
    if (ppm > DANGEROUS_PPM) {
      activateAlert();
      alertActive = true;
    } else {
      deactivateAlert();
      alertActive = false;
    }
    
    // Update display
    updateDisplay(ppm, alertActive);
  }
}

void activateAlert() {
  // Play alert tone (2 kHz)
  tone(BUZZER_PIN, 2000, 100);
}

void deactivateAlert() {
  noTone(BUZZER_PIN);
}

void updateDisplay(float ppm, bool alert) {
  display.clearDisplay();
  
  // Title
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("GAS MONITOR");
  
  // Gas Level
  display.setTextSize(1);
  display.setCursor(0, 20);
  display.print("Level: ");
  display.print((int)ppm);
  display.println(" ppm");
  
  // Status
  display.setCursor(0, 35);
  if (alert) {
    display.print("Status: DANGEROUS!");
  } else {
    display.print("Status: SAFE");
  }
  
  // Threshold
  display.setCursor(0, 50);
  display.print("Threshold: ");
  display.print(DANGEROUS_PPM);
  display.println(" ppm");
  
  display.display();
}

void displayStartupMessage() {
  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(0, 0);
  display.println("Roxie");
  display.setTextSize(1);
  display.setCursor(0, 30);
  display.println("Gas Detection");
  display.println("System");
  display.setCursor(0, 55);
  display.println("Initializing...");
  display.display();
}
```

## Code Template System

Templates exist for:

1. **Base Template** (`base.cpp`)
   - Setup function
   - Loop function
   - Serial initialization

2. **Sensor Templates** (`sensor_*.cpp`)
   - ADC reading
   - I2C communication
   - Serial protocol

3. **Actuator Templates** (`actuator_*.cpp`)
   - GPIO control
   - PWM signals
   - I2C commands

4. **Protocol Templates** (`protocol_*.cpp`)
   - UART handling
   - I2C communication
   - SPI transaction

## Customization Options

Users can specify:

1. **Read Frequency** - How often to sample sensors
2. **Thresholds** - Trigger values for conditions
3. **Behaviors** - What actuators do when triggered
4. **Logging** - Level of serial output
5. **Optimization** - Power vs. performance

## Library Auto-Selection

The generator automatically includes libraries based on components:

| Component | Required Libraries |
|-----------|-------------------|
| MQ2 Sensor | MQ2 |
| DHT11 | DHT |
| OLED SSD1306 | Adafruit_SSD1306, Adafruit_GFX |
| Servo | Servo |
| I2C Device | Wire |
| SPI Device | SPI |

## Error Handling

Generated code includes:

1. **Sensor Failures** - Check for invalid readings
2. **Communication Errors** - Retry logic
3. **Pin Conflicts** - Caught during validation
4. **Voltage Issues** - Flagged pre-generation

## Performance Optimization

Generated firmware:

1. **Minimizes Interrupts** - Uses polling for simplicity
2. **Efficient Loops** - Fixed-interval reading
3. **Memory Efficient** - Appropriate data types
4. **No Blocking** - Uses millis() for timing

## Future Enhancements

Phase 2:
- Custom ISR generation
- MQTT integration
- WiFi configuration
- Cloud logging

Phase 3:
- Machine learning integration
- Predictive alerts
- Multi-device coordination
- OTA updates

---

For implementation details, see:
- [Architecture](ARCHITECTURE.md)
- [Hardware Specs](HARDWARE.md)
- [API Reference](API.md)
