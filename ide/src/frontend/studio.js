/**
 * Roxie Embedded Studio - Main UI Controller
 * Handles initialization and communication with backend
 */

class RoxieStudio {
  constructor() {
    this.currentBoard = null;
    this.currentProject = null;
    this.selectedComponents = [];
    this.socket = null;
    this.apiBaseUrl = '/api';

    this.init();
  }

  /**
   * Initialize the application
   */
  async init() {
    console.log('[Studio] Initializing Roxie Embedded Studio...');

    try {
      // Initialize WebSocket
      this.initWebSocket();

      // Load available boards
      await this.loadBoards();

      // Setup UI event listeners
      this.setupEventListeners();

      // Load projects
      await this.loadProjects();

      console.log('[Studio] Initialization complete ✓');
    } catch (error) {
      console.error('[Studio] Initialization failed:', error);
      this.showError('Failed to initialize application');
    }
  }

  /**
   * Initialize WebSocket connection
   */
  initWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const socketUrl = `${protocol}//${window.location.host}`;

    this.socket = io(socketUrl, {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });

    this.socket.on('connect', () => {
      console.log('[WebSocket] Connected ✓');
      this.updateConnectionStatus(true);
    });

    this.socket.on('disconnect', () => {
      console.log('[WebSocket] Disconnected');
      this.updateConnectionStatus(false);
    });

    this.socket.on('firmware:progress', (data) => {
      this.updateFirmwareStatus(data);
    });

    this.socket.on('serial:data', (data) => {
      this.appendSerialMonitor(data);
    });

