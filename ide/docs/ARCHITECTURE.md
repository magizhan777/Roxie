# Roxie Embedded Studio - Architecture & Design

## System Overview

Roxie Embedded Studio is a full-stack application consisting of:

### Frontend
- **Framework**: Vanilla JavaScript with Web APIs
- **UI Library**: Custom HTML5 Canvas and SVG for 3D board visualization
- **Communication**: WebSocket for real-time updates, HTTP for API calls
- **Styling**: CSS with CSS Variables for theming

### Backend
- **Framework**: Express.js
- **Language**: JavaScript (Node.js)
- **Communication**: RESTful API + WebSocket
- **Database**: (To be implemented - MongoDB or PostgreSQL)

### Firmware Generator
- **LLM Integration**: OpenAI GPT-4 (configurable)
- **Code Generation**: Template-based C/C++ code synthesis
- **Validation**: Hardware compatibility and pin conflict detection

### Hardware Engine
- **Database**: In-memory (JSON) initially, expandable to persistent storage
- **Knowledge Base**: Board specs, component specs, library mappings
- **Pin Validator**: Ensures valid hardware configurations

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser (Frontend)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Roxie Studio UI (3D Board, Components, Commands)    │  │
│  │                                                       │  │
│  │  - 3D Board Viewer (Three.js or Babylon.js)         │  │
│  │  - Component Library                                 │  │
│  │  - Natural Language Panel                            │  │
│  │  - Firmware Status Monitor                           │  │
│  │  - Serial Monitor                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
           │                                          │
           │ WebSocket & HTTP                         │
           │                                          │
┌──────────────────────────────────────────────────────────────┐
│               Backend Server (Node.js/Express)              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Routes                                           │  │
│  │  ├── /api/boards          → Board Management        │  │
│  │  ├── /api/components      → Component Library       │  │
│  │  ├── /api/projects        → Project Management      │  │
│  │  ├── /api/firmware        → Firmware Generation     │  │
│  │  ├── /api/compiler        → Build & Upload          │  │
│  │  └── /api/serial          → Serial Communication    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Hardware Engine                                      │  │
│  │  ├── Board Database (specs, pins, capabilities)     │  │
│  │  ├── Component Database (sensors, actuators)        │  │
│  │  ├── Library Database (dependencies)                │  │
│  │  └── Validators (pin conflict, compatibility)       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Firmware Generator                                  │  │
│  │  ├── LLM Adapter (OpenAI API)                       │  │
│  │  ├── Code Generator (C/C++ templates)              │  │
│  │  ├── Library Resolver (dependency resolution)       │  │
│  │  └── Validator (syntax & compatibility)             │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
           │                              │
           │ Compiler API                 │ Serial Port
           │ File I/O                     │
           │                              │
┌──────────────────────────┐   ┌─────────────────────────────┐
│  Build System            │   │  Device Communication       │
│  ├── Arduino CLI         │   │  ├── Serial Port Monitor    │
│  ├── ESP-IDF             │   │  └── Over-the-Air Updates   │
│  └── Build Artifacts     │   │                             │
└──────────────────────────┘   └─────────────────────────────┘
           │                              │
           ▼                              ▼
┌──────────────────────────┐   ┌─────────────────────────────┐
│  Microcontroller         │   │  Physical Device            │
│  ├── ESP32              │   │  ├── Sensors               │
│  ├── Arduino Uno        │   │  ├── Actuators             │
│  └── Arduino Nano       │   │  └── Display               │
└──────────────────────────┘   └─────────────────────────────┘
```

## Data Flow

### 1. Project Creation Flow

```
User selects board → Creates project → Saved in database
```

### 2. Component Addition Flow

```
User selects components → API validates compatibility →
Components stored with pin assignments → UI updated
```

### 3. Firmware Generation Flow

```
User enters natural language intent →
Backend calls LLM with:
  - Board specifications
  - Selected components
  - User intent
  - Hardware constraints
        ↓
