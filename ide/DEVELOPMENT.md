# Development Setup Guide

## Quick Start

### 1. Environment Setup

```bash
# Install Node.js 18+
# Download from https://nodejs.org/

# Verify installation
node --version  # v18.x or higher
npm --version   # 9.x or higher
```

### 2. Install Dependencies

```bash
cd roxie-embedded-studio
npm install
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
# Windows:
notepad .env

# macOS/Linux:
nano .env
```

**Key configurations:**

```env
# Server
PORT=3000
NODE_ENV=development

# Arduino CLI (required for Arduino boards)
ARDUINO_CLI_PATH=C:\Program Files\Arduino\arduino-cli.exe
# or on macOS/Linux:
ARDUINO_CLI_PATH=/usr/local/bin/arduino-cli

# ESP-IDF (required for ESP32)
EPSDIR=C:\esp\esp-idf
# or on macOS/Linux:
EPSDIR=~/esp/esp-idf

# LLM API (for AI firmware generation)
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_API_KEY=your_api_key_here
```

### 4. Install Build Tools

#### Arduino CLI

**Windows:**
```bash
# Download from https://github.com/arduino/arduino-cli/releases
# Extract to C:\Program Files\Arduino\

# Verify
arduino-cli version
```

**macOS:**
```bash
brew install arduino-cli

# Verify
arduino-cli version
```

**Linux:**
```bash
# Download and extract
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

# Verify
arduino-cli version
```

#### ESP-IDF

**Windows:**
```bash
# Download ESP-IDF from:
# https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/windows-setup.html

# Or use:
git clone https://github.com/espressif/esp-idf.git
cd esp-idf
./install.bat
```

**macOS:**
```bash
mkdir -p ~/esp
cd ~/esp
git clone https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh
```

**Linux:**
```bash
mkdir -p ~/esp
cd ~/esp
git clone https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh
```

### 5. Start Development

```bash
# Terminal 1: Start backend server
npm run dev

# Terminal 2: Build UI (watch mode)
npm run build-ui:dev

# Open browser to http://localhost:3000
```

## Project Structure

```
roxie-embedded-studio/
├── src/
│   ├── backend/           # Express.js backend
│   │   ├── server.js      # Entry point
│   │   ├── routes/        # API endpoints
│   │   └── hardware-engine/  # Hardware database
│   └── frontend/          # Web UI
│       ├── studio.js      # Main controller
│       └── index.html     # Scripts loader
├── config/                # Configuration files
├── templates/             # Code templates
├── assets/                # Static assets
├── docs/                  # Documentation
└── package.json           # Dependencies
```

## Available Commands

```bash
# Development
npm run dev              # Start development server
npm run build-ui:dev    # Build UI (watch mode)

# Production
npm start               # Start production server
npm run build-ui       # Build UI (production)

# Maintenance
npm test               # Run tests
npm run lint           # Lint code
npm run lint:fix       # Fix linting issues
```

## Debugging

### Backend Debugging

```bash
# Run with debugging enabled
NODE_DEBUG=* npm run dev

# Or use VS Code debugger
# Add .vscode/launch.json:
```

### Frontend Debugging

Use browser DevTools:

```javascript
// In browser console
roxieStudio.currentProject  // View current project
roxieStudio.boards         // View loaded boards
roxieStudio.generateFirmware('...')  // Test firmware generation
```

### Logging

The backend uses winston for logging:

```javascript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'debug',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' })
  ]
});

logger.info('Application started');
logger.error('An error occurred', error);
```

## Testing

### Unit Tests

```bash
npm test
```

### Integration Testing

Test with real hardware:

1. **Arduino Uno:**
   - Upload simple blink sketch
   - Verify serial communication
   - Test pin assignments

2. **Arduino Nano:**
   - Same as Uno
   - Verify programmer settings

3. **ESP32:**
   - Flash firmware via esptool
   - Verify WiFi connectivity
   - Test serial output

## Troubleshooting

### Arduino CLI Not Found

```bash
# Check if installed
arduino-cli version

# Add to PATH if needed
# Windows: Set environment variable
# macOS/Linux: Add to ~/.bashrc or ~/.zshrc
export PATH=$PATH:/path/to/arduino-cli
```

### ESP-IDF Issues

```bash
# Source the environment
# Windows:
esp-idf\export.bat

# macOS/Linux:
source ~/esp/esp-idf/export.sh

# Verify
idf.py --version
```

### Node Modules Issues

```bash
# Clean installation
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use

```bash
# Find process using port 3000
# Windows:
netstat -ano | findstr :3000

# macOS/Linux:
lsof -i :3000

# Kill process
# Windows:
taskkill /PID <PID> /F

# macOS/Linux:
kill -9 <PID>
```

## IDE Setup

### VS Code

Install extensions:
- **ES Lint** (dbaeumer.vscode-eslint)
- **Prettier** (esbenp.prettier-vscode)
- **REST Client** (humao.rest-client)
- **Serial Monitor** (ms-vscode.serial-monitor)

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch Backend",
      "program": "${workspaceFolder}/src/backend/server.js",
      "console": "integratedTerminal"
    }
  ]
}
```

### WebStorm

- Right-click `src/backend/server.js` → "Run"
- Set Node.js interpreter
- Configure run configuration

## Git Setup

```bash
# Configure git
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create feature branch
git checkout -b feature/my-feature

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/my-feature
```

## Additional Resources

- [Node.js Documentation](https://nodejs.org/en/docs/)
- [Express.js Guide](https://expressjs.com/)
- [Arduino CLI Docs](https://arduino.github.io/arduino-cli/)
- [ESP-IDF Guide](https://docs.espressif.com/projects/esp-idf/)
- [Socket.io Docs](https://socket.io/docs/)

---

For more details, see:
- [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [API.md](docs/API.md)
