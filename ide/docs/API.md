# Roxie Embedded Studio - API Reference

## Base URL
```
http://localhost:3000/api
```

## Authentication
Currently, the API uses no authentication. This will be added in future versions using JWT tokens.

## Response Format

All API responses follow a standard JSON format:

### Success Response
```json
{
  "success": true,
  "data": {},
  "message": "Optional message"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error description",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Endpoints

### Boards

#### List All Boards
```http
GET /boards
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "id": "esp32-devkit-v1",
      "name": "ESP32 DevKit V1",
      "manufacturer": "Espressif",
      "pins_total": 38,
      "features": ["WiFi", "Bluetooth", "BLE", "ADC", "DAC", "I2C", "SPI", "UART", "PWM"]
    }
  ]
}
```

#### Get Board Details
```http
GET /boards/{boardId}
```

**Parameters:**
- `boardId` (string, required): Board identifier (e.g., `esp32-devkit-v1`)

**Response:**
```json
{
  "success": true,
  "id": "esp32-devkit-v1",
  "data": {
    "name": "ESP32 DevKit V1",
    "manufacturer": "Espressif",
    "core": "Xtensa 32-bit LX6",
    "cpu_frequency": "240 MHz",
    "flash": "4 MB",
    "ram": "520 KB",
    "voltage": 3.3,
    "pins_total": 38,
    "reserved_pins": [0, 2, 12, 15],
    "features": ["WiFi", "Bluetooth", "BLE"]
  }
}
```

#### Get Pin Configuration
```http
GET /boards/{boardId}/pins
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total": 38,
    "reserved": [0, 2, 12, 15],
    "adc_channels": {
      "ADC1": [32, 33, 34, 35, 36, 37, 38, 39],
      "ADC2": [0, 2, 4, 12, 13, 14, 15, 25, 26, 27]
    },
    "pwm_pins": [0, 2, 4, 5, 12, 13, 14, 15],
    "uart_ports": {
      "UART0": { "tx": 1, "rx": 3 }
    },
    "i2c_ports": {
      "I2C0": { "sda": 21, "scl": 22 }
    }
  }
}
```

#### Get Board Capabilities
```http
GET /boards/{boardId}/capabilities
```

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "ESP32 DevKit V1",
    "manufacturer": "Espressif",
    "core": "Xtensa 32-bit LX6",
    "frequency": "240 MHz",
    "flash": "4 MB",
    "ram": "520 KB",
    "voltage": 3.3,
    "features": ["WiFi", "Bluetooth", "BLE"],
    "compilers": ["ESP-IDF", "Arduino-ESP32"]
  }
}
```

### Components

#### List All Components
```http
GET /components
```

**Response:**
```json
{
  "success": true,
  "data": {
    "sensors": [
      {
        "id": "mq2",
        "name": "MQ2 Gas Sensor",
        "type": "Sensor",
        "communication": "ADC"
      }
    ],
    "actuators": [
      {
        "id": "led",
        "name": "LED",
        "type": "Actuator",
        "communication": "GPIO"
      }
    ]
  }
}
```

#### Get Components by Category
```http
GET /components/{category}
```

**Parameters:**
- `category` (string, required): `sensors` or `actuators`

**Response:**
```json
{
  "success": true,
  "category": "sensors",
  "count": 8,
  "data": [
    {
      "id": "mq2",
      "name": "MQ2 Gas Sensor",
      "voltage_range": "4.9-5.1V",
      "communication": "ADC",
      "libraries": ["MQ2"]
    }
  ]
}
```

#### Get Component Details
```http
GET /components/{category}/{componentId}
```

