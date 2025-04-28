import 'dart:io';
import 'package:args/args.dart';

/// Runs the Flutter String Scanner tool to detect untranslated static strings.
Future<void> scanProject({
  String projectPath = '.',
  List<String> excludeDirs = const ['build', '.dart_tool', 'generated'],
  List<String> excludeFiles = const ['main.dart'],
}) async {
  final dir = Directory(projectPath);
  final staticStrings = <String>[];

  // Recursively scan .dart files
  await for (final entity in dir.list(recursive: true)) {
    if (entity is File && entity.path.endsWith('.dart')) {
      final filePath = entity.path;
      if (excludeDirs.any((dir) => filePath.contains(dir)) ||
          excludeFiles.contains(File(filePath).uri.pathSegments.last)) {
        continue;
      }

      final content = await entity.readAsString();
      final lines = content.split('\n');

      // Regex for static strings (double or single quotes)
      final stringPattern = RegExp(r'''("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')''');
          final matches = stringPattern.allMatches(content);

      for (final match in matches) {
        final string = match.group(0)!;
        final startPos = match.start;
        final lineNumber = content.substring(0, startPos).split('\n').length;

        // Skip strings in comments or localization contexts
        final line = lines[lineNumber - 1];
        if (line.contains('//') ||
            line.contains('AppLocalizations.of(context)') ||
            line.contains('S.of(context)')) {
          continue;
        }

        staticStrings.add('File: $filePath, Line: $lineNumber, String: $string');
      }
    }
  }

  // Generate report
  if (staticStrings.isEmpty) {
    print('No untranslated static strings found.');
  } else {
    print('Untranslated Static Strings Report');
    print('=' * 40);
    print(staticStrings.join('\n' + '-' * 40 + '\n'));
  }
}

void main(List<String> arguments) {
  final parser = ArgParser()
    ..addOption('path',
        defaultsTo: '.',
        help: 'Path to the Flutter project directory (default: current directory)')
    ..addMultiOption('exclude-dirs',
        defaultsTo: ['build', '.dart_tool', 'generated'],
        help: 'Directories to exclude from scanning')
    ..addMultiOption('exclude-files',
        defaultsTo: ['main.dart'],
        help: 'Files to exclude from scanning');

  final results = parser.parse(arguments);

  scanProject(
    projectPath: results['path'] as String,
    excludeDirs: results['exclude-dirs'] as List<String>,
    excludeFiles: results['exclude-files'] as List<String>,
  );
}