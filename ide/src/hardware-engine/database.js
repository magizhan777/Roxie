/**
 * Hardware Knowledge Engine
 * Central database for all board and component specifications
 */

export const BOARDS = {
  'esp32-devkit-v1': {
    name: 'ESP32 DevKit V1',
    manufacturer: 'Espressif',
    core: 'Xtensa 32-bit LX6',
    cpu_frequency: '240 MHz',
    flash: '4 MB',
    ram: '520 KB',
    voltage: 3.3,
    pins_total: 38,
    reserved_pins: [0, 2, 12, 15], // Bootstrap pins
    boot_pins: [0, 2, 12, 15],
    strapping_pins: [0, 2, 4, 5, 12, 15],
    adc_channels: {
      'ADC1': [32, 33, 34, 35, 36, 37, 38, 39],
      'ADC2': [0, 2, 4, 12, 13, 14, 15, 25, 26, 27]
    },
    pwm_channels: 16,
    pwm_capable_pins: [0, 2, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33],
    uart_ports: {
      'UART0': { tx: 1, rx: 3, reserved: true },
      'UART1': { tx: 10, rx: 9 },
      'UART2': { tx: 17, rx: 16 }
    },
    spi_ports: {
      'SPI1': { mosi: 7, miso: 8, clk: 6, cs: 11 },
      'SPI2': { mosi: 13, miso: 12, clk: 14, cs: 15 },
      'SPI3': { mosi: 23, miso: 19, clk: 18, cs: 5 }
    },
    i2c_ports: {
      'I2C0': { sda: 21, scl: 22 },
      'I2C1': { sda: 25, scl: 26 }
    },
    features: ['WiFi', 'Bluetooth', 'BLE', 'ADC', 'DAC', 'I2C', 'SPI', 'UART', 'PWM', 'Touch'],
    compiler_support: ['ESP-IDF', 'Arduino-ESP32'],
    image_url: '/assets/models/esp32-devkit-v1.svg',
    datasheet_url: 'https://docs.espressif.com/projects/esp32-devkit/...'
  },
  'arduino-uno': {
    name: 'Arduino Uno',
    manufacturer: 'Arduino',
    core: 'ATmega328P',
    cpu_frequency: '16 MHz',
    flash: '32 KB',
    ram: '2 KB',
    eeprom: '1 KB',
    voltage: 5,
    pins_total: 14,
    digital_pins: 14,
    analog_pins: 6,
    pwm_pins: [3, 5, 6, 9, 10, 11],
    adc_channels: [0, 1, 2, 3, 4, 5],
    uart_ports: {
      'Serial': { tx: 1, rx: 0 }
    },
    spi_pins: { mosi: 11, miso: 12, clk: 13, cs: 10 },
    i2c_pins: { sda: 'A4', scl: 'A5' },
    features: ['16-bit Timer', 'SPI', 'I2C', 'UART', 'PWM', 'ADC', 'Comparator'],
    compiler_support: ['Arduino-CLI'],
    image_url: '/assets/models/arduino-uno.svg',
    datasheet_url: 'https://ww1.microchip.com/en-US/product/ATmega328p'
  },
  'arduino-nano': {
    name: 'Arduino Nano',
    manufacturer: 'Arduino',
    core: 'ATmega328P',
    cpu_frequency: '16 MHz',
    flash: '32 KB',
    ram: '2 KB',
    eeprom: '1 KB',
    voltage: 5,
    pins_total: 30,
    digital_pins: 14,
    analog_pins: 8,
    pwm_pins: [3, 5, 6, 9, 10, 11],
    adc_channels: [0, 1, 2, 3, 4, 5, 6, 7],
    uart_ports: {
      'Serial': { tx: 1, rx: 0 }
    },
    spi_pins: { mosi: 11, miso: 12, clk: 13, cs: 10 },
    i2c_pins: { sda: 'A4', scl: 'A5' },
    features: ['16-bit Timer', 'SPI', 'I2C', 'UART', 'PWM', 'ADC', 'Comparator'],
    compiler_support: ['Arduino-CLI'],
    image_url: '/assets/models/arduino-nano.svg',
    datasheet_url: 'https://ww1.microchip.com/en-US/product/ATmega328p'
  }
};

