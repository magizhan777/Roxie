/**
 * Board Routes - API endpoints for board management
 */

import express from 'express';
import { getAllBoards, getBoard } from '../../hardware-engine/database.js';

const router = express.Router();

/**
 * GET /api/boards
 * Get all available boards
 */
router.get('/', (req, res) => {
  try {
    const boards = getAllBoards();
    res.json({
      success: true,
      count: boards.length,
      data: boards
    });
  } catch (error) {
    console.error('[Error] Failed to fetch boards:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/boards/:boardId
 * Get specific board details
 */
router.get('/:boardId', (req, res) => {
  try {
    const { boardId } = req.params;
    const board = getBoard(boardId);

    if (!board) {
      return res.status(404).json({
        success: false,
        error: `Board '${boardId}' not found`
      });
    }

    res.json({
      success: true,
      id: boardId,
      data: board
    });
  } catch (error) {
    console.error('[Error] Failed to fetch board:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/boards/:boardId/pins
 * Get pin configuration for a board
 */
router.get('/:boardId/pins', (req, res) => {
  try {
    const { boardId } = req.params;
    const board = getBoard(boardId);

    if (!board) {
      return res.status(404).json({
        success: false,
        error: `Board '${boardId}' not found`
      });
    }

    const pinConfig = {
      total: board.pins_total,
      reserved: board.reserved_pins,
      adc_channels: board.adc_channels,
      pwm_pins: board.pwm_capable_pins,
      uart_ports: board.uart_ports,
      spi_ports: board.spi_ports,
      i2c_ports: board.i2c_ports
    };

    res.json({
      success: true,
      data: pinConfig
    });
  } catch (error) {
    console.error('[Error] Failed to fetch pin configuration:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/boards/:boardId/capabilities
 * Get board capabilities and features
 */
router.get('/:boardId/capabilities', (req, res) => {
  try {
    const { boardId } = req.params;
    const board = getBoard(boardId);

    if (!board) {
      return res.status(404).json({
        success: false,
        error: `Board '${boardId}' not found`
      });
    }

    const capabilities = {
      name: board.name,
      manufacturer: board.manufacturer,
      core: board.core,
      frequency: board.cpu_frequency,
      flash: board.flash,
      ram: board.ram,
      voltage: board.voltage,
      features: board.features,
      compilers: board.compiler_support
    };

    res.json({
      success: true,
      data: capabilities
    });
  } catch (error) {
    console.error('[Error] Failed to fetch board capabilities:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

export default router;
