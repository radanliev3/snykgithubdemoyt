# demo_snyk_scan.py
import subprocess
import json
import sys

def run_snyk_test():
    try:
        result = subprocess.run(
            ["snyk", "test", "--severity-threshold=high", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Snyk test failed:", e.stderr, file=sys.stderr)
        sys.exit(e.returncode)

def main():
    report = run_snyk_test()
    vulnerabilities = report.get("vulnerabilities", [])
    print(f"💣 High-severity vulnerabilities found: {len(vulnerabilities)}")
    for vuln in vulnerabilities:
        print(f"- {vuln['id']}: {vuln['packageName']} {vuln['severity']}")

    if vulnerabilities:
        sys.exit(1)
    print("✅ No high-severity issues found.")

if __name__ == "__main__":
    main()