export const COMPONENTS = {
  sensors: {
    'mq2': {
      name: 'MQ2 Gas Sensor',
      type: 'Sensor',
      category: 'Gas',
      voltage_range: '4.9-5.1V',
      output_type: 'Analog',
      communication: 'ADC',
      libraries: ['MQ2'],
      pin_count: 4,
      pins: {
        'VCC': 'Power',
        'GND': 'Ground',
        'DOUT': 'Digital Output',
        'AOUT': 'Analog Output'
      },
      compatible_interfaces: ['ADC'],
      typical_connections: {
        esp32: { adc: 'ADC1_0' },
        arduino: { analog: 'A0' }
      },
      datasheet_url: 'https://www.sparkfun.com/datasheets/Sensors/Biometric/MQ2.pdf',
      notes: 'Requires warm-up time of 24-48 hours for calibration'
    },
    'mq135': {
      name: 'MQ135 Air Quality Sensor',
      type: 'Sensor',
      category: 'Gas/Air Quality',
      voltage_range: '4.9-5.1V',
      output_type: 'Analog',
      communication: 'ADC',
      libraries: ['MQ135'],
      pin_count: 4,
      pins: {
        'VCC': 'Power',
        'GND': 'Ground',
        'DOUT': 'Digital Output',
        'AOUT': 'Analog Output'
      },
      compatible_interfaces: ['ADC'],
      datasheet_url: 'https://www.sparkfun.com/datasheets/Sensors/Biometric/MQ135.pdf'
    },
    'dht11': {
      name: 'DHT11 Temperature & Humidity Sensor',
      type: 'Sensor',
      category: 'Environmental',
      voltage_range: '3.3-5.5V',
      output_type: 'Digital',
      communication: '1-Wire',
      libraries: ['DHT', 'DHT11'],
      pin_count: 3,
      pins: {
        'VCC': 'Power',
        'GND': 'Ground',
        'DATA': 'Digital Signal'
      },
      compatible_interfaces: ['GPIO'],
      datasheet_url: 'https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT11.pdf'
    },
    'pir': {
      name: 'PIR Motion Sensor',
      type: 'Sensor',
      category: 'Motion',
      voltage_range: '4.5-20V',
      output_type: 'Digital',
      communication: 'GPIO',
      libraries: [],
      pin_count: 3,
      pins: {
        'VCC': 'Power',
        'GND': 'Ground',
        'OUT': 'Digital Output'
      },
      compatible_interfaces: ['GPIO'],
      datasheet_url: 'https://www.sparkfun.com/datasheets/Sensors/Infrared/Parallax-PIR.pdf'
    }
  },
  actuators: {
    'led': {
      name: 'LED',
      type: 'Actuator',
      category: 'Light',
      voltage_range: '2-3.3V',
      current: '20mA',
      output_type: 'Digital',
      communication: 'GPIO',
      libraries: [],
      pin_count: 2,
      pins: {
        'Anode': 'Positive',
        'Cathode': 'Negative'
      },
      compatible_interfaces: ['GPIO', 'PWM'],
      requires_resistor: true,
      resistor_value: '330Ω'
    },
    'buzzer': {
      name: 'Buzzer',
      type: 'Actuator',
      category: 'Sound',
      voltage_range: '3.3-5V',
      current: '30-50mA',
      output_type: 'Digital',
      communication: 'GPIO',
      libraries: [],
      pin_count: 2,
      pins: {
        'Positive': 'Power',
        'Negative': 'Ground'
      },
      compatible_interfaces: ['GPIO', 'PWM'],
      pwm_capable: true
    },
    'oled-display': {
      name: 'OLED Display (128x64)',
      type: 'Actuator',
      category: 'Display',
      voltage_range: '3.3V',
      current: '20mA',
      output_type: 'Display',
      communication: 'I2C',
      libraries: ['Adafruit_SSD1306', 'Adafruit_GFX'],
      pin_count: 4,
      pins: {
        'VCC': 'Power',
        'GND': 'Ground',
        'SCL': 'I2C Clock',
        'SDA': 'I2C Data'
      },
      compatible_interfaces: ['I2C'],
      i2c_address: '0x3C',
      datasheet_url: 'https://learn.adafruit.com/monochrome-oled-displays'
    },
    'servo': {
      name: 'Servo Motor',
      type: 'Actuator',
      category: 'Motion',
      voltage_range: '4.8-6V',
      current: '100-200mA',
      output_type: 'Motion',
      communication: 'PWM',
      libraries: ['Servo'],
      pin_count: 3,
      pins: {
        'VCC': 'Power',
        'GND': 'Ground',
        'SIGNAL': 'PWM Signal'
      },
      compatible_interfaces: ['PWM'],
      pwm_frequency: '50Hz',
      datasheet_url: 'https://www.sparkfun.com/datasheets/Robotics/Servo/HiTec-HS-311.pdf'
    }
  }
};

