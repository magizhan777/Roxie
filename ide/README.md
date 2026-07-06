# Roxie Embedded Studio

**AI-Powered Embedded Systems and IoT Development Environment**

An intelligent IDE for embedded systems and IoT development that eliminates manual coding through visual hardware design and natural language intent description.

## 🎯 Vision

Traditional embedded development requires deep knowledge of microcontrollers, pin configurations, libraries, and firmware compilation. Roxie Embedded Studio democratizes this process by allowing developers to:

1. **Select Hardware** - Choose from supported microcontrollers (ESP32, Arduino, STM32, etc.)
2. **Visual Design** - Interact with 3D board models and click pins directly
3. **Add Components** - Select sensors and actuators from a library
4. **Describe Intent** - Write natural language descriptions of desired behavior
5. **Auto-Generate** - Let AI handle:
   - Pin assignment
   - Library selection
   - Firmware generation
   - Configuration
   - Compilation
   - Deployment

## 🚀 Features (Phase 1)

### Core Capabilities

- **Interactive 3D Board Viewer**
  - Real-time 3D models of microcontroller boards
  - Pin detection and capability display
  - Hover information and tooltips
  - Zoom, rotate, pan controls

- **Component Library**
  - **Sensors**: MQ2, MQ135, DHT11, DHT22, PIR, Ultrasonic, LDR, Soil Moisture
  - **Actuators**: LED, RGB LED, Relay, Buzzer, Servo, DC Motor, OLED, LCD

- **Natural Language Command Panel**
  - Conversational interface for firmware instructions
  - Real-time AI processing
  - Hardware validation and constraint checking

- **Firmware Generator**
  - Automatic pin assignment optimization
  - Library dependency resolution
  - Embedded C/C++ code generation
  - Conflict detection and reporting

- **Compiler Integration**
  - Arduino CLI for Arduino boards
  - ESP-IDF for ESP32 boards
  - Real-time build logs
  - Error reporting and suggestions

- **Serial Monitor**
  - Real-time device logs
  - Sensor data visualization
  - Command execution interface
  - Debug output streaming

### Supported Microcontrollers (Phase 1)

- ESP32 DevKit V1
- Arduino Uno
- Arduino Nano

## 📁 Project Structure

```
roxie-embedded-studio/
├── src/
│   ├── frontend/              # Web UI components
│   │   ├── components/        # React/Vue components
│   │   ├── modules/          # Feature modules
│   │   ├── styles/           # CSS/styling
│   │   └── index.js          # Entry point
│   ├── backend/              # Node.js backend server
│   │   ├── routes/           # API endpoints
│   │   ├── controllers/      # Request handlers
│   │   ├── middleware/       # Express middleware
│   │   ├── services/         # Business logic
│   │   ├── models/           # Data models
│   │   └── server.js         # Entry point
│   ├── firmware-generator/   # AI firmware code generation
│   │   ├── llm-adapter/      # LLM integration
│   │   ├── code-generator/   # C/C++ generation
│   │   ├── library-resolver/ # Dependency resolution
│   │   └── validator/        # Hardware validation
│   └── hardware-engine/      # Hardware knowledge base
│       ├── boards/           # Board definitions
│       ├── components/       # Component specs
│       ├── validators/       # Pin/config validation
│       └── database/         # Hardware metadata
├── config/                   # Configuration files
│   ├── boards/              # Board configurations
│   ├── components/          # Component definitions
│   ├── compilers/           # Compiler settings
│   └── libraries/           # Library mappings
├── templates/               # Code templates
│   ├── arduino/
│   ├── esp32/
│   └── base/
├── assets/                  # Static assets
│   ├── models/              # 3D board models
│   ├── icons/               # UI icons
│   └── images/              # UI images
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md      # System design
│   ├── API.md              # API documentation
│   ├── HARDWARE.md         # Hardware specs
│   └── FIRMWARE-GEN.md     # Firmware generation guide
├── package.json            # Node.js dependencies
├── .env.example            # Environment variables template
└── roxie_embedded_studio.html # Main HTML entry point
```

## 🔧 Installation

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Arduino CLI (for Arduino board support)
- ESP-IDF (for ESP32 support)

### Setup

```bash
# Clone the repository
git clone https://github.com/roxie-ai/roxie-embedded-studio.git
cd roxie-embedded-studio

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Configure Arduino CLI path and ESP-IDF path in .env
# Edit .env with your local paths

# Start development server
npm run dev

# In another terminal, build UI assets
npm run build-ui:dev
```

## 📖 Documentation

- [Architecture & Design](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Hardware Specifications](docs/HARDWARE.md)
- [Firmware Generation Guide](docs/FIRMWARE-GEN.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🔄 Workflow Example

### User: Gas Detection System with Alert

**Input:**
- Board: ESP32 DevKit V1
- Components: MQ2 Sensor, Buzzer, OLED Display
- Intent: "If gas concentration exceeds 300 ppm, activate the buzzer and display warning on OLED"

**System Output:**
1. ✅ Hardware validation completed
2. ✅ Pin assignment optimized
   - MQ2 → GPIO32 (ADC)
   - Buzzer → GPIO33 (PWM)
   - OLED → GPIO21, GPIO22 (I2C)
3. ✅ Libraries resolved
   - ESP32 Core
   - Adafruit_MQ2
   - Adafruit_SSD1306
4. ✅ Firmware generated (150 lines of C++)
5. ✅ Compilation successful
6. ✅ Ready to upload

## 🚀 Roadmap

### Phase 2
- MQTT Integration
- Wi-Fi Configuration Wizard
- Cloud Dashboard Generation
- Mobile Monitoring App

### Phase 3
- Circuit Diagram Generator
- Wiring Diagram Generator
- Component Cost Estimator
- BOM (Bill of Materials) Generator

### Phase 4
- AI Wiring Verification via Camera
- Circuit Image Analysis
- Automatic Fault Detection

### Phase 5
- PCB Designer Integration
- KiCad Project Generation
- Schematic Generation
- PCB Layout Suggestions
- Gerber Export

## 🔗 Future Integration with Roxie AI

Roxie Embedded Studio operates as a standalone module but will integrate with the larger Roxie AI ecosystem:

```
Roxie AI Frontend
    ↓
"Create an ESP32-based gas detection system"
    ↓
Roxie Embedded Studio API
    ↓
[Automatic Hardware Design → Firmware Generation → Compilation → Deployment]
    ↓
Deployment Status & Logs
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📞 Support

For issues, feature requests, and discussions:
- GitHub Issues: [roxie-ai/roxie-embedded-studio/issues](https://github.com/roxie-ai/roxie-embedded-studio/issues)
- Documentation: [docs/](docs/)

---

**Built with ❤️ by the Roxie AI Team**