    this.socket.on('error', (error) => {
      console.error('[WebSocket] Error:', error);
      this.showError(`WebSocket error: ${error}`);
    });
  }

  /**
   * Load available boards from API
   */
  async loadBoards() {
    try {
      const response = await fetch(`${this.apiBaseUrl}/boards`);
      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error);
      }

      this.boards = result.data;
      this.populateBoardSelector();

      console.log(`[Studio] Loaded ${result.count} boards ✓`);
    } catch (error) {
      console.error('[Studio] Failed to load boards:', error);
      throw error;
    }
  }

  /**
   * Load available components from API
   */
  async loadComponents() {
    try {
      const response = await fetch(`${this.apiBaseUrl}/components`);
      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error);
      }

      this.components = result.data;
      this.populateComponentLibrary();

      console.log('[Studio] Loaded components ✓');
    } catch (error) {
      console.error('[Studio] Failed to load components:', error);
      throw error;
    }
  }

  /**
   * Load projects from API
   */
  async loadProjects() {
    try {
      const response = await fetch(`${this.apiBaseUrl}/projects`);
      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error);
      }

      this.projects = result.data;
      this.populateProjectList();

      console.log(`[Studio] Loaded ${result.count} projects ✓`);
    } catch (error) {
      console.error('[Studio] Failed to load projects:', error);
      // Non-critical error, continue
    }
  }

  /**
   * Create a new project
   */
  async createProject(name, boardId, description = '') {
    try {
      const response = await fetch(`${this.apiBaseUrl}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, boardId, description })
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error);
      }

      this.currentProject = result.data;
      await this.loadProjects();

      console.log(`[Studio] Project created: ${name} ✓`);
      return result.data;
    } catch (error) {
      console.error('[Studio] Failed to create project:', error);
      this.showError(`Failed to create project: ${error.message}`);
      throw error;
    }
  }

  /**
   * Update current project
   */
  async updateProject(updates) {
    if (!this.currentProject) {
      throw new Error('No project selected');
    }

    try {
      const response = await fetch(
        `${this.apiBaseUrl}/projects/${this.currentProject.id}`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(updates)
        }
      );

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error);
      }

      this.currentProject = result.data;
      console.log('[Studio] Project updated ✓');
      return result.data;
    } catch (error) {
      console.error('[Studio] Failed to update project:', error);
      this.showError(`Failed to update project: ${error.message}`);
      throw error;
    }
  }

  /**
   * Generate firmware for current project
   */
  async generateFirmware(naturalLanguageIntent) {
    if (!this.currentProject) {
      throw new Error('No project selected');
    }

    try {
      this.showFirmwareStatus('Generating firmware...');

      const response = await fetch(`${this.apiBaseUrl}/firmware/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId: this.currentProject.id,
          boardId: this.currentProject.boardId,
          components: this.currentProject.components,
          naturalLanguageIntent
        })
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error);
      }

      console.log('[Studio] Firmware generation initiated ✓');
      return result;
    } catch (error) {
      console.error('[Studio] Failed to generate firmware:', error);
      this.showError(`Firmware generation failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Compile firmware for current project
   */
  async compileFirmware() {
    if (!this.currentProject) {
      throw new Error('No project selected');
    }

    try {
      this.showFirmwareStatus('Compiling...');

      const response = await fetch(`${this.apiBaseUrl}/compiler/build`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId: this.currentProject.id,
          boardId: this.currentProject.boardId
        })
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error);
      }

      console.log('[Studio] Compilation initiated ✓');
      return result;
    } catch (error) {
      console.error('[Studio] Failed to compile:', error);
      this.showError(`Compilation failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Upload firmware to device
   */
  async uploadFirmware(port, baudRate = 115200) {
    if (!this.currentProject) {
      throw new Error('No project selected');
    }

    try {
      this.showFirmwareStatus('Uploading...');

      const response = await fetch(`${this.apiBaseUrl}/compiler/upload`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId: this.currentProject.id,
          boardId: this.currentProject.boardId,
          port,
          baudRate
        })
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error);
      }

      console.log('[Studio] Upload initiated ✓');
      return result;
    } catch (error) {
      console.error('[Studio] Failed to upload:', error);
      this.showError(`Upload failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Setup UI event listeners
   */
  setupEventListeners() {
    // Board selector
    const boardSelector = document.querySelector('[data-action="select-board"]');
    if (boardSelector) {
      boardSelector.addEventListener('change', (e) => this.selectBoard(e.target.value));
    }

    // Create project button
    const createBtn = document.querySelector('[data-action="create-project"]');
    if (createBtn) {
      createBtn.addEventListener('click', () => this.showCreateProjectDialog());
    }

    // Natural language input
    const nlInput = document.querySelector('[data-action="nl-command"]');
    const nlSend = document.querySelector('[data-action="nl-send"]');
    if (nlSend) {
      nlSend.addEventListener('click', () => {
        if (nlInput) {
          const intent = nlInput.value.trim();
          if (intent) {
            this.generateFirmware(intent);
            nlInput.value = '';
          }
        }
      });
    }

    // Compile button
    const compileBtn = document.querySelector('[data-action="compile"]');
    if (compileBtn) {
      compileBtn.addEventListener('click', () => this.compileFirmware());
    }

    // Upload button
    const uploadBtn = document.querySelector('[data-action="upload"]');
    if (uploadBtn) {
      uploadBtn.addEventListener('click', () => {
        const port = prompt('Enter serial port (e.g., COM3, /dev/ttyUSB0):');
        if (port) {
          this.uploadFirmware(port);
        }
      });
    }
  }

  /**
   * Select board
   */
  async selectBoard(boardId) {
    const board = this.boards?.find(b => b.id === boardId);
    if (board) {
      this.currentBoard = board;
      await this.loadComponents();
      console.log(`[Studio] Board selected: ${board.name}`);
    }
  }

  /**
   * Add component to project
   */
  async addComponent(componentId, category) {
    if (!this.currentProject) {
      this.showError('Please create a project first');
      return;
    }

    try {
      // Get compatible pins
      const response = await fetch(`${this.apiBaseUrl}/components/compatible-pins`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          boardId: this.currentProject.boardId,
          componentId,
          category
        })
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error);
      }

      const pins = result.compatible_pins;
      const selectedPin = pins[0]; // Default to first available

      // Add to project
      this.currentProject.components.push({
        id: componentId,
        category,
        pin: selectedPin
      });

      await this.updateProject({ components: this.currentProject.components });
      console.log(`[Studio] Component added: ${componentId} on pin ${selectedPin}`);
    } catch (error) {
      console.error('[Studio] Failed to add component:', error);
      this.showError(`Failed to add component: ${error.message}`);
    }
  }

  /**
   * Populate board selector in UI
   */
  populateBoardSelector() {
    // This will be implemented in the HTML template
    console.log('[Studio] Board selector populated');
  }

  /**
   * Populate component library in UI
   */
  populateComponentLibrary() {
    // This will be implemented in the HTML template
    console.log('[Studio] Component library populated');
  }

  /**
   * Populate project list in UI
   */
  populateProjectList() {
    // This will be implemented in the HTML template
    console.log('[Studio] Project list populated');
  }

  /**
   * Show firmware status
   */
  showFirmwareStatus(message) {
    console.log(`[Firmware] ${message}`);
    // Update UI
  }

  /**
   * Update firmware status
   */
  updateFirmwareStatus(data) {
    console.log('[Firmware] Status update:', data);
    // Update UI with progress
  }

  /**
   * Append to serial monitor
   */
  appendSerialMonitor(data) {
    console.log('[Serial]', data);
    // Update serial monitor UI
  }

  /**
   * Update connection status
   */
  updateConnectionStatus(connected) {
    const statusDot = document.querySelector('[data-element="connection-status"]');
    if (statusDot) {
      if (connected) {
        statusDot.classList.add('connected');
        statusDot.textContent = '●';
      } else {
        statusDot.classList.remove('connected');
        statusDot.textContent = '○';
      }
    }
  }

  /**
   * Show error message
   */
  showError(message) {
    console.error('[Error]', message);
    alert(message); // TODO: Replace with better UI notification
  }

  /**
   * Show create project dialog
   */
  showCreateProjectDialog() {
    const name = prompt('Project name:');
    if (name && this.currentBoard) {
      this.createProject(name, this.currentBoard.id);
    }
  }
}

// Initialize studio when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.roxieStudio = new RoxieStudio();
});
