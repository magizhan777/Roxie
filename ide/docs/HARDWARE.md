# Roxie Embedded Studio - Hardware Specifications

## Supported Microcontrollers

### Phase 1 (Current)

#### ESP32 DevKit V1
```
Manufacturer:     Espressif Systems
Core:            Xtensa 32-bit LX6 (dual-core)
Clock Speed:     240 MHz
Flash Memory:    4 MB
RAM:             520 KB (SRAM)
Voltage:         3.3V
GPIO Pins:       38
ADC Channels:    18 (ADC1: 8-channel, ADC2: 10-channel)
PWM Channels:    16
UART Ports:      3
SPI Ports:       4
I2C Ports:       2
DAC:             2 channels
Features:        WiFi 802.11b/g/n, Bluetooth, BLE
```

**Pin Configuration:**
| Pin | Function | Notes |
|-----|----------|-------|
| GPIO0 | Boot | Can be used as GPIO after boot |
| GPIO2 | Strapping | Must be LOW at boot |
| GPIO4-GPIO39 | GPIO | Can be used for various functions |
| GPIO34-GPIO39 | Input Only | Cannot be used as outputs |

**ADC Mapping:**
- ADC1: GPIO 32-39 (8 channels)
- ADC2: GPIO 0, 2, 4, 12-15, 25-27 (10 channels)

**UART Ports:**
- UART0: TX=GPIO1, RX=GPIO3 (reserved for serial monitor)
- UART1: TX=GPIO10, RX=GPIO9
- UART2: TX=GPIO17, RX=GPIO16

**I2C Ports:**
- I2C0: SDA=GPIO21, SCL=GPIO22
- I2C1: SDA=GPIO25, SCL=GPIO26

**Compiler Support:**
- ESP-IDF (native, recommended)
- Arduino-ESP32 (compatible)

**Datasheet:** [ESP32 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf)

---

#### Arduino Uno
```
Manufacturer:     Arduino
Processor:       ATmega328P
Clock Speed:     16 MHz
Flash Memory:    32 KB
SRAM:            2 KB
EEPROM:          1 KB
Voltage:         5V
GPIO Pins:       14 (0-13)
Analog Pins:     6 (A0-A5)
PWM Pins:        6 (3, 5, 6, 9, 10, 11)
UART:            1 port (RX/TX pins 0-1)
SPI:             Hardware SPI
I2C:             Hardware I2C (pins A4, A5)
```

**Pin Configuration:**
| Pin | Function |
|-----|----------|
| 0-1 | UART (Serial) |
| 2-13 | Digital I/O |
| A0-A5 | Analog Input |
| 3,5,6,9,10,11 | PWM Output |

**I2C Pins:**
- SDA: A4 (pin 18)
- SCL: A5 (pin 19)

**SPI Pins:**
- MOSI: 11
- MISO: 12
- SCK: 13
- CS: 10

**Compiler Support:**
- Arduino CLI (recommended)
- Arduino IDE

