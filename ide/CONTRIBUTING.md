# Contributing to Roxie Embedded Studio

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on the code, not the person
- Help others learn and grow
- Report issues responsibly

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Git
- Arduino CLI (for Arduino board testing)
- ESP-IDF (for ESP32 testing)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/roxie-ai/roxie-embedded-studio.git
cd roxie-embedded-studio

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# - Set Arduino CLI path
# - Set ESP-IDF path
# - Set LLM API key (optional for testing)

# Start development server
npm run dev

# In another terminal, watch UI changes
npm run build-ui:dev
```

## Development Workflow

### Creating a Feature

1. Create a new branch from `main`:
   ```bash
   git checkout -b feature/my-feature-name
   ```

2. Make your changes with meaningful commits:
   ```bash
   git commit -m "feat: add new feature"
   ```

3. Push to your branch:
   ```bash
   git push origin feature/my-feature-name
   ```

4. Open a Pull Request with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots if UI changes
   - Test results

### Commit Message Format

Use conventional commits:

```
feat: add new feature
fix: resolve issue
docs: update documentation
style: format code
refactor: reorganize code
test: add tests
chore: maintenance tasks
```

## Code Style

### JavaScript

- Use ES6+ syntax
- Use const/let (no var)
- Meaningful variable names
- Comments for complex logic
- 2-space indentation

```javascript
// Good
const calculateGasThreshold = (baseLevel) => {
  return baseLevel * 1.5;
};

// Bad
var ct = (b) => b * 1.5;
```

### Documentation

- Document public functions/classes
- Include JSDoc comments
- Provide usage examples
- Update README if adding features

```javascript
/**
 * Calculate compatible pins for a component
 * @param {string} boardId - The board identifier
 * @param {string} componentId - The component identifier
 * @returns {Array<number>} Array of compatible pin numbers
 * @throws {Error} If board or component not found
 */
function getCompatiblePins(boardId, componentId) {
  // Implementation
}
```

## Testing

### Unit Tests

```bash
npm test
```

### Integration Tests

Test against real hardware when possible:

1. Test with each supported board
2. Verify component compatibility
3. Check hardware validation

### Manual Testing Checklist

- [ ] Can create a project
- [ ] Can add components
- [ ] Can select pins without conflicts
- [ ] Can generate firmware code
- [ ] UI responds correctly to actions
- [ ] WebSocket updates work
- [ ] Serial monitor connects/disconnects

## Areas for Contribution

### High Priority

1. **Firmware Generation** - Improve LLM prompts and code generation
2. **Hardware Engine** - Add more boards and components
3. **Build System** - Enhance Arduino CLI and ESP-IDF integration
4. **UI/UX** - Improve 3D board visualization and interactions
5. **Testing** - Add comprehensive test coverage

### Medium Priority

1. **Documentation** - Improve guides and API docs
2. **Error Handling** - Better error messages and recovery
3. **Performance** - Optimize firmware generation speed
4. **Code Quality** - Refactor and improve code structure

### Nice to Have

1. **Features** - MQTT support, dashboard generation
2. **Visualization** - Circuit diagrams, wiring guides
3. **Tools** - Cost calculator, BOM generator
4. **Integration** - Roxie AI ecosystem integration

## Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (OS, Node version, etc.)
- Error messages or logs

```markdown
## Bug: Firmware generation fails for ESP32

**Description:**
When I try to generate firmware with MQ2 sensor, it fails.

**Steps to Reproduce:**
1. Create project with ESP32 DevKit V1
2. Add MQ2 sensor (pin 32)
3. Enter natural language intent
4. Click "Generate Firmware"

**Error:**
```
Error: Cannot read property 'libraries' of undefined
```

**Environment:**
- OS: Windows 10
- Node: 18.16.0
- Browser: Chrome 114
```

### Feature Requests

Include:
- Clear use case
- Expected behavior
- Example workflow
- Benefit to users

## Pull Request Process

1. **Update Tests** - Add tests for new functionality
2. **Update Docs** - Update README, API docs, etc.
3. **Keep PR Focused** - One feature per PR when possible
4. **Request Review** - Ask maintainers to review
5. **Address Feedback** - Make requested changes
6. **Squash Commits** - Optional: squash before merge

## Documentation

### When to Update Docs

- Adding a new API endpoint → Update [API.md](docs/API.md)
- Adding a new board → Update [HARDWARE.md](docs/HARDWARE.md)
- Changing architecture → Update [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- New firmware feature → Update [FIRMWARE-GEN.md](docs/FIRMWARE-GEN.md)
- Installation steps → Update [README.md](README.md)

### Documentation Format

Use Markdown with:
- Clear headings
- Code blocks with language specification
- Examples where helpful
- Links to related docs
- Tables for structured data

## License

By contributing, you agree that your contributions will be licensed under the same MIT License as the project.

## Questions?

- Open a GitHub issue
- Start a discussion
- Check existing documentation
- Ask on community forums

---

**Thank you for contributing to Roxie Embedded Studio! 🚀**

Your contributions help make embedded development more accessible to everyone.
