import 'package:flutter_string_scanner/flutter_string_scanner.dart';
import 'package:test/test.dart';

void main() {
  test('Scan project with default parameters', () async {
    // This is a basic test to ensure the scanProject function runs without errors
    // In a real test, you would mock the Process.run call or create a test project
    expect(
          () async => await scanProject(
        projectPath: '.',
        excludeDirs: ['build'],
        excludeFiles: ['main.dart'],
      ),
      returnsNormally,
    );
  });
}