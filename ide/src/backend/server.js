/**
 * Roxie Embedded Studio - Main Backend Server
 * Entry point for the API server
 */

import express from 'express';
import http from 'http';
import { Server as SocketIOServer } from 'socket.io';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

// Load environment variables
dotenv.config();

// Import routes
import boardRoutes from './routes/boards.js';
import projectRoutes from './routes/projects.js';
import firmwareRoutes from './routes/firmware.js';
import compilerRoutes from './routes/compiler.js';
import componentRoutes from './routes/components.js';
import serialRoutes from './routes/serial.js';

// Get __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = http.createServer(app);
const io = new SocketIOServer(server, {
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    methods: ['GET', 'POST']
  }
});

const PORT = process.env.PORT || 3000;
const NODE_ENV = process.env.NODE_ENV || 'development';

// Middleware
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));

// Logging middleware
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// CORS headers
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

// Serve static files
app.use(express.static(path.join(__dirname, '../../')));

// API Routes
app.use('/api/boards', boardRoutes);
app.use('/api/projects', projectRoutes);
app.use('/api/firmware', firmwareRoutes);
app.use('/api/compiler', compilerRoutes);
app.use('/api/components', componentRoutes);
app.use('/api/serial', serialRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    environment: NODE_ENV,
    version: '0.1.0'
  });
});

// Serve main HTML file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../../roxie_embedded_studio.html'));
});

// WebSocket connection handling
io.on('connection', (socket) => {
  console.log(`[WebSocket] Client connected: ${socket.id}`);

  socket.on('disconnect', () => {
    console.log(`[WebSocket] Client disconnected: ${socket.id}`);
  });

  // Firmware generation events
  socket.on('generate-firmware', async (data) => {
    console.log('[WebSocket] Firmware generation requested:', data);
    // Handler will be implemented in the firmware service
  });

  // Serial monitor events
  socket.on('serial-monitor:start', (data) => {
    console.log('[WebSocket] Serial monitor started:', data);
  });

  socket.on('serial-monitor:stop', (data) => {
    console.log('[WebSocket] Serial monitor stopped:', data);
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('[Error]', err);
  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error',
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    path: req.path,
    timestamp: new Date().toISOString()
  });
});

// Start server
server.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════════════╗
║      Roxie Embedded Studio - Backend Server       ║
╠════════════════════════════════════════════════════╣
║ Environment: ${NODE_ENV.padEnd(35)} ║
║ Port:        ${PORT.toString().padEnd(35)} ║
║ Status:      Ready                                 ║
╚════════════════════════════════════════════════════╝
  `);
  console.log(`API Documentation: http://localhost:${PORT}/api/docs`);
  console.log(`WebSocket: ws://localhost:${PORT}`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n[Server] Shutting down gracefully...');
  server.close(() => {
    console.log('[Server] Server closed');
    process.exit(0);
  });
});

export { app, io };
