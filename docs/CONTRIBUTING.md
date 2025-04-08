# Guía para Contribuidores

Gracias por considerar contribuir a pyBCRAdata. Este documento proporciona directrices para contribuir al proyecto, especialmente respecto a la documentación bilingüe.

## Estructura del Proyecto

El proyecto sigue esta estructura básica:
- `src/pyBCRAdata/`: Código fuente de la librería
  - `client.py`: Cliente principal y generación de APIs
  - `settings.py`: Configuración y constantes
  - `connector.py`: Conexión HTTP y manejo de certificados
- `docs/`: Documentación en español e inglés
- `tests/`: Pruebas automatizadas

## Documentación Bilingüe

Todo el contenido de documentación debe estar disponible en español e inglés. Sigue estas directrices:

### Formato de Documentos Bilingües

1. Comienza cada documento con el contenido en español
2. Utiliza una línea separadora `---` para dividir los idiomas
3. Continúa con el contenido en inglés, marcado con el emoji 🌐

### Ejemplo de Estructura

```markdown
# Título en Español

Contenido en español...

---

# 🌐 Title in English

Content in English...
```


### Consideraciones para Traducciones

- Mantén la misma estructura de secciones en ambos idiomas
- Asegúrate de que los ejemplos de código funcionan en ambas versiones
- Utiliza las mismas imágenes/diagramas, pero con textos traducidos cuando sea posible
- Mantén sincronizados los cambios en ambos idiomas

## Flujo de Trabajo para Contribuciones

1. Realiza un fork del repositorio
2. Crea una rama para tu contribución: `git checkout -b mi-contribucion`
3. Realiza cambios en el código o documentación
4. Asegúrate de que la documentación está en ambos idiomas
5. Envía un Pull Request

## Pautas para Commits

Utiliza mensajes de commit claros y descriptivos:
- `docs: actualización documentación bilingüe sobre API monetaria`
- `feat: nuevo endpoint para consulta de cheques`
- `fix: corrección en parámetros de divisas`

## Estructura de Código

El proyecto utiliza una estructura modular con las siguientes características:

1. **APIs Preconfiguradas**: Cada API (monetary, currency, checks, debtors) es una instancia preconfigurada
2. **Cliente Principal**: `BCRAclient` proporciona acceso a todas las APIs
3. **Configuración Unificada**: Todas las configuraciones están centralizadas en `settings.py`

---

# 🌐 Guidelines for Contributors

Thank you for considering contributing to pyBCRAdata. This document provides guidelines for contributing to the project, especially regarding bilingual documentation.

## Project Structure

The project follows this basic structure:
- `src/pyBCRAdata/`: Library source code
  - `client.py`: Main client and API generation
  - `settings.py`: Configuration and constants
  - `connector.py`: HTTP connection and certificate handling
- `docs/`: Documentation in Spanish and English
- `tests/`: Automated tests

## Bilingual Documentation

All documentation content must be available in both Spanish and English. Follow these guidelines:

### Bilingual Document Format

1. Start each document with the Spanish content
2. Use a separator line `---` to divide languages
3. Continue with English content, marked with the 🌐 emoji

### Structure Example

```markdown
# Título en Español

Contenido en español...

---

# 🌐 Title in English

Content in English...
```
### Translation Considerations

- Maintain the same section structure in both languages
- Ensure code examples work in both versions
- Use the same images/diagrams, but with translated text when possible
- Keep changes synchronized in both languages

## Contribution Workflow

1. Fork the repository
2. Create a branch for your contribution: `git checkout -b my-contribution`
3. Make changes to code or documentation
4. Ensure documentation is in both languages
5. Submit a Pull Request

## Commit Guidelines

Use clear and descriptive commit messages:
- `docs: updated bilingual documentation on monetary API`
- `feat: new endpoint for check queries`
- `fix: fixed currency parameters`

## Code Structure

The project uses a modular structure with the following features:

1. **Preconfigured APIs**: Each API (monetary, currency, checks, debtors) is a preconfigured instance
2. **Main Client**: `BCRAclient` provides access to all APIs
3. **Unified Configuration**: All configurations are centralized in `settings.py`
