
# ⚗️ PyThermoDB Settings

[![PyPI Downloads](https://static.pepy.tech/badge/pythermodb-settings/month)](https://pepy.tech/projects/pythermodb-settings)
![PyPI Version](https://img.shields.io/pypi/v/pythermodb-settings)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/pythermodb-settings.svg)
![License](https://img.shields.io/pypi/l/pythermodb-settings)
[![Download on the App Store](https://img.shields.io/badge/Download_on_the_App_Store-0D0D0D?logo=apple&logoColor=white)](https://apps.apple.com/ca/app/mozithermocalc/id6759209992)

## 📖 Introduction

**PyThermoDB Settings** is a Python package that acts as an interface between [pythermdb](https://github.com/sinagilassi/pythermdb) and other applications, providing robust, Pydantic-based data models and configuration structures for managing thermodynamic database (ThermoDB) settings.

Calculations can also be done on your mobile with the MoziThermoCalc iOS app: [Download on the App Store](https://apps.apple.com/ca/app/mozithermocalc/id6759209992).

## ✨ Features

- 🧪 **Component Modeling:**

	Define chemical components with attributes such as name, formula, state (gas, liquid, solid, aqueous), and mole fraction.

- 🌡️ **Condition Models:**

	Represent temperature and pressure conditions with unit validation.

- ⚙️ **Component Configuration:**

	TypedDict-based configuration for databook, table, mode, and custom labels.

- 📚 **Reference Models:**

	- `ReferenceThermoDB`: Structure for reference thermodynamic databases, including references, contents, configs, rules, and label management.
	- `ComponentReferenceThermoDB`: Links a component to its reference database.
	- `ReferencesThermoDB`: Handles multiple references and their configurations.

- 📏 **Rule Management:**

	Define and manage rules for components using dictionary-based structures.

- ✅ **Extensible and Validated:**

	All models use Pydantic for input validation and extensibility.


## 💾 Installation

Install via pip (after packaging):

```bash
pip install pythermodb_settings
```


## 🚀 Usage Example

```python
from pythermodb_settings.models import Component, Temperature, Pressure

# component example
component = Component(
		name="Water",
		formula="H2O",
		state="l",
		mole_fraction=1.0
)

# condition examples
temperature = Temperature(value=298.15, unit="K")
pressure = Pressure(value=1.0, unit="atm")
```

## 📝 API Documentation


### 🧩 Models

- **Component**

	- `name`: str — Name of the component
	- `formula`: str — Chemical formula
	- `state`: Literal['g', 'l', 's', 'aq'] — State (gas, liquid, solid, aqueous)
	- `mole_fraction`: float — Mole fraction (default 1.0)

- **Temperature**

	- `value`: float — Temperature value
	- `unit`: str — Unit (e.g., 'K', 'C', 'F')

- **Pressure**

	- `value`: float — Pressure value
	- `unit`: str — Unit (e.g., 'bar', 'atm', 'Pa')

- **ComponentConfig**

	- `databook`: str — Name of the databook
	- `table`: str — Table name
	- `mode`: str — Mode (e.g., 'DATA', 'EQUATION')
	- `label`: str — Optional label
	- `labels`: dict[str, str] — Optional labels

- **ReferenceThermoDB**

	- `reference`: Dict[str, List[str]] — References and contents
	- `contents`: List[str] — Reference contents
	- `configs`: Dict[str, ComponentConfig] — Reference configs
	- `rules`: Dict[str, ComponentRule] — Reference rules
	- `labels`, `ignore_labels`, `ignore_props`: Optional label/property management

- **ComponentReferenceThermoDB**

	- `component`: Component
	- `reference_thermodb`: ReferenceThermoDB

- **ReferencesThermoDB**

    - Handles multiple references, contents, configs, rules, and label management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request to improve the project.

## 📝 License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software in your own applications or projects. However, if you choose to use this app in another app or software, please ensure that my name, Sina Gilassi, remains credited as the original author. This includes retaining any references to the original repository or documentation where applicable. By doing so, you help acknowledge the effort and time invested in creating this project.

## ❓ FAQ

For any questions, contact me on [LinkedIn](https://www.linkedin.com/in/sina-gilassi/).

## 👨‍💻 Authors

- [@sinagilassi](https://www.github.com/sinagilassi)