**Datasheet:** [ATmega328P Datasheet](https://ww1.microchip.com/en-US/product/ATmega328p)

---

#### Arduino Nano
```
Manufacturer:     Arduino
Processor:       ATmega328P
Clock Speed:     16 MHz
Flash Memory:    32 KB
SRAM:            2 KB
EEPROM:          1 KB
Voltage:         5V (or 3.3V variant)
GPIO Pins:       22
Analog Pins:     8 (A0-A7)
PWM Pins:        6 (3, 5, 6, 9, 10, 11)
UART:            1 port
SPI:             Hardware SPI
I2C:             Hardware I2C
```

**Pin Configuration:** Similar to Arduino Uno but with additional analog pins (A6, A7)

**Compiler Support:**
- Arduino CLI
- Arduino IDE

**Datasheet:** [ATmega328P Datasheet](https://ww1.microchip.com/en-US/product/ATmega328p)

---

### Phase 2 (Planned)

- STM32F1 Series
- STM32L Series
- Raspberry Pi Pico
- nRF52 Series

---

### Phase 3+ (Planned)

- ESP32-CAM
- ESP32-S3
- STM32H Series
- ESP32-C Series

---

## Supported Components

### Sensors

#### MQ2 Gas Sensor
```
Communication:   ADC (Analog Input)
Voltage:         4.9-5.1V
Output:          Analog (0-1023)
Pin Count:       4 (VCC, GND, DOUT, AOUT)
Detection Range: LPG, Methane, CO, Alcohol
Calibration:     Requires 24-48 hours warm-up
Library:         MQ2
```

**Wiring:**
- VCC → Power (5V)
- GND → Ground
- AOUT → ADC Pin (A0)
- DOUT → Digital Pin (optional)

---

#### DHT11 Temperature & Humidity Sensor
```
Communication:   1-Wire Digital
Voltage:         3.3-5.5V
Output:          Digital (temperature + humidity)
Pin Count:       3 (VCC, GND, DATA)
Temperature:     0-50°C (±2°C)
Humidity:        20-90% RH (±5%)
Library:         DHT, DHT11
```

**Wiring:**
- VCC → Power (3.3V or 5V)
- GND → Ground
- DATA → GPIO Pin

**Code Example (Arduino):**
```cpp
#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  dht.begin();
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  Serial.println(temperature);
}
```

---

#### PIR Motion Sensor
```
Communication:   GPIO Digital
Voltage:         4.5-20V
Output:          Digital (HIGH when motion detected)
Detection Range: 5-10 meters
Pin Count:       3 (VCC, GND, OUT)
```

**Wiring:**
- VCC → Power
- GND → Ground
- OUT → GPIO Pin

---

### Actuators

#### LED
```
Communication:   GPIO Digital / PWM
Voltage:         2-3.3V
Current:         20mA (max)
Resistor:        330Ω (recommended)
Pin Count:       2 (Anode, Cathode)
PWM Capable:     Yes (for brightness control)
```

**Wiring:**
```
Resistor (330Ω) → LED Anode
LED Cathode → Ground
Resistor → GPIO Pin
```

---

#### Buzzer
```
Communication:   GPIO Digital / PWM
Voltage:         3.3-5V
Current:         30-50mA
Pin Count:       2 (Positive, Negative)
Frequency:       2-5 kHz (typical)
PWM Capable:     Yes (for tone control)
```

**Wiring:**
- Positive → GPIO Pin
- Negative → Ground

---

#### OLED Display (128x64, SSD1306)
```
Communication:   I2C
Voltage:         3.3V
Current:         20mA
Resolution:      128x64 pixels
I2C Address:     0x3C (typical)
Pin Count:       4 (VCC, GND, SCL, SDA)
Library:         Adafruit_SSD1306, Adafruit_GFX
```

**Wiring:**
- VCC → 3.3V
- GND → Ground
- SCL → I2C Clock Pin (ESP32: GPIO22, Arduino: SCL)
- SDA → I2C Data Pin (ESP32: GPIO21, Arduino: SDA)

**Code Example:**
```cpp
#include <Adafruit_SSD1306.h>
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Hello!");
  display.display();
}
```

---

#### Servo Motor
```
Communication:   PWM
Voltage:         4.8-6V
Current:         100-200mA
Pin Count:       3 (VCC, GND, Signal)
PWM Frequency:   50 Hz
Pulse Width:     1000-2000 µs (0-180°)
Library:         Servo
```

**Wiring:**
- VCC → Power (5V)
- GND → Ground
- Signal → PWM Pin

**Code Example:**
```cpp
#include <Servo.h>
Servo myservo;
int pos = 0;

void setup() {
  myservo.attach(9); // PWM pin
}

void loop() {
  for (pos = 0; pos <= 180; pos += 1) {
    myservo.write(pos);
    delay(15);
  }
}
```

---

## Communication Protocols

### GPIO (General Purpose Input/Output)
- Basic digital input/output
- 1-bit resolution (HIGH/LOW)
- Speed: Microsecond range
- Used by: Buttons, LEDs, motion sensors

### ADC (Analog-to-Digital Converter)
- Converts analog voltage to digital value
- Resolution: 10-bit (0-1023) or 12-bit (0-4095)
- Voltage range: 0-3.3V (ESP32) or 0-5V (Arduino)
- Used by: Gas sensors, temperature sensors, analog inputs

### PWM (Pulse Width Modulation)
- Simulates analog output using digital pins
- Resolution: 8-16 bits
- Frequency: 490-5000 Hz
- Used by: LED brightness, servo control, buzzer frequency

### I2C (Inter-Integrated Circuit)
- Two-wire communication protocol
- Speed: 100 kHz to 3.4 MHz
- Addressing: 7-bit or 10-bit address
- Used by: OLED displays, sensors, expanders

### SPI (Serial Peripheral Interface)
- Four-wire communication protocol
- Speed: Up to 10 MHz
- Master-slave architecture
- Used by: SD cards, flash memory, displays

### UART (Universal Asynchronous Receiver-Transmitter)
- Serial communication protocol
- Speed: 9600-115200 baud (typical)
- Used by: Serial monitor, wireless modules, GPS

---

## Pin Conflict Detection

Roxie validates that:
1. No two components use the same pin
2. Components use only compatible interfaces
3. Reserved pins are not overused
4. Power and ground availability
5. Voltage compatibility

### ESP32 Example: Gas Detection System
```
MQ2 Sensor:
  - Interface: ADC1
  - Pin: GPIO32 ✓ (ADC1 channel)
  - Voltage: 5V ✓ (with power module)

Buzzer:
  - Interface: GPIO + PWM
  - Pin: GPIO33 ✓ (GPIO + PWM capable)
  - Voltage: 3.3V ✓

OLED Display:
  - Interface: I2C0
  - Pins: GPIO21 (SDA), GPIO22 (SCL) ✓
  - Voltage: 3.3V ✓

Validation: ✓ No conflicts detected
```

---

## Power Considerations

### ESP32 DevKit V1
- Operating Voltage: 3.3V (internally)
- Input Voltage: 5V USB or 4.5-5.5V external
- Current Consumption: ~80mA (idle), ~160mA (WiFi active)
- Recommended Power Supply: 2A

### Arduino Uno
- Operating Voltage: 5V
- Input Voltage: 7-12V external, 5V USB
- Current Consumption: ~50mA (at 5V)
- Max per pin: 40mA

### Arduino Nano
- Operating Voltage: 5V or 3.3V (variant dependent)
- Input Voltage: 7-12V or USB
- Current Consumption: ~50mA (at 5V)
- Max per pin: 40mA

---

## Temperature & Environmental Ratings

| Board | Operating Temp | Storage Temp | Humidity |
|-------|----------------|--------------|----------|
| ESP32 | 0-40°C | -40 to 85°C | 30-70% |
| Arduino Uno | 0-45°C | -20 to 85°C | 30-70% |
| Arduino Nano | 0-45°C | -20 to 85°C | 30-70% |

---

For more details, see:
- [API Reference](API.md)
- [Architecture](ARCHITECTURE.md)
- [Firmware Generation Guide](FIRMWARE-GEN.md)
