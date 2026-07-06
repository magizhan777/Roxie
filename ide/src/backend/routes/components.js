/**
 * Components Routes - API endpoints for component management
 */

import express from 'express';
import { getComponentsByCategory, getComponent, getCompatiblePins } from '../../hardware-engine/database.js';

const router = express.Router();

/**
 * GET /api/components
 * Get all components grouped by category
 */
router.get('/', (req, res) => {
  try {
    const categories = ['sensors', 'actuators'];
    const components = {};

    for (const category of categories) {
      components[category] = getComponentsByCategory(category);
    }

    res.json({
      success: true,
      data: components
    });
  } catch (error) {
    console.error('[Error] Failed to fetch components:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/components/:category
 * Get components by category
 */
router.get('/:category', (req, res) => {
  try {
    const { category } = req.params;
    const components = getComponentsByCategory(category);

    if (components.length === 0) {
      return res.status(404).json({
        success: false,
        error: `Category '${category}' not found`
      });
    }

    res.json({
      success: true,
      category,
      count: components.length,
      data: components
    });
  } catch (error) {
    console.error('[Error] Failed to fetch components:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/components/:category/:componentId
 * Get specific component details
 */
router.get('/:category/:componentId', (req, res) => {
  try {
    const { category, componentId } = req.params;
    const component = getComponent(category, componentId);

    if (!component) {
      return res.status(404).json({
        success: false,
        error: `Component '${componentId}' not found in category '${category}'`
      });
    }

    res.json({
      success: true,
      data: component
    });
  } catch (error) {
    console.error('[Error] Failed to fetch component:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/components/compatible-pins
 * Get compatible pins for component on board
 * Body: { boardId, componentId, category }
 */
router.post('/compatible-pins', (req, res) => {
  try {
    const { boardId, componentId, category } = req.body;

    if (!boardId || !componentId || !category) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields: boardId, componentId, category'
      });
    }

    const pins = getCompatiblePins(boardId, componentId);

    if (pins === null) {
      return res.status(404).json({
        success: false,
        error: 'Board or component not found'
      });
    }

    res.json({
      success: true,
      boardId,
      componentId,
      compatible_pins: pins
    });
  } catch (error) {
    console.error('[Error] Failed to fetch compatible pins:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

export default router;
