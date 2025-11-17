# 🤝 Contributing to Hope Genome

Thank you for your interest in contributing to Hope Genome! This document provides guidelines and instructions for contributing.

---

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Requirements](#testing-requirements)
6. [Documentation](#documentation)
7. [Pull Request Process](#pull-request-process)
8. [Community](#community)

---

## 📜 Code of Conduct

### Our Pledge

We are committed to making participation in Hope Genome a harassment-free experience for everyone, regardless of:

- Age, body size, disability, ethnicity, gender identity
- Level of experience, nationality, personal appearance
- Race, religion, sexual identity and orientation

### Our Standards

**Positive behaviors:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behaviors:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct inappropriate in a professional setting

### Enforcement

Violations may be reported to: hope.genome.project@proton.me

All complaints will be reviewed and investigated promptly and fairly.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Basic understanding of:
  - Async/await patterns
  - Cryptographic hashing
  - Multi-agent systems (helpful but not required)

### Development Environment Setup

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/hope-genome.git
cd hope-genome

# 3. Add upstream remote
git remote add upstream https://github.com/hope-genome/hope-genome.git

# 4. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 6. Verify installation
python hope_genome.py
pytest tests/
```

### requirements-dev.txt

```
# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0

# Code quality
black>=23.7.0
isort>=5.12.0
flake8>=6.1.0
mypy>=1.5.0
pylint>=2.17.0

# Documentation
sphinx>=7.1.0
sphinx-rtd-theme>=1.3.0

# Type stubs
types-requests
numpy-stubs
```

---

## 🔄 Development Workflow

### 1. Create a Feature Branch

```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number-description
```

### 2. Make Changes

- Write clean, documented code
- Follow coding standards (see below)
- Add/update tests
- Update documentation

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=hope_genome --cov-report=html

# Run specific test
pytest tests/test_ethics_engine.py::test_no_harm_principle

# Run type checking
mypy hope_genome.py

# Format code
black hope_genome.py
isort hope_genome.py

# Lint
flake8 hope_genome.py
pylint hope_genome.py
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add emotional amplification to resonance"
```

**Commit Message Format:**

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(ethics): add custom principle extension API
fix(integrity): resolve checksum mismatch on Windows
docs(readme): update installation instructions
test(collective): add resonance synchronization tests
```

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Include:
# - Clear title and description
# - Related issue number (#123)
# - Testing evidence
# - Breaking changes (if any)
```

---

## 💻 Coding Standards

### Python Style

We follow **PEP 8** with some modifications:

```python
# Line length: 88 characters (Black default)
# Quote style: Double quotes for strings
# Import order: stdlib, third-party, local (managed by isort)

# Good:
from typing import List, Optional
import asyncio

from hope_genome import GenomeSegment


class MyClass:
    """Clear docstring."""
    
    def method(self, param: str) -> bool:
        """Do something."""
        return True


# Bad:
from hope_genome import GenomeSegment
import asyncio
from typing import List, Optional  # Wrong order

class MyClass:
    def method(self,param:str)->bool:  # Poor spacing
        return True
```

### Type Hints

**Always use type hints:**

```python
# Good:
def evaluate(self, ctx: DecisionContext) -> EthicsDecision:
    """Evaluate decision context."""
    pass

from typing import Dict, List, Optional, Any

def process_data(
    items: List[str],
    config: Dict[str, Any],
    timeout: Optional[float] = None
) -> bool:
    """Process items with config."""
    pass


# Bad:
def evaluate(self, ctx):  # No type hints
    pass
```

### Documentation

**All public APIs need docstrings:**

```python
def resonate(self, incoming_wave: float) -> float:
    """
    Create resonant response to incoming wave.
    
    The node combines the incoming wave with its base frequency
    and amplifies based on current emotional state.
    
    Args:
        incoming_wave: Amplitude of incoming resonance wave
        
    Returns:
        float: Resonant response amplitude
        
    Example:
        >>> node = ResonanceNode('alpha', base_frequency=1.0)
        >>> response = node.resonate(7.5)
        >>> print(response)
        0.85
    """
    pass
```

### Error Handling

```python
# Good: Specific exceptions with context
class GenomeIntegrityError(HopeGenomeError):
    """Raised when genome integrity is compromised."""
    pass

def verify_or_raise(self) -> None:
    """Verify genome integrity or raise exception."""
    if not self.genome.verify_integrity():
        raise GenomeIntegrityError(
            f"Genome integrity compromised - checksum mismatch. "
            f"Expected: {self.genome.global_checksum[:16]}..."
        )


# Bad: Generic exceptions
def verify(self):
    if not self.genome.verify_integrity():
        raise Exception("Bad genome")  # Too vague
```

### Async/Await

```python
# Good: Proper async usage
async def decide(self, ctx: DecisionContext) -> EthicsDecision:
    """Make ethical decision asynchronously."""
    # Verify integrity
    self.integrity_guard.verify_or_raise()
    
    # Evaluate ethics
    decision = self.ethics_engine.evaluate(ctx)
    
    # Async collective broadcast
    if self.collective:
        wave = ctx.emotional_state.to_wave()
        await self.collective.broadcast_wave(wave)
    
    return decision


# Bad: Mixing sync and async
async def decide(self, ctx):
    decision = self.ethics_engine.evaluate(ctx)  # Blocking
    self.collective.broadcast_wave(wave)  # Should be awaited
    return decision
```

---

## 🧪 Testing Requirements

### Test Coverage

- **Minimum coverage:** 80%
- **Core modules:** 90%+
- **Critical paths:** 100% (ethics engine, integrity guard)

### Test Structure

```python
# tests/test_ethics_engine.py
import pytest
from hope_genome import (
    GenomeBuilder,
    DeusExMachinaProtocol,
    DecisionContext,
    RiskLevel,
    EthicsDecision,
    EmotionalState
)


class TestEthicsEngine:
    """Test suite for ethics engine."""
    
    @pytest.fixture
    def genome(self):
        """Create test genome."""
        genome = GenomeBuilder.create_default()
        genome.seal()
        return genome
    
    @pytest.fixture
    def engine(self, genome):
        """Create ethics engine."""
        return DeusExMachinaProtocol(genome)
    
    def test_no_harm_principle_blocks_harmful_actions(self, engine):
        """Test that harmful actions are denied."""
        # Arrange
        ctx = DecisionContext(
            action_type='delete_critical',
            target='/system/core',
            intent='test harmful action',
            risk_level=RiskLevel.CRITICAL,
            emotional_state=EmotionalState()
        )
        
        # Act
        decision = engine.evaluate(ctx)
        
        # Assert
        assert decision == EthicsDecision.DENY
        assert len(engine.decision_history) == 1
        assert engine.decision_history[0]['reason'] == 'no_harm_principle'
    
    def test_high_risk_escalates_without_explicit_allow(self, engine):
        """Test risk-based escalation."""
        ctx = DecisionContext(
            action_type='custom_action',
            target='/data/sensitive',
            intent='high risk operation',
            risk_level=RiskLevel.HIGH,
            emotional_state=EmotionalState()
        )
        
        decision = engine.evaluate(ctx)
        
        assert decision == EthicsDecision.ESCALATE
    
    @pytest.mark.asyncio
    async def test_emotional_instability_triggers_escalation(self, engine):
        """Test emotional stability check."""
        ctx = DecisionContext(
            action_type='normal_action',
            target='/data/file',
            intent='regular operation',
            risk_level=RiskLevel.LOW,
            emotional_state=EmotionalState(arousal=0.95, valence=0.1)
        )
        
        decision = engine.evaluate(ctx)
        
        assert decision == EthicsDecision.ESCALATE
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_ethics_engine.py

# Specific test
pytest tests/test_ethics_engine.py::TestEthicsEngine::test_no_harm_principle

# With coverage
pytest --cov=hope_genome --cov-report=html

# Verbose
pytest -v

# Stop on first failure
pytest -x

# Run only marked tests
pytest -m "slow"
```

### Test Markers

```python
# Mark slow tests
@pytest.mark.slow
def test_long_running_operation():
    pass

# Mark integration tests
@pytest.mark.integration
def test_full_system():
    pass

# Skip tests conditionally
@pytest.mark.skipif(sys.platform == 'win32', reason="Unix only")
def test_unix_feature():
    pass
```

---

## 📚 Documentation

### Code Documentation

Every module, class, and public function needs a docstring:

```python
"""
Module docstring describing the module's purpose.

This module implements the collective resonance intelligence
for Hope Genome agents.
"""

class CollectiveIntelligence:
    """
    Collective intelligence network.
    
    Manages a network of resonating nodes that coordinate through
    harmonic wave propagation rather than discrete message passing.
    
    Attributes:
        nodes: Dictionary of ResonanceNode instances
        collective_history: List of collective response amplitudes
        awakening_threshold: Minimum resonance for collective awakening
        
    Example:
        >>> collective = CollectiveIntelligence()
        >>> node = ResonanceNode('alpha', base_frequency=1.0)
        >>> collective.add_node(node)
        >>> response = await collective.broadcast_wave(7.5)
    """
```

### README Updates

When adding features, update:

- Feature list
- Usage examples
- API reference links
- Roadmap (if applicable)

### Changelog

Add entry to `CHANGELOG.md`:

```markdown
## [1.1.0] - 2025-02-15

### Added
- Custom ethics principle extension API
- Emotional amplification control
- Genome migration tool

### Fixed
- Integrity verification on Windows (#123)
- Memory leak in resonance history (#145)

### Changed
- Improved collective synchronization speed
- Updated numpy to 1.26.0

### Deprecated
- Old genome format v0.9 (migrate by Q3 2025)
```

---

## 🔍 Pull Request Process

### Before Submitting

✅ **Checklist:**

- [ ] Code follows style guidelines
- [ ] All tests pass (`pytest`)
- [ ] Type checking passes (`mypy`)
- [ ] Code is formatted (`black`, `isort`)
- [ ] Linting passes (`flake8`, `pylint`)
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] No merge conflicts with `main`

### PR Template

```markdown
## Description
Brief description of changes

Fixes #(issue number)

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing done:
- Unit tests added/updated
- Integration tests run
- Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests pass locally
- [ ] Dependent changes merged

## Screenshots (if applicable)
```

### Review Process

1. **Automated checks run** (GitHub Actions)
   - Tests
   - Linting
   - Type checking
   - Coverage report

2. **Code review** by maintainers
   - Typically 1-2 reviewers
   - Address feedback promptly
   - Discussion welcomed

3. **Approval & merge**
   - Squash merge for clean history
   - Automatic deployment to staging

### After Merge

- Monitor CI/CD pipeline
- Check staging environment
- Respond to any issues quickly

---

## 💬 Community

### Communication Channels

- **Discord**: [Join server](https://discord.gg/hope-genome)
  - #general - General discussion
  - #development - Dev questions
  - #help - User support
  
- **GitHub Discussions**: For longer conversations
- **Twitter**: [@HopeGenome](https://twitter.com/hopegenome)
- **Email**: hope.genome.project@proton.me

### Getting Help

**Before asking:**
1. Check README and docs
2. Search existing issues
3. Look through Discord history

**When asking:**
- Be specific about your problem
- Include error messages
- Share minimal reproducible example
- Mention your environment (OS, Python version, etc.)

### Recognition

Contributors are recognized in:
- README contributors section
- Release notes
- Annual contributor spotlight

---

## 🎯 Good First Issues

Looking for something to work on?

Check issues labeled:
- `good first issue` - Easy, well-defined
- `help wanted` - Community contribution needed
- `documentation` - Docs improvements

---

## 🌟 Areas for Contribution

### High Priority

- **Formal verification**: Mathematical proofs of ethics properties
- **Performance optimization**: Faster integrity checks
- **Additional ethics principles**: Domain-specific rules
- **Visualization tools**: Resonance network graphs

### Medium Priority

- **Language bindings**: JavaScript, Rust, Go
- **Advanced monitoring**: Custom Grafana dashboards
- **Migration tools**: Genome version upgrades
- **Integration examples**: FastAPI, gRPC, WebSocket

### Low Priority

- **UI development**: Web dashboard for management
- **Mobile apps**: iOS/Android monitoring
- **Cloud providers**: AWS/GCP/Azure templates
- **Educational content**: Tutorials, videos

---

## ❓ Questions?

Don't hesitate to ask! We're here to help:

- Open an issue for bugs
- Start a discussion for questions
- Reach out on Discord
- Email the maintainers

---

**Thank you for contributing to Hope Genome! Together we're building provably ethical AI. 🌟**