LLM generates C/C++ code →
Code generator creates full firmware →
Validator checks syntax and hardware compatibility →
Generated code stored →
Ready for compilation
```

### 4. Compilation & Upload Flow

```
User clicks "Compile" →
Backend detects board type →
Calls appropriate compiler (Arduino CLI or ESP-IDF) →
Captures build output →
Returns status to frontend via WebSocket →
User selects serial port →
Uploads compiled binary →
Real-time progress via WebSocket
```

### 5. Serial Monitoring Flow

```
User connects to device via serial port →
Backend opens serial connection →
Forwards data to frontend via WebSocket →
Frontend displays logs in real-time →
User can send commands via WebSocket
```

## Key Components

### Frontend
- **3D Board Viewer**: Interactive 3D representation of microcontroller
- **Component Library Panel**: Drag-and-drop component selection
- **Natural Language Panel**: Text input for firmware intent
- **Firmware Status Panel**: Visual progress of generation/compilation
- **Serial Monitor**: Real-time device output

### Backend

#### Board Management Service
- Retrieve board specifications
- Validate pin capabilities
- Check reserved pins
- Map pins to functions

#### Component Management Service
- Get component specifications
- Check voltage/current requirements
- Determine communication protocols
- Find compatible pins

#### Firmware Generation Service
- Interface with LLM
- Template-based code synthesis
- Hardware compatibility validation
- Dependency resolution

#### Compiler Service
- Detect available compilers
- Execute build commands
- Parse compilation output
- Handle errors

#### Serial Communication Service
- Open/close serial ports
- Read device output
- Send commands to device
- Monitor connection status

### Hardware Engine

#### Board Database
```json
{
  "id": "esp32-devkit-v1",
  "name": "ESP32 DevKit V1",
  "pins_total": 38,
  "adc_channels": { "ADC1": [32, 33, ...], "ADC2": [...] },
  "pwm_capable_pins": [0, 2, 4, ...],
  "uart_ports": { "UART0": {...}, ... },
  "spi_ports": { "SPI1": {...}, ... },
  "i2c_ports": { "I2C0": {...}, ... }
}
```

#### Component Database
```json
{
  "id": "mq2",
  "name": "MQ2 Gas Sensor",
  "communication": "ADC",
  "compatible_interfaces": ["ADC"],
  "libraries": ["MQ2"],
  "pins": { "AOUT": "Analog Output" }
}
```

## API Specification

### Boards API
```
GET    /api/boards              - List all boards
GET    /api/boards/:id          - Get board details
GET    /api/boards/:id/pins     - Get pin configuration
GET    /api/boards/:id/capabilities - Get features
```

### Components API
```
GET    /api/components          - List all components
GET    /api/components/:category - Get by category
GET    /api/components/:cat/:id - Get component details
POST   /api/components/compatible-pins - Find compatible pins
```

### Projects API
```
POST   /api/projects            - Create project
GET    /api/projects            - List projects
GET    /api/projects/:id        - Get project
PUT    /api/projects/:id        - Update project
DELETE /api/projects/:id        - Delete project
```

### Firmware API
```
POST   /api/firmware/generate   - Generate firmware
GET    /api/firmware/:id/status - Get generation status
```

### Compiler API
```
POST   /api/compiler/build      - Compile firmware
POST   /api/compiler/upload     - Upload to device
GET    /api/compiler/devices    - List serial ports
```

### Serial API
```
POST   /api/serial/connect      - Open serial connection
POST   /api/serial/disconnect   - Close connection
POST   /api/serial/send         - Send command
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Backend | Node.js, Express.js |
| Real-time | WebSocket (Socket.io) |
| Database | MongoDB/PostgreSQL (planned) |
| 3D Visualization | Three.js or Babylon.js (planned) |
| LLM Integration | OpenAI API / Hugging Face (planned) |
| Build Tools | Arduino CLI, ESP-IDF |
| Serial Communication | node-serialport |

## Security Considerations

1. **API Authentication**: Implement JWT tokens for API access
2. **LLM API Keys**: Store securely in environment variables
3. **File Upload**: Validate uploaded firmware binaries
4. **Serial Port Access**: Restrict to authorized users
5. **Input Validation**: Sanitize all user inputs
6. **Code Injection**: Prevent malicious code in firmware generation

## Performance Optimization

1. **Caching**: Cache board and component specs
2. **WebSocket**: Use WebSocket for real-time updates instead of polling
3. **Code Generation**: Implement incremental compilation
4. **Database**: Index frequently queried fields
5. **Frontend**: Lazy load 3D models and large assets

## Scalability Plan

1. **Microservices**: Separate firmware generator into dedicated service
2. **Queue System**: Use job queue (Bull, RabbitMQ) for long-running tasks
3. **Load Balancing**: Deploy multiple backend instances
4. **Database**: Use proper database instead of in-memory storage
5. **Caching Layer**: Redis for caching hardware specs and project data

## Testing Strategy

1. **Unit Tests**: Test individual services and validators
2. **Integration Tests**: Test API endpoints and hardware engine
3. **E2E Tests**: Test complete workflows from UI to device
4. **Hardware Tests**: Test on real microcontroller boards

## Deployment

### Development
```bash
npm run dev
npm run build-ui:dev
```

### Production
```bash
npm start
npm run build-ui
```

### Docker (future)
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]
```

---

For detailed information on specific components, see:
- [Firmware Generation Guide](FIRMWARE-GEN.md)
- [Hardware Specifications](HARDWARE.md)
- [API Reference](API.md)
