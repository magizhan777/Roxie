/**
 * Projects Routes - API endpoints for project management
 */

import express from 'express';
import { v4 as uuidv4 } from 'uuid';

const router = express.Router();

// In-memory storage (replace with database later)
const projects = new Map();

/**
 * POST /api/projects
 * Create a new project
 */
router.post('/', (req, res) => {
  try {
    const { name, boardId, description } = req.body;

    if (!name || !boardId) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields: name, boardId'
      });
    }

    const projectId = uuidv4();
    const project = {
      id: projectId,
      name,
      boardId,
      description: description || '',
      components: [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    projects.set(projectId, project);

    res.status(201).json({
      success: true,
      data: project
    });
  } catch (error) {
    console.error('[Error] Failed to create project:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/projects
 * Get all projects
 */
router.get('/', (req, res) => {
  try {
    const projectList = Array.from(projects.values());

    res.json({
      success: true,
      count: projectList.length,
      data: projectList
    });
  } catch (error) {
    console.error('[Error] Failed to fetch projects:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/projects/:projectId
 * Get specific project
 */
router.get('/:projectId', (req, res) => {
  try {
    const { projectId } = req.params;
    const project = projects.get(projectId);

    if (!project) {
      return res.status(404).json({
        success: false,
        error: `Project '${projectId}' not found`
      });
    }

    res.json({
      success: true,
      data: project
    });
  } catch (error) {
    console.error('[Error] Failed to fetch project:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * PUT /api/projects/:projectId
 * Update project
 */
router.put('/:projectId', (req, res) => {
  try {
    const { projectId } = req.params;
    const project = projects.get(projectId);

    if (!project) {
      return res.status(404).json({
        success: false,
        error: `Project '${projectId}' not found`
      });
    }

    const { name, description, components } = req.body;

    if (name) project.name = name;
    if (description !== undefined) project.description = description;
    if (components) project.components = components;
    project.updated_at = new Date().toISOString();

    projects.set(projectId, project);

    res.json({
      success: true,
      data: project
    });
  } catch (error) {
    console.error('[Error] Failed to update project:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * DELETE /api/projects/:projectId
 * Delete project
 */
router.delete('/:projectId', (req, res) => {
  try {
    const { projectId } = req.params;

    if (!projects.has(projectId)) {
      return res.status(404).json({
        success: false,
        error: `Project '${projectId}' not found`
      });
    }

    projects.delete(projectId);

    res.json({
      success: true,
      message: 'Project deleted successfully'
    });
  } catch (error) {
    console.error('[Error] Failed to delete project:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

export default router;
