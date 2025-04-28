# Flutter String Scanner

A tool to scan Flutter projects for untranslated static strings, helping developers improve multi-language support by identifying strings that should be replaced with standard localization methods.

## Installation

Add this to your `pubspec.yaml`:

```yaml
dev_dependencies:
  flutter_string_scanner: ^1.0.1

Or install it globally for CLI usage:
dart pub global activate flutter_string_scanner

Usage
Run the scanner from the command line:
flutter_string_scanner --path /path/to/flutter/project

Or, if added as a dependency:
dart run flutter_string_scanner: --path /path/to/flutter/project

Options

--path: Specify the Flutter project directory (default: current directory).
--exclude-dirs: List of directories to exclude (default: build, .dart_tool, generated).
--exclude-files: List of files to exclude (default: main.dart).

Example:
flutter_string_scanner --path ./my_project --exclude-dirs test assets --exclude-files home.dart

Features

Detects static strings in .dart files that are not used in localization contexts.
Supports excluding specific directories and files.
Generates a detailed report with file paths, line numbers, and the static strings found.
Ideal for preparing Flutter apps for multi-language support.

Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.
License
MIT License```