**Parameters:**
- `category` (string, required): `sensors` or `actuators`
- `componentId` (string, required): Component identifier

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "mq2",
    "name": "MQ2 Gas Sensor",
    "type": "Sensor",
    "voltage_range": "4.9-5.1V",
    "output_type": "Analog",
    "communication": "ADC",
    "libraries": ["MQ2"],
    "compatible_interfaces": ["ADC"],
    "datasheet_url": "https://..."
  }
}
```

#### Get Compatible Pins
```http
POST /components/compatible-pins
```

**Request Body:**
```json
{
  "boardId": "esp32-devkit-v1",
  "componentId": "mq2",
  "category": "sensors"
}
```

**Response:**
```json
{
  "success": true,
  "boardId": "esp32-devkit-v1",
  "componentId": "mq2",
  "compatible_pins": [32, 33, 34, 35, 36, 37, 38, 39]
}
```

### Projects

#### Create Project
```http
POST /projects
```

**Request Body:**
```json
{
  "name": "Gas Detection System",
  "boardId": "esp32-devkit-v1",
  "description": "Real-time gas monitoring with alerts"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "proj-uuid-1234",
    "name": "Gas Detection System",
    "boardId": "esp32-devkit-v1",
    "description": "Real-time gas monitoring with alerts",
    "components": [],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

#### List Projects
```http
GET /projects
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": "proj-uuid-1234",
      "name": "Gas Detection System",
      "boardId": "esp32-devkit-v1",
      "components": [],
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Get Project
```http
GET /projects/{projectId}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "proj-uuid-1234",
    "name": "Gas Detection System",
    "boardId": "esp32-devkit-v1",
    "components": [
      {
        "id": "mq2",
        "category": "sensors",
        "pin": 32
      }
    ],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

#### Update Project
```http
PUT /projects/{projectId}
```

**Request Body:**
```json
{
  "name": "Advanced Gas Detection",
  "components": [
    {
      "id": "mq2",
      "category": "sensors",
      "pin": 32
    },
    {
      "id": "buzzer",
      "category": "actuators",
      "pin": 33
    }
  ]
}
```

#### Delete Project
```http
DELETE /projects/{projectId}
```

**Response:**
```json
{
  "success": true,
  "message": "Project deleted successfully"
}
```

### Firmware Generation

#### Generate Firmware
```http
POST /firmware/generate
```

**Request Body:**
```json
{
  "projectId": "proj-uuid-1234",
  "boardId": "esp32-devkit-v1",
  "components": [
    {
      "id": "mq2",
      "category": "sensors",
      "pin": 32
    },
    {
      "id": "buzzer",
      "category": "actuators",
      "pin": 33
    }
  ],
  "naturalLanguageIntent": "If gas concentration exceeds 300 ppm, activate the buzzer and display warning"
}
```

**Response:** *(Not yet implemented)*
```json
{
  "success": false,
  "message": "Firmware generation not yet implemented"
}
```

#### Get Firmware Status
```http
GET /firmware/{projectId}/status
```

**Response:**
```json
{
  "success": true,
  "projectId": "proj-uuid-1234",
  "status": "idle",
  "steps": [
    {
      "name": "Validating hardware",
      "status": "completed",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Compiler

#### Build Firmware
```http
POST /compiler/build
```

**Request Body:**
```json
{
  "projectId": "proj-uuid-1234",
  "boardId": "esp32-devkit-v1"
}
```

#### Upload Firmware
```http
POST /compiler/upload
```

**Request Body:**
```json
{
  "projectId": "proj-uuid-1234",
  "boardId": "esp32-devkit-v1",
  "port": "/dev/ttyUSB0",
  "baudRate": 115200
}
```

#### List Available Devices
```http
GET /compiler/devices
```

**Response:**
```json
{
  "success": true,
  "devices": [
    {
      "port": "/dev/ttyUSB0",
      "serialNumber": "ABC123",
      "manufacturer": "FTDI"
    }
  ]
}
```

### Serial Monitor

#### Connect to Device
```http
POST /serial/connect
```

**Request Body:**
```json
{
  "port": "/dev/ttyUSB0",
  "baudRate": 115200
}
```

#### Send Command
```http
POST /serial/send
```

**Request Body:**
```json
{
  "port": "/dev/ttyUSB0",
  "command": "STATUS"
}
```

#### Disconnect
```http
POST /serial/disconnect
```

**Request Body:**
```json
{
  "port": "/dev/ttyUSB0"
}
```

## WebSocket Events

### Connection
```javascript
const socket = io('http://localhost:3000');

socket.on('connect', () => {
  console.log('Connected to server');
});
```

### Firmware Generation
```javascript
// Subscribe to firmware generation progress
socket.on('firmware:generating', (data) => {
  console.log('Step:', data.step);
  console.log('Progress:', data.progress);
});

socket.on('firmware:complete', (data) => {
  console.log('Firmware generated:', data.code);
});

socket.on('firmware:error', (data) => {
  console.log('Error:', data.error);
});
```

### Serial Monitor
```javascript
// Real-time device output
socket.on('serial:data', (data) => {
  console.log('Device output:', data);
});

socket.on('serial:error', (error) => {
  console.error('Serial error:', error);
});
```

---

For implementation details, see [ARCHITECTURE.md](ARCHITECTURE.md)
