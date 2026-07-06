# Roxie Embedded Studio - Quick Reference

## 🚀 Start Server

```bash
npm run dev          # Development mode
npm start            # Production mode
npm run build-ui:dev # Watch UI changes
```

**Access:** http://localhost:3000

## 📚 API Quick Reference

### Boards
```bash
GET /api/boards
GET /api/boards/{id}
GET /api/boards/{id}/pins
GET /api/boards/{id}/capabilities
```

### Components
```bash
GET /api/components
GET /api/components/{category}
GET /api/components/{category}/{id}
POST /api/components/compatible-pins
```

### Projects
```bash
POST /api/projects                    # Create
GET /api/projects                     # List
GET /api/projects/{id}                # Get one
PUT /api/projects/{id}                # Update
DELETE /api/projects/{id}             # Delete
```

### Firmware
```bash
POST /api/firmware/generate           # Generate code
GET /api/firmware/{projectId}/status  # Check progress
```

### Compiler
```bash
POST /api/compiler/build              # Compile
POST /api/compiler/upload             # Upload to device
GET /api/compiler/devices             # List COM ports
```

### Serial
```bash
POST /api/serial/connect              # Open connection
POST /api/serial/send                 # Send command
POST /api/serial/disconnect           # Close connection
```

## 📋 Supported Boards

| Board | Pins | Compiler | Status |
|-------|------|----------|--------|
| ESP32 DevKit V1 | 38 | ESP-IDF, Arduino-ESP32 | ✅ |
| Arduino Uno | 14 | Arduino CLI | ✅ |
| Arduino Nano | 22 | Arduino CLI | ✅ |

## 🔌 Supported Components

### Sensors (8 types)
- MQ2, MQ135 (Gas)
- DHT11, DHT22 (Temp/Humidity)
- PIR (Motion)
- Ultrasonic (Distance)
- LDR (Light)
- Soil Moisture

### Actuators (7 types)
- LED, RGB LED
- Buzzer
- Servo Motor
- Relay
- DC Motor
- OLED Display
- LCD Display

## 🛠️ Configuration

### Environment Variables
```env
PORT=3000
NODE_ENV=development
LLM_API_KEY=your_key
ARDUINO_CLI_PATH=/path/to/arduino-cli
EPSDIR=/path/to/esp-idf
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/backend/server.js` | Server entry point |
| `src/hardware-engine/database.js` | Board specs |
| `src/backend/routes/*.js` | API endpoints |
| `src/frontend/studio.js` | UI controller |
| `roxie_embedded_studio.html` | HTML entry point |

## 🔌 WebSocket Events

```javascript
// Connect
const socket = io();

// Listen for firmware updates
socket.on('firmware:progress', (data) => { ... });

// Listen for serial data
socket.on('serial:data', (data) => { ... });

// Listen for errors
socket.on('error', (error) => { ... });
```

## 💻 Frontend API Usage

```javascript
// Get all boards
fetch('/api/boards')
  .then(r => r.json())
  .then(data => console.log(data.data));

// Create project
fetch('/api/projects', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'My Project',
    boardId: 'esp32-devkit-v1'
  })
})
.then(r => r.json())
.then(data => console.log(data.data));
```

## 🧪 Testing

```bash
# Unit tests
npm test

# Lint code
npm run lint

# Fix linting
npm run lint:fix
```

## 🐛 Debugging

### Check Logs
```bash
# View error log
tail -f logs/error.log

# View combined log
tail -f logs/combined.log
```

### Browser Console
```javascript
roxieStudio.currentProject     # Current project
roxieStudio.boards            # All boards
roxieStudio.components        # All components
roxieStudio.socket            # WebSocket connection
```

### Server Debugging
```bash
NODE_DEBUG=* npm run dev
```

## 🔧 Common Tasks

### Add New Board
1. Edit `src/hardware-engine/database.js`
2. Add to `BOARDS` object
3. Define pins, features, capabilities

### Add New Component
1. Edit `src/hardware-engine/database.js`
2. Add to `COMPONENTS[category]` object
3. Specify pins, libraries, interfaces

### Add New API Route
1. Create file in `src/backend/routes/`
2. Define endpoints with Express
3. Import and mount in `server.js`

### Update Documentation
- API changes → `docs/API.md`
- Architecture → `docs/ARCHITECTURE.md`
- Hardware → `docs/HARDWARE.md`
- Setup → `DEVELOPMENT.md`

## 📊 Project Stats

```
Lines of Code:     ~500 (core)
API Endpoints:     18
Supported Boards:  3
Components:        15+
Documentation:     6 files
```

## 🔗 Important Links

- **GitHub**: https://github.com/roxie-ai/roxie-embedded-studio
- **Arduino CLI**: https://arduino.github.io/arduino-cli/
- **ESP-IDF**: https://docs.espressif.com/projects/esp-idf/
- **Socket.io**: https://socket.io/docs/
- **Express.js**: https://expressjs.com/

## 🆘 Troubleshooting

### Arduino CLI Not Found
```bash
# Add to PATH or set ARDUINO_CLI_PATH in .env
which arduino-cli  # macOS/Linux
where arduino-cli  # Windows
```

### Port 3000 Already in Use
```bash
# Find process
lsof -i :3000      # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill it
kill -9 <PID>      # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Node Modules Broken
```bash
rm -rf node_modules package-lock.json
npm install
```

### WebSocket Connection Failed
1. Check if server is running
2. Check CORS settings
3. Verify WebSocket URL in config

## 📝 Workflow Example

```javascript
// 1. Create project
const project = await fetch('/api/projects', {
  method: 'POST',
  body: JSON.stringify({
    name: 'Gas Detector',
    boardId: 'esp32-devkit-v1'
  })
});

// 2. Add components
components: [
  { id: 'mq2', category: 'sensors', pin: 32 },
  { id: 'buzzer', category: 'actuators', pin: 33 }
]

// 3. Generate firmware
await roxieStudio.generateFirmware(
  'Alert when gas exceeds 300 ppm'
);

// 4. Compile
await roxieStudio.compileFirmware();

// 5. Upload
await roxieStudio.uploadFirmware('COM3');

// 6. Monitor
socket.on('serial:data', msg => console.log(msg));
```

## 📞 Support

- **Issues**: Open on GitHub
- **Questions**: Check documentation
- **Discussions**: Use GitHub Discussions
- **Bugs**: File with reproduction steps

---

**Last Updated:** January 2024  
**Version:** 0.1.0  
**Status:** In Development