export const LIBRARIES = {
  esp32: {
    'DHT': { version: '1.4.4', dependencies: [] },
    'MQ2': { version: '1.0.0', dependencies: [] },
    'Adafruit_SSD1306': { version: '2.5.9', dependencies: ['Adafruit_GFX'] },
    'Adafruit_GFX': { version: '1.11.9', dependencies: [] },
    'ArduinoJson': { version: '7.0.4', dependencies: [] },
    'PubSubClient': { version: '2.8.0', dependencies: [] }
  },
  arduino: {
    'DHT': { version: '1.4.4', dependencies: [] },
    'MQ2': { version: '1.0.0', dependencies: [] },
    'Adafruit_SSD1306': { version: '2.5.9', dependencies: ['Adafruit_GFX'] },
    'Adafruit_GFX': { version: '1.11.9', dependencies: [] },
    'Servo': { version: '1.2.2', dependencies: [] },
    'Wire': { version: 'built-in', dependencies: [] }
  }
};

/**
 * Get board specification by ID
 */
export function getBoard(boardId) {
  return BOARDS[boardId] || null;
}

/**
 * Get all boards
 */
export function getAllBoards() {
  return Object.entries(BOARDS).map(([id, board]) => ({
    id,
    ...board
  }));
}

/**
 * Get component specification by category and component ID
 */
export function getComponent(category, componentId) {
  if (COMPONENTS[category] && COMPONENTS[category][componentId]) {
    return {
      id: componentId,
      ...COMPONENTS[category][componentId]
    };
  }
  return null;
}

/**
 * Get all components by category
 */
export function getComponentsByCategory(category) {
  if (COMPONENTS[category]) {
    return Object.entries(COMPONENTS[category]).map(([id, component]) => ({
      id,
      ...component
    }));
  }
  return [];
}

/**
 * Get compatible pins for a component on a board
 */
export function getCompatiblePins(boardId, componentId) {
  const board = getBoard(boardId);
  if (!board) return null;

  // Find component in all categories
  let component = null;
  for (const category in COMPONENTS) {
    if (COMPONENTS[category][componentId]) {
      component = COMPONENTS[category][componentId];
      break;
    }
  }

  if (!component) return null;

  const compatiblePins = [];

  // Match component interfaces with board capabilities
  for (const iface of component.compatible_interfaces) {
    if (iface === 'GPIO') {
      // All non-reserved pins
      for (let i = 0; i < board.pins_total; i++) {
        if (!board.reserved_pins.includes(i)) {
          compatiblePins.push(i);
        }
      }
    } else if (iface === 'ADC') {
      compatiblePins.push(...Object.values(board.adc_channels || {}).flat());
    } else if (iface === 'PWM') {
      compatiblePins.push(...(board.pwm_capable_pins || []));
    } else if (iface === 'I2C') {
      if (board.i2c_ports) {
        Object.values(board.i2c_ports).forEach(port => {
          compatiblePins.push(port.sda, port.scl);
        });
      }
    }
  }

  return [...new Set(compatiblePins)]; // Remove duplicates
}

export default {
  getBoard,
  getAllBoards,
  getComponent,
  getComponentsByCategory,
  getCompatiblePins,
  BOARDS,
  COMPONENTS,
  LIBRARIES
};
